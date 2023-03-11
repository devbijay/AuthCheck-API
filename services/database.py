import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
DATABASE = os.getenv("DATABASE")
client = MongoClient(DATABASE)
db = client.VerifySaas
