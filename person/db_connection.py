import pymongo

url = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'test'


client = pymongo.MongoClient(url)
mongo_db = client[MONGO_DB_NAME]