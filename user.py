from pymongo import MongoClient

# Replace these with your MongoDB connection details
mongo_host = 'localhost'
mongo_port = 27017
database_name = 'queryres'
collection_name = 'userid'

# Connect to MongoDB
client = MongoClient(mongo_host, mongo_port)
db = client[database_name]
collection = db[collection_name]

# Data to be inserted
user_data = {"phone_number": "70348638587", "user_id": 50}

# Insert the data into the collection
result = collection.insert_one(user_data)

# Print the inserted document's ID
print(f"Inserted document ID: {result.inserted_id}")

# Close the MongoDB connection
client.close()