from flask import Flask, request, jsonify
from azure.cosmos import CosmosClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration details
COSMOS_DB_URI = os.getenv("COSMOS_DB_URI")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
DATABASE_NAME = os.getenv("DATABASE_NAME")
CONVERSATION_LOG_CONTAINER = os.getenv("CONVERSATION_LOG_CONTAINER")
CONVERSATION_ERROR_CONTAINER = os.getenv("CONVERSATION_ERROR_CONTAINER")


# Initialize the Cosmos client
client = CosmosClient(COSMOS_DB_URI, COSMOS_DB_KEY)
database = client.get_database_client(DATABASE_NAME)

def query_cosmos_db(container_name, date_field, user_name, from_time, to_time, prompt):
    container = database.get_container_client(container_name)
    
    # Base query without the prompt condition
    query = f"""
    SELECT * FROM c 
    WHERE c.userName = @userName 
    AND c.{date_field} >= @fromTime 
    AND c.{date_field} <= @toTime
    """
    
    # Define base parameters
    parameters = [
        {"name": "@userName", "value": user_name},
        {"name": "@fromTime", "value": from_time},
        {"name": "@toTime", "value": to_time}
    ]

    # Add prompt condition if prompt is provided
    if prompt:
        query += " AND CONTAINS(c.convPrompt, @prompt)"
        parameters.append({"name": "@prompt", "value": prompt})
    
    items = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    
    filtered_items = [
        {k: v for k, v in item.items() if not k.startswith('_')}
        for item in items
    ]
    
    return filtered_items

@app.route('/getLogs', methods=['GET'])
def get_logs():
    user_name = request.args.get('user_name')
    from_time = request.args.get('from_time')
    to_time = request.args.get('to_time')
    prompt = request.args.get('prompt')
    log_type = request.args.get('log_type')

    if not all([user_name, from_time, to_time, log_type]):
        return jsonify({"error": "Missing one or more required parameters"}), 400

    if log_type.upper() == "C":
        container_name = CONVERSATION_LOG_CONTAINER
        date_field = "convDateTime"
    elif log_type.upper() == "E":
        container_name = CONVERSATION_ERROR_CONTAINER
        date_field = "errorDateTime"
    else:
        return jsonify({"error": "Invalid log type. Use 'C' for conversation logs and 'E' for error logs."}), 400

    items = query_cosmos_db(container_name, date_field, user_name, from_time, to_time, prompt)

    if items:
        return jsonify(items), 200
    else:
        return jsonify({"message": "No matching records found."}), 200

if __name__ == '__main__':
    app.run(debug=True)
