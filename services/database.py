import os

from pymongo import MongoClient

DATABASE = os.getenv("DATABASE")
client = MongoClient(DATABASE)
db = client.VerifySaas