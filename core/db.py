import os
import datetime

try:
    from pymongo import MongoClient
    from pymongo.server_api import ServerApi
    from bson.objectid import ObjectId
except ImportError:
    MongoClient = None
    ServerApi = None
    ObjectId = None

def get_mongo_client():
    """
    Retrieves the MongoClient configured with the environment-supplied MONGO_URI.
    Falls back to localhost if the variable is not set.
    """
    if MongoClient is None or ServerApi is None:
        raise ImportError('pymongo is required for MongoDB-backed appointment actions.')

    uri = os.environ.get('MONGO_URI')
    if not uri:
        uri = "mongodb://localhost:27017/"
    
    return MongoClient(uri, server_api=ServerApi('1'))

def test_mongo_connection():
    """
    Pings the MongoDB server to verify a successful connection.
    Returns (status, message).
    """
    client = get_mongo_client()
    try:
        client.admin.command('ping')
        return True, "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        return False, str(e)
    finally:
        client.close()
def save_appointment_to_mongodb(data):
    """
    Saves the validated appointment form data as a document in the MongoDB database collection.
    """
    client = get_mongo_client()
    try:
        db = client.get_database('neurotech')
        collection = db.get_collection('appointments')
        
        document = {
            'full_name': data.get('full_name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'company': data.get('company', ''),
            'service': data.get('service'),
            'message': data.get('message', ''),
            'status': 'NEW',
            'note': '',
            'created_at': datetime.datetime.utcnow()
        }
        
        result = collection.insert_one(document)
        return result.inserted_id
    finally:
        client.close()

def get_all_appointments():
    """
    Fetches all appointments sorted by created_at descending.
    """
    client = get_mongo_client()
    try:
        db = client.get_database('neurotech')
        collection = db.get_collection('appointments')
        appointments = list(collection.find().sort('created_at', -1))
        # Convert ObjectId to string for easy templating
        for appt in appointments:
            appt['id_str'] = str(appt['_id'])
        return appointments
    finally:
        client.close()

def update_appointment(appt_id, status=None, note=None):
    """
    Updates the status or note for a specific appointment document.
    """
    if ObjectId is None:
        raise ImportError('pymongo is required for MongoDB-backed appointment actions.')

    client = get_mongo_client()
    try:
        db = client.get_database('neurotech')
        collection = db.get_collection('appointments')
        
        update_fields = {}
        if status is not None:
            update_fields['status'] = status
        if note is not None:
            update_fields['note'] = note
            
        if update_fields:
            collection.update_one({'_id': ObjectId(appt_id)}, {'$set': update_fields})
    finally:
        client.close()

def delete_appointment(appt_id):
    """
    Deletes an appointment document from the collection by ID.
    """
    if ObjectId is None:
        raise ImportError('pymongo is required for MongoDB-backed appointment actions.')

    client = get_mongo_client()
    try:
        db = client.get_database('neurotech')
        collection = db.get_collection('appointments')
        collection.delete_one({'_id': ObjectId(appt_id)})
    finally:
        client.close()
