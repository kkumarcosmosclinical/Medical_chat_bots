# mongo_utils.py
from pymongo import MongoClient
from urllib.parse import quote_plus
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

# Function to establish a connection to the MongoDB database
def get_db_connection():
    # Use configuration settings
    mongo_uri = settings.get_mongo_uri()
    client = MongoClient(mongo_uri)
    return client[settings.MONGO_DBNAME]

# ... rest of the functions ...
# mongo_utils.py
# ... existing code for get_db_connection ...

# Function to get a collection from the database
def get_collection(collection_name):
    db = get_db_connection()
    return db[collection_name]

# Function to insert or update the study and collection name
def insert_or_update_study(study, collection_name):
    collection = get_collection('collection_data')  # Use your actual collection name
    existing_study = collection.find_one({"study": study})
    if existing_study:
        # If study exists, check if the new collection_name is already in the list
        if collection_name not in existing_study.get("collection_names", []):
            # If not, add it to the list
            collection.update_one(
                {"study": study},
                {"$push": {"collection_names": collection_name}}
            )
    else:
        # If study does not exist, insert a new document with collection_names as a list
        collection.insert_one({"study": study, "collection_names": [collection_name]})

def get_all_studies():
    collection = get_collection('collection_data')  # Use your actual collection name
    studies = collection.find({}, {'_id': 0})
    return list(studies)
# Function to get all collection names for a specific study
def get_collections_by_study(study_name):
    collection = get_collection('collection_data')  # Use your actual collection name
    study_data = collection.find_one({"study": study_name}, {'_id': 0, 'collection_names': 1})
    if study_data:
        return study_data.get('collection_names', [])
    else:
        return {"Error":"study name does not exist"}