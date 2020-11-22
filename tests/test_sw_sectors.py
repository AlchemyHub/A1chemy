import json
import a1chemy.data_source as data_source
import pymongo


def test_parse_sw_sectors():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/", username='a1chemy', password='1B2C9046-E3CC-447F-9961-E125759BA44F')
    mongo_tags_client = data_source.MongoTags(mongo_client=mongo_client)
    swsindex_tag_tree = mongo_tags_client.tree(id='汽车')
    print(swsindex_tag_tree.root)


def test_find_children():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/", username='a1chemy', password='1B2C9046-E3CC-447F-9961-E125759BA44F')
    mongo_tags_client = data_source.MongoTags(mongo_client=mongo_client)
    result = mongo_tags_client.find_children(parent_list=['汽车'])
    print(result)

test_parse_sw_sectors()
# test_find_children()