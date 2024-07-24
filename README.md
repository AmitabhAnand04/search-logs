# API Documentation

## Overview

This API provides endpoints to retrieve logs from Azure Cosmos DB. It allows querying conversation logs and error logs based on various parameters such as username, time range, and optional prompts.

## Base URL

`http://<your-domain>/`

## Endpoints

### 1. Get Logs

**Endpoint:** `/getLogs`

**Method:** `GET`

**Description:** Retrieves logs from Azure Cosmos DB based on the provided parameters.

**Parameters:**

| Name      | Type   | Required | Description                                                                                                                                                    |
|-----------|--------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| user_name | String | Yes      | The username to filter logs.                                                                                                                                   |
| from_time | String | Yes      | The start time for the logs in ISO 8601 format (e.g., `2023-01-01T00:00:00Z`).                                                                                 |
| to_time   | String | Yes      | The end time for the logs in ISO 8601 format (e.g., `2023-01-31T23:59:59Z`).                                                                                    |
| prompt    | String | No       | An optional parameter to filter logs containing this prompt.                                                                                                    |
| log_type  | String | Yes      | The type of logs to retrieve. Use 'C' for conversation logs and 'E' for error logs.                                                                              |

**Responses:**

- **200 OK**

  - **Description:** Logs successfully retrieved.
  - **Body:**
    ```json
    [
        {
            "log_id": "1",
            "user_name": "john_doe",
            "convDateTime": "2023-01-01T12:00:00Z",
            "convPrompt": "How to use the API?",
            "convResponse": "Here's how you use the API..."
        },
        ...
    ]
    ```

  - **Description:** No matching records found.
  - **Body:**
    ```json
    {
        "message": "No matching records found."
    }
    ```

- **400 Bad Request**

  - **Description:** Missing or invalid parameters.
  - **Body:**
    ```json
    {
        "error": "Missing one or more required parameters"
    }
    ```
    or
    ```json
    {
        "error": "Invalid log type. Use 'C' for conversation logs and 'E' for error logs."
    }
    ```

## Example Request

### Request

```http
GET /getLogs?user_name=john_doe&from_time=2023-01-01T00:00:00Z&to_time=2023-01-31T23:59:59Z&prompt=API&log_type=C
```

### Response

```json
[
    {
        "log_id": "1",
        "user_name": "john_doe",
        "convDateTime": "2023-01-01T12:00:00Z",
        "convPrompt": "How to use the API?",
        "convResponse": "Here's how you use the API..."
    }
]
```

## Environment Variables

The API relies on the following environment variables configured in a `.env` file:

- **COSMOS_DB_URI:** The URI for the Azure Cosmos DB account.
- **COSMOS_DB_KEY:** The primary key for the Azure Cosmos DB account.
- **DATABASE_NAME:** The name of the database in Cosmos DB.
- **CONVERSATION_LOG_CONTAINER:** The name of the container for conversation logs.
- **CONVERSATION_ERROR_CONTAINER:** The name of the container for error logs.

## Error Handling

The API returns appropriate HTTP status codes and error messages for missing parameters, invalid log types, and other issues.

## Run the Application

To run the application, execute the following command:

```bash
python app.py
```

Ensure that the `.env` file is properly configured with the required environment variables.
