# User Publications Microservice

## Project Overview

This service provides an API endpoint to retrieve publications associated with a user. It uses a Flask backend, authenticates users via JWT tokens, and fetches data from a MongoDB database. The project is containerized using Docker and includes GitHub Actions workflows for CI/CD.

## Folder Structure

Here's an overview of the main folders and their purposes:

-   **`.github/`**: Contains GitHub Actions workflows and other GitHub-specific configurations.
    -   **`.github/workflows/`**: Holds YAML files defining CI/CD pipelines, such as Docker image building/publishing and deployment.
        -   `docker-publish.yml`: Workflow for building, publishing, and deploying the Docker image for the main branch.
        -   `docker-publish_qa.yml`: (Assumed) Workflow for a QA or testing environment.
-   **`conections/`**: Manages database connections.
    -   `mongo.py`: Contains logic to establish a connection with the MongoDB database.
-   **`services/`**: Contains the business logic of the application.
    -   `functions.py`: Includes functions that perform core operations, like fetching user publications.
-   **`tests/`**: Holds automated tests for the application.
    -   `route_test.py`: (Assumed) Contains tests for the API routes.
    -   `test_get_publications.py`: Contains tests for the "get publications" functionality.
-   **`__pycache__/`**: Contains Python bytecode cache files (auto-generated and usually ignored by version control).

Key files in the root directory:

-   `.gitignore`: Specifies files and directories to be ignored by Git.
-   `dockerfile`: Instructions for building the Docker image of the application.
-   `main.py`: The main entry point for the Flask web application. It defines API endpoints, handles requests, and coordinates with the service layer.
-   `requirements.txt`: Lists the Python dependencies required for the project.

## Backend Design Pattern

The application follows a **Layered Architecture** pattern:

1.  **Presentation Layer (`main.py`)**: Handles incoming HTTP requests, performs authentication (JWT decoding), delegates to the service layer, and formats the API response (JSON).
2.  **Service Layer (`services/functions.py`)**: Encapsulates the core business logic. For example, the `user_publications` function orchestrates data retrieval.
3.  **Data Access Layer (`conections/mongo.py` and its usage in `services/functions.py`)**: Responsible for all database interactions, primarily with MongoDB.

## Communication Architecture

-   **API Style**: The service exposes a **RESTful API**.
-   **Protocol**: Communication is over **HTTP/HTTPS**.
-   **Data Format**: **JSON** is used for request and response bodies.
-   **Authentication**: Endpoints are secured using **JWT (JSON Web Tokens)**. Clients must provide a Bearer token in the `Authorization` header.
-   **Database Communication**: The service communicates with a **MongoDB** instance for data persistence and retrieval. Connection details are managed via environment variables.

## Folder Pattern

The project uses a **Layer-Based Folder Pattern**. Components are organized into directories based on their architectural layer or technical responsibility, rather than by application feature. This includes distinct folders for `services` (business logic), `conections` (data access), and `tests`.

## API Endpoints

### Get User Publications

Retrieves all non-archived (Status != 0) publications for the authenticated user.

-   **URL:** `/my-publications`
-   **HTTP Method:** `GET`
-   **Headers:**
    -   `Authorization`: **Required**. A JWT Bearer token.
        -   Format: `Bearer <your_jwt_token>`
-   **Request Body:** None.
-   **Query Parameters:** None.

-   **Success Response (`200 OK`):**
    -   **Content-Type:** `application/json`
    -   **Body:** An array of publication objects.
        ```json
        [
          {
            "_id": "stringified_object_id",
            "Id_user": "user_id_associated_with_token",
            "Status": 1, // Example: Status is not 0
            "Datepublish": "stringified_date_value",
            // ... other fields related to the publication
          }
          // ... more publications
        ]
        ```

-   **Error Responses:**
    -   **`401 Unauthorized`**:
        -   `{"error": "Token missing or invalid"}` (If Authorization header is missing or malformed)
        -   `{"error": "Invalid token data"}` (If JWT payload is missing `user_id`)
        -   `{"error": "Token expired"}`
        -   `{"error": "Invalid token"}`
    -   **`500 Internal Server Error`**:
        -   `{"error": "description_of_the_server_error"}`

