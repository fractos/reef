import sqlite3
import abc
from .base import Database

from logzero import logger

class SqliteDatabase(Database):

    def initialise(self, settings):
        logger.info("sqlite_database: initialise()")
        con = None

        create = False

        self.db_name = settings["db_name"]

        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute("SELECT * FROM query")
            _ = cur.fetchone()
        except sqlite3.Error:
            # no table
            create = True
        finally:
            if con:
                con.close()

        if create:
            self.create_schema()
        else:
            logger.info("sqlite_database: schema ready")


    def create_schema(self):
        logger.debug("sqlite_database: create_schema()")
        con = None

        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute("CREATE TABLE query (id TEXT, search TEXT)")
            con.commit()
            cur.execute("CREATE TABLE result (id TEXT, query TEXT, timestamp TEXT, title TEXT, content TEXT)")
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during create_schema() - %s" % str(e))
        finally:
            if con:
                con.close()

    def get_query(self, query_id):
        logger.debug("sqlite_database: get_query()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('''SELECT * FROM query WHERE id = ?''',
                (query_id))
            data = cur.fetchone()
            return data
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during get_query() - %s" % str(e))
        finally:
            if con:
                con.close()


    def get_all_queries(self):
        logger.debug("sqlite_database: get_all_queries()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM query")
            data = cur.fetchall()
            return data
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during get_all_queries() - %s" % str(e))
            return None
        finally:
            if con:
                con.close()


    def save_query(self, query):
        logger.debug("sqlite_database: save_query()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute("INSERT INTO query VALUES (?, ?)", (query.id,query.search))
            con.commit()
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during save_query() - %s" % str(e))
        finally:
            if con:
                con.close()


    def remove_query(self, query):
        logger.debug("sqlite_database: remove_query()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute("DELETE FROM query WHERE id = ?",
                (query.id))
            con.commit()
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during remove_query() - %s" % str(e))
        finally:
            if con:
                con.close()


    def get_result(self, result_id):
        logger.debug("sqlite_database: get_result()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('''SELECT * FROM result WHERE id = ?''',
                (result_id,))
            data = cur.fetchone()
            return data
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during get_result() - %s" % str(e))
        finally:
            if con:
                con.close()


    def get_all_results_for_query(self, query_id):
        logger.debug("sqlite_database: get_all_results_for_query()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM result WHERE query = ? ORDER BY timestamp DESC", (query_id,))
            data = cur.fetchall()
            return data
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during get_all_results_for_query() - %s" % str(e))
            return None
        finally:
            if con:
                con.close()


    def get_top_results_for_query(self, query_id, num_results=10):
        logger.debug("sqlite_database: get_top_results_for_query()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM result WHERE query = ? ORDER BY timestamp DESC LIMIT ?", (query_id, num_results))
            data = cur.fetchall()
            return data
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during get_top_results_for_query() - %s" % str(e))
            return None
        finally:
            if con:
                con.close()


    def get_all_results(self):
        logger.debug("sqlite_database: get_all_results()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM result")
            data = cur.fetchall()
            return data
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during get_all_results() - %s" % str(e))
            return None
        finally:
            if con:
                con.close()


    def save_result(self, result):
        logger.debug("sqlite_database: save_result()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute("INSERT INTO result VALUES (?,?,?,?,?)",
                (result.id, result.query, result.timestamp, result.title, result.content))
            con.commit()
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during save_result() - %s" % str(e))
        finally:
            if con:
                con.close()


    def result_exists(self, result):
        logger.debug("sqlite_database: result_exists()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute('''SELECT COUNT(*) FROM result WHERE query = ? AND title = ? AND content = ?''',
                (result.query, result.title, result.content))
            data = cur.fetchone()
            return int(data[0]) > 0
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during result_exists() - %s" % str(e))
        finally:
            if con:
                con.close()


    def remove_result(self, result):
        logger.debug("sqlite_database: remove_result()")
        con = None
        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute("DELETE FROM result WHERE id = ?",
                (result.id,))
            con.commit()
        except sqlite3.Error as e:
            logger.error("sqlite_database: problem during remove_result() - %s" % str(e))
        finally:
            if con:
                con.close()
