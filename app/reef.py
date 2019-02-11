from logzero import logger
import logging
import logzero
from urllib.parse import urlparse
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from concurrent.futures.thread import ThreadPoolExecutor
import re
import socket
import http.client
import json
import time
import requests
import signal
import os
import boto3
import uuid
from datetime import datetime
from gsearch.googlesearch import search
from feedgen.feed import FeedGenerator
from models import Query, Result
import settings

requested_to_quit = False

def main():
    logger.info("starting...")

    setup_signal_handling()

    global db
    db = settings.get_database()

    read_config()

    while lifecycle_continues():
        lifecycle()

        if lifecycle_continues():
            logger.info("sleeping for %s seconds..." % settings.SLEEP_SECONDS)
            for _ in range(settings.SLEEP_SECONDS):
                if lifecycle_continues():
                    time.sleep(1)


def read_config():
    global db

    if settings.CONFIG_FILE:
        logger.info("reading config file: " + settings.CONFIG_FILE)
        config = json.loads(
            get_file_or_s3(settings.CONFIG_FILE)
        )

        for query_config in config["queries"]:
            query = Query(json=query_config)
            db.save_query(query)
            logger.debug("saved query " + query.id + ": " + query.search)


def lifecycle_continues():
    return not requested_to_quit


def signal_handler(signum, frame):
    logger.info("Caught signal %s" % signum)
    global requested_to_quit
    requested_to_quit = True


def setup_signal_handling():
    logger.info("setting up signal handling")
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


def get_file_or_s3(uri):
    logger.debug("getting file URI %s" % uri)

    if uri.lower().startswith("s3://"):
        s3 = boto3.resource("s3")
        parse_result = urlparse(uri)
        s3_object = s3.Object(parse_result.netloc, parse_result.path.lstrip("/"))
        return s3_object.get()["Body"].read().decode("utf-8")

    with open(uri) as file:
        return file.read()


def write_to_file_or_s3(uri, query, body):
    logger.debug(f"writing to file URI {uri}/{query.id}.xml")

    if uri.lower().startswith("s3://"):
        s3 = boto3.resource("s3")
        parse_result = urlparse(uri)
        bucket = parse_result.netloc
        key = parse_result.path.lstrip("/") + f"{query.id}.xml"
        logger.debug(f"s3 bucket: {bucket} key: {key}")
        s3_object = s3.Object(bucket, key)
        s3_object.put(Body=body)
        if settings.S3_SET_PUBLIC_ACL:
            logger.debug("putting s3 acl for public-read")
            object_acl = s3.ObjectAcl(bucket, key)
            object_acl.put(ACL='public-read')
    else:
        with open(f"{uri}/{query.id}", "w") as file:
            file.write(body)


def get_now_as_timestamp():
    return datetime.now()


def lifecycle():
    global db

    queries = db.get_all_queries()

    for query_raw in queries:
        query = Query(json=query_raw)
        logger.debug(f'checking query {query.id}')

        logger.debug("performing search...")
        results = search(query.search, num_results=10)
        logger.info(f"query {query.id}: hits: {len(results)}")

        new_items = False

        for result_raw in results:
            #logger.debug(f'result_raw: {result_raw[0]}\t {result_raw[1]}')

            result = Result(
                id=str(uuid.uuid4()),
                query=query.id,
                timestamp=str(get_now_as_timestamp()),
                title=result_raw[0],
                content=result_raw[1])

            logger.debug("result: " + json.dumps(
                result.as_dict(),
                indent=4,
                sort_keys=True))

            if not db.result_exists(result):
                logger.debug("result has not previously been recorded")
                new_items = True
                db.save_result(result)

        if new_items:
            feed_string = generate_feed_for_query(query)
            write_to_file_or_s3(uri=settings.RESULTS_FOLDER, query=query, body=feed_string)


def generate_feed_for_query(query):
    global db

    logger.debug("generate_feed_for_query()")
    results = db.get_top_results_for_query(query.id)

    fg = FeedGenerator()
    fg.id(f"{settings.BASE_URL}/results/{query.id}")
    fg.title(f"Results for {query.search}")
    fg.author({"name": "Reef", "email": "reef@fractos.com"})
    fg.description("A list of latest results for a search")
    fg.link(href=settings.BASE_URL)
    fg.language("en")

    for result_raw in results:
        result = Result(json=result_raw)
        logger.debug(f"adding entry for {result.id}: {result.title}: {result.content}")
        fe = fg.add_entry()
        fe.id(f"{settings.BASE_URL}/results/{query.id}/{result.id}")
        fe.title(result.title)
        fe.link(href=result.content)

    if settings.FEED_FORMAT == "rss":
        return fg.rss_str(pretty=True)
    # else...
    return fg.atom_str(pretty=True)


if __name__ == "__main__":
    if settings.DEBUG:
        logzero.loglevel(logging.DEBUG)
    else:
        logzero.loglevel(logging.INFO)

    main()
