import abc

class Database(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def initialise(self, settings):
        raise NotImplementedError("must define initialise() to use this base class")

    @abc.abstractmethod
    def get_query(self, query_id):
        raise NotImplementedError("must define get_query() to use this base class")

    @abc.abstractmethod
    def get_all_queries(self):
        raise NotImplementedError("must define get_all_queries() to use this base class")

    @abc.abstractmethod
    def save_query(self, query):
        raise NotImplementedError("must define save_query() to use this base class")

    @abc.abstractmethod
    def remove_query(self, query):
        raise NotImplementedError("must define remove_query() to use this base class")

    @abc.abstractmethod
    def get_result(self, result_id):
        raise NotImplementedError("must define get_result() to use this base class")

    @abc.abstractmethod
    def get_all_results_for_query(self, query_id):
        raise NotImplementedError("must define get_all_results_for_query() to use this base class")

    @abc.abstractmethod
    def get_top_results_for_query(self, query_id, num_items):
        raise NotImplementedError("must define get_top_results_for_query() to use this base class")

    @abc.abstractmethod
    def get_all_results(self):
        raise NotImplementedError("must define get_all_results() to use this base class")

    @abc.abstractmethod
    def save_result(self, result):
        raise NotImplementedError("must define save_result() to use this base class")

    @abc.abstractmethod
    def result_exists(self, result):
        raise NotImplementedError("must define result_exists() to use this base class")

    @abc.abstractmethod
    def remove_result(self, result):
        raise NotImplementedError("must define remove_result() to use this base class")
