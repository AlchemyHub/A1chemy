from a1chemy.common import Tag


class MongoTag(object):
    mongo_client = None
    db = None
    tags_collection = None

    def __init__(self, mongo_client) -> None:
        self.mongo_client = mongo_client
        self.db = mongo_client["a1chemy"]
        self.tags_collection = self.db['tags']

    