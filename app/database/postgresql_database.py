import psycopg2
import psycopg2.extras
import abc
from .base import Database
from logzero import logger

class PostgreSqlDatabase(Database):

    def initialise(self, settings):
        logger.info("postgresql_database: initialise()")
        con = None

        create = False

        self.connection_string = "dbname='%s' user='%s' host='%s' password='%s'" % \
            (settings["dbname"], settings["user"], settings["host"], settings["password"])

        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor()
            cur.execute("SELECT * FROM query")
        except psycopg2.Error:
            # no table
            create = True
        finally:
            if con:
                con.close()

        if create:
            self.create_schema()
        else:
            logger.info("postgresql_database: schema ready")


    def create_schema(self):
        logger.debug("postgresql_database: create_schema()")
        con = None

        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor()
            cur.execute("CREATE TABLE query (id CHARACTER VARYING(100), search CHARACTER VARYING(100))")
            con.commit()
            cur.execute("CREATE TABLE result (id CHARACTER VARYING(100), query CHARACTER VARYING(100), timestamp CHARACTER VARYING(100), title CHARACTER VARYING(200), content CHARACTER VARYING(500))")
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during create_schema() - %s" % str(e))
        finally:
            if con:
                con.close()


    def get_query(self, query_id):
        logger.debug("postgresql_database: get_query()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('''SELECT * FROM query WHERE id=%s''',
                (query_id))
            data = cur.fetchone()
            return data
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during get_query() - %s" % str(e))
        finally:
            if con:
                con.close()


    def get_all_queries(self):
        logger.debug("postgresql_database: get_all_queries()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM query")
            data = cur.fetchall()
            return data
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during get_all_queries() - %s" % str(e))
            return None
        finally:
            if con:
                con.close()


    def save_query(self, query):
        logger.debug("postgresql_database: save_query()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor()
            cur.execute("INSERT INTO query VALUES (%s, %s)",
                (query.id, query.search))
            con.commit()
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during save_query() - %s" % str(e))
        finally:
            if con:
                con.close()


    def remove_query(self, query):
        logger.debug("postgresql_database: remove_query()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor()
            cur.execute("DELETE FROM query WHERE id = %s",
                (query.id))
            con.commit()
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during remove_query() - %s" % str(e))
        finally:
            if con:
                con.close()


    def get_result(self, result_id):
        logger.debug("postgresql_database: get_result()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('''SELECT * FROM result WHERE id = %s''',
                (result_id,))
            data = cur.fetchone()
            return data
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during get_result() - %s" % str(e))
        finally:
            if con:
                con.close()


    def get_all_results_for_query(self, query_id):
        logger.debug("postgresql_database: get_all_results_for_query()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM result WHERE query = %s ORDER BY timestamp DESC", (query_id,))
            data = cur.fetchall()
            return data
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during get_all_results_for_query() - %s" % str(e))
            return None
        finally:
            if con:
                con.close()


    def get_top_results_for_query(self, query_id, num_results=10):
        logger.debug("postgresql_database: get_top_results_for_query()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM result WHERE query = %s LIMIT %s ORDER BY timestamp DESC", (query_id, num_results))
            data = cur.fetchall()
            return data
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during get_top_results_for_query() - %s" % str(e))
            return None
        finally:
            if con:
                con.close()


    def get_all_results(self):
        logger.debug("postgresql_database: get_all_results()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM result")
            data = cur.fetchall()
            return data
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during get_all_results() - %s" % str(e))
            return None
        finally:
            if con:
                con.close()


    def save_result(self, result):
        logger.debug("postgresql_database: save_result()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor()
            cur.execute("INSERT INTO result VALUES (%s,%s,%s,%s,%s)",
                (result.id, result.query, result.timestamp, result.title, result.content))
            con.commit()
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during save_result() - %s" % str(e))
        finally:
            if con:
                con.close()


    def result_exists(self, result):
        logger.debug("postgresql_database: result_exists()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor()
            cur.execute('''SELECT COUNT(*) FROM result WHERE query = %s AND title = %s AND content = %s''',
                (result.query, result.title, result.content))
            data = cur.fetchone()
            return int(data[0]) > 0
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during result_exists() - %s" % str(e))
        finally:
            if con:
                con.close()


    def remove_result(self, result):
        logger.debug("postgresql_database: remove_result()")
        con = None
        try:
            con = psycopg2.connect(self.connection_string)
            cur = con.cursor()
            cur.execute("DELETE FROM result WHERE id = %s",
                (result.id,))
            con.commit()
        except psycopg2.Error as e:
            logger.error("postgresql_database: problem during remove_result() - %s" % str(e))
        finally:
            if con:
                con.close()
