from pymongo import MongoClient

# Replace these with your MongoDB connection details
mongo_host = 'localhost'
mongo_port = 27017
database_name = 'queryres'
collection_name_user = 'userid'
collection_name_orders = 'orders'

# Connect to MongoDB
client = MongoClient(mongo_host, mongo_port)
db = client[database_name]
collection_user = db[collection_name_user]
collection_orders = db[collection_name_orders]
user_id = None

# Function to get user info
def get_user_info(phone_number):
    # Query the database to find the user ID based on the phone number
    user_data = collection_user.find_one({"phone_number": phone_number})

    if user_data:
        global user_id
        user_id = user_data.get("user_id", "N/A")
        service_needed = user_data.get("service_needed", "N/A")

        return f"Your user ID is {user_id}. What service do you need? ({service_needed})"
    else:
        return "User not found."

phone_no = "9495864957"

# Call the function and print the result
output_message = get_user_info(phone_no)
print(output_message)

# Function to fetch response from MongoDB based on keyword
def get_response(keyword):
    response = db.responses.find_one({"keyword": keyword})
    return response["response"] if response else "Sorry, I couldn't find a suitable response."

# Function to handle booking
def book_order(order_details):
    # Check if the user ID already exists in the collection
    existing_order = collection_orders.find_one({"user_id": order_details["user_id"]})

    if existing_order:
        # User ID already exists, return a response indicating that the order is already booked
        return "Order already booked for this user ID."
    else:
        # User ID doesn't exist, insert the order details
        db.orders.insert_one(order_details)
        return "Booking successful! Your order has been placed."

def cancel_order(user_id):
    # Check if the order with the given user_id exists in the "orders" collection
    existing_order = collection_orders.find_one({"user_id": user_id})

    if existing_order:
        # If the order exists, delete it
        collection_orders.delete_one({"user_id": user_id})
        return "Order cancellation successful."
    else:
        # If the order doesn't exist, return a response indicating so
        return "No order in this user ID."
def process_user_input(user_input):
    # Implement your logic to determine the response keyword based on user input
    # This could involve tokenization, keyword extraction, or any other NLP technique
    # For simplicity, I'm using a basic keyword check in this example

    keywords = {
        "booking": ["book", "order", "reserve"],
        "cancelling": ["cancel", "delete", "remove"]
        # Add more keywords as needed
    }

    for keyword, synonyms in keywords.items():
        if any(synonym in user_input.lower() for synonym in synonyms):
            return keyword

    return "enquiry"

# Example usage
user_input = input("Enter your request: ")
response_keyword = process_user_input(user_input)  # Implement your logic to determine the keyword

if response_keyword == "booking":
    order_details = {"user_id": user_id, "status": "booked"}
    response = book_order(order_details)
elif response_keyword == "cancelling":
    user_id = user_id  # Replace with user identification logic
    response = cancel_order(user_id)
else:
    response = get_response(response_keyword)

print(response)

# Close the MongoDB connection
client.close()