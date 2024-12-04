from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()

def Getdb(DB_Name):
    uri = F"mongodb+srv://{os.getenv('MongoDB_User')}:{os.getenv('MongoDB_pass')}@nyster.4uqrj.mongodb.net/?retryWrites=true&w=majority&appName=Nyster"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        
    db=client[DB_Name]
    return db
