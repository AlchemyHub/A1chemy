from a1chemy.common.tag import Tree
from a1chemy.common import Tag
import itertools


class MongoTags(object):
    mongo_client = None
    db = None
    tags_collection = None

    def __init__(self, mongo_client) -> None:
        self.mongo_client = mongo_client
        self.db = mongo_client["a1chemy"]
        self.tags_collection = self.db['tags']

    def find(self, id=None):
        data = self.tags_collection.find_one({'id': id})
        return Tag(data)

    def tree(self, id=None):
        root = self.find(id=id)
        tree = Tree(root=root)
        parent_id_list = [root.id]
        while parent_id_list:
            print(parent_id_list)
            children_dict = self.find_children(parent_list=parent_id_list)
            next_parent_id_list = []
            for parent, children in children_dict.items():
                tree.add_relation(parent=parent, children=children)
                current_children_id_list = [child.id for child in children]
                next_parent_id_list.extend(current_children_id_list)
            parent_id_list = next_parent_id_list
        return tree

    def find_children(self, parent_list=None):
        query = {
            'parent': {
                '$in': parent_list
            }
        }
        data = self.tags_collection.find(query)
        return dict((k, list(map(lambda x: Tag(x), values))) for k, values in itertools.groupby(data, key=lambda x: x['parent']))

    def delete(self, id=None):
        return self.tags_collection.delete_many({'id': id})

    def insert(self, tag: Tag = None):
        """
        insert tag, if exsits, delete first.
        """
        query = {
            'id': tag.id,
            'parent':tag.parent
        }
        new_value = {
            '$set': tag.to_dict()
        }
        return self.tags_collection.update_one(query, new_value, upsert=True)
