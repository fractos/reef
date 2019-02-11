import os
import database
import re
import distutils.util
from database.sqlite_database import SqliteDatabase
from database.postgresql_database import PostgreSqlDatabase

DEBUG = bool(distutils.util.strtobool(os.getenv("DEBUG", "False")))
SLEEP_SECONDS = int(os.getenv("SLEEP_SECONDS"))
DB_TYPE = os.getenv("DB_TYPE")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", default="2"))
CONFIG_FILE = os.getenv("CONFIG_FILE", default="")
BASE_URL = os.getenv("BASE_URL", default="")
RESULTS_FOLDER = os.getenv("RESULTS_FOLDER", default="/tmp")
S3_SET_PUBLIC_ACL = bool(distutils.util.strtobool(os.getenv("S3_SET_PUBLIC_ACL", default="False")))
FEED_FORMAT = os.getenv("FEED_FORMAT", default="rss")

def get_database():
  if DB_TYPE == "postgresql":
    return get_database_postgresql()
  else:
    return get_database_sqlite()


def get_database_postgresql():
  db = PostgreSqlDatabase()
  db.initialise({
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "host": os.getenv("DB_HOST"),
    "password": os.getenv("DB_PASSWORD")
  })

  return db


def get_database_sqlite():
  db = SqliteDatabase()
  db.initialise({
    "db_name": os.getenv("DB_NAME")
  })

  return db
