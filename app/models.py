import json

class Query:
    """
    Hold the fields associated with a query
    """

    def __init__(self, json="", id="", search=""):
        if json:
            self.id = json["id"]
            self.search = json["search"]
        else:
            self.id = id
            self.search = search


    def as_dict(self):
        return {
            "id": self.id,
            "search": self.search
        }

class Result:
    """
    Holds the fields associated with a result
    """

    def __init__(self, json="", id="", query="", timestamp="", title="", content=""):
        if json:
            self.id = json["id"]
            self.query = json["query"]
            self.timestamp = json["timestamp"]
            self.title = json["title"]
            self.content = json["content"]
        else:
            self.id = id
            self.query = query
            self.timestamp = timestamp
            self.title = title
            self.content = content


    def as_dict(self):
        return {
            "id": self.id,
            "query": self.query,
            "timestamp": self.timestamp,
            "title": self.title,
            "content": self.content
        }
