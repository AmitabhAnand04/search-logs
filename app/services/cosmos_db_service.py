from azure.cosmos import CosmosClient
from flask import current_app

def query_cosmos_db(container_name, date_field, user_name, from_time, to_time, prompt):
    client = CosmosClient(current_app.config['COSMOS_DB_URI'], current_app.config['COSMOS_DB_KEY'])
    database = client.get_database_client(current_app.config['DATABASE_NAME'])
    container = database.get_container_client(container_name)
    
    query = f"""
    SELECT * FROM c 
    WHERE c.userName = @userName 
    AND c.{date_field} >= @fromTime 
    AND c.{date_field} <= @toTime
    """
    
    parameters = [
        {"name": "@userName", "value": user_name},
        {"name": "@fromTime", "value": from_time},
        {"name": "@toTime", "value": to_time}
    ]

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
