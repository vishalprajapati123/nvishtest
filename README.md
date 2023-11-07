# Setting Up a Django Project

This document outlines the process for setting up a Django development environment, preparing your Django project, and running it on Ubuntu and Windows systems.

## Prerequisites:
- Python 3 installed on your system
- Pip (Python package installer)

## 1. Setup Virtual Environment

### On Ubuntu:

Open a terminal and install `virtualenv` with pip:

```
pip install virtualenv
```

Create a new directory for your project and navigate into it:

```
mkdir nvishtest
cd nvishtest
```

Create a virtual environment:

```
virtualenv venv
```

Activate the virtual environment:

```
source venv/bin/activate
```

### On Windows:

Open a command prompt and use the built-in `venv` module to create a virtual environment:

```cmd
python -m venv env
```

Activate the virtual environment:

```cmd
.\env\Scripts\activate
```

## 2. Install Django and Requirements

With the virtual environment activated, install Django:

```sh
pip install django
```

If you have a `requirements.txt` file for your project, install the requirements using:

```sh
pip install -r requirements.txt
```

## 3. Initialize Django Project

If you're starting a new project:

```sh
git clone https://github.com/vishalprajapati123/nvishtest.git
```

Navigate to the project directory:

```sh
cd nvishtest
```

## 4. Migrate the Database

Apply the initial database migrations with:

```sh
python manage.py migrate
```

## 5. Create Superuser

To access the Django admin interface, create a superuser:

```sh
python manage.py createsuperuser
```

Follow the prompts to set up the superuser account.

## 6. Run Development Server

Start the Django development server:

```sh
python manage.py runserver
```

You'll find the server running at `http://127.0.0.1:8000/`. The admin interface will be at `http://127.0.0.1:8000/admin`.

---

**Deactivating the Virtual Environment:**

When you're finished working, deactivate the virtual environment with:

```sh
deactivate
```

**Notes:**

- Always activate the virtual environment when working on the project.
- Replace `my_django_project` and `myproject` with the actual names of your project directory and Django project.
- `python manage.py runserver` is only for development. For production, you should use a more robust server setup.

---

You're now set to develop with Django on your system!



# Exerciese1

## Overview
The Ping endpoint is a simple API endpoint that is used to check the responsiveness and connectivity of the server. When a GET request is made to this endpoint, it responds with a "pong" message, indicating that the server is reachable and functioning properly.

## Endpoint
- **URL: `/ping`
- **Method: `GET`
- **Auth required:** No

## Request
There are no parameters or body required for this request.

## Response

### Success Response
- **Condition:** If the request to the server is successful.
- **Code:** `200 OK`
- **Content example:**
```json
{
  "message": "pong"
}
```

### Error Response
Typically, this endpoint should always be accessible as long as the server is up and running. However, if there are any internal issues, you might receive a standard error response with a corresponding status code indicating the nature of the error.

## Example
Here is an example using `curl` from the command line:

```sh
curl -X GET http://localhost:8000/ping
```

This should return:

```json
{
  "message": "pong"
}
```

## Notes
- The `/ping` endpoint can be used for health checks or simple service monitoring.
- No authentication or additional headers are required for this endpoint.

---

# Exercise 2:

## Overview
The following documentation outlines two secured API endpoints, `/authorize` and `/generate-token`, which are used for user authentication and token management. The `/authorize` endpoint validates the user's pre-shared key token authentication, while the `/generate-token` endpoint generates an authentication token for superusers.

## Endpoints

### 1. Authorize Endpoint

- **URL:** `/authorize`
- **Method:** `POST`
- **Auth required:** Yes (Pre-shared key token authentication)
- **Permissions:** Authenticated User

#### Request
- **Headers:** 
  - `Authorization: Bearer <PRESHARED_KEY_TOKEN>`

#### Response

##### Success Response
- **Condition:** If the user is authenticated successfully.
- **Code:** `200 OK`
- **Content example:**
```json
{
  "detail": "User is authenticated.",
  "user": "<USERNAME>"
}
```

##### Error Response
- **Condition:** If the pre-shared key token is invalid.
- **Code:** `401 Unauthorized`
- **Content:**
```json
{
  "detail": "Invalid token."
}
```

- **Condition:** If the user is inactive or deleted.
- **Code:** `401 Unauthorized`
- **Content:**
```json
{
  "detail": "User inactive or deleted."
}
```

### 2. Generate Token Endpoint

- **Endpoint:** `/generate-token`
- **Supported Method:** `POST`
- **Base URL:** Assumed to be `http://localhost:8000` for local development

#### Authentication

- **Type:** Basic Authentication
- **Credentials Required:** Superuser username and password

#### Headers

- **Content-Type:** `application/json`
- **Authorization:** `Basic <BASE64_ENCODED_CREDENTIALS>`

*Note: The `<BASE64_ENCODED_CREDENTIALS>` will be auto-generated by Postman when you enter the username and password in the Basic Auth fields.*


#### Response

##### Success Response
- **Condition:** If the user is a superuser and the token is successfully generated or retrieved.
- **Code:** `201 Created` (new token generated) or `200 OK` (existing token retrieved)
- **Content example for a new token:**
```json
{
  "token": "<TOKEN_KEY>"
}
```
  
- **Content example for an existing token:**
```json
{
  "token": "<EXISTING_TOKEN_KEY>"
}
```

##### Error Response
- **Condition:** If the user is not a superuser.
- **Code:** `403 Forbidden`
- **Content:**
```json
{
  "detail": "User is not a superuser."
}
```

## Examples

### Authorize Endpoint
Here is an example using `curl` for the `/authorize` endpoint:

```sh
curl -X POST http://localhost:8000/authorize \
     -H "Authorization: Bearer <PRESHARED_KEY_TOKEN>"
```

### Generate Token Endpoint
Here is an example using `curl` for the `/generate-token` endpoint:

```sh
curl -X POST http://localhost:8000/generate-token \
     -H "Authorization: Basic <BASE64_ENCODED_CREDENTIALS>"
```

To encode your username and password in Base64, you can run:

```sh
echo -n 'username:password' | base64
```

**Note:**
Replace `<PRESHARED_KEY_TOKEN>` and `<BASE64_ENCODED_CREDENTIALS>` with the actual pre-shared key token and encoded credentials respectively.

---

**Notes:**
- The `/authorize` endpoint is used to verify that a user's request is authenticated using a custom token authentication scheme based on pre-shared keys.
- The `/generate-token` endpoint is designed for superusers to obtain their authentication token, which can be used for token-based authentication in subsequent requests.
- Ensure that your API consumers are aware that the token should be kept secure and not shared publicly.
- These endpoints are part of an API exercise designed to demonstrate secure API interactions and should be adapted as needed for real-world applications.


# Exercise 3: 

## Overview

This documentation outlines the usage of the Key-Value Store API. The API allows clients to save, retrieve, and delete key-value pairs from a database using RESTful endpoints.

## Endpoints

### Save Key-Value Pair

- **URL**: `/save`
- **Method**: `POST`
- **Description**: Saves a key-value pair to the database. If the key already exists, the value is updated.
- **Request Body**: 
  ```json
  {
    "key": "yourKey",
    "value": "yourValue"
  }
  ```
- **Responses**:
  - **201 Created**: The key-value pair was successfully created or updated.
    ```json
    {
      "key": "yourKey",
      "value": "yourValue"
    }
    ```
  - **400 Bad Request**: Key or value is missing from the request.
    ```json
    {
      "error": "Key and value are required."
    }
    ```

### Retrieve Value by Key

- **URL**: `/get`
- **Method**: `GET`
- **Description**: Retrieves the value for a given key from the database.
- **Query Parameters**:
  - `key`: The key for which the value is to be retrieved.
- **Responses**:
  - **200 OK**: The request was successful, and the value is included in the response.
    ```json
    {
      "key": "yourKey",
      "value": "yourValue"
    }
    ```
  - **400 Bad Request**: The key parameter is missing from the request.
    ```json
    {
      "error": "Key is required."
    }
    ```
  - **404 Not Found**: The specified key does not exist in the database.
    ```json
    {
      "error": "Key not found."
    }
    ```

### Delete Key-Value Pair

- **URL**: `/delete`
- **Method**: `DELETE`
- **Description**: Deletes a key-value pair from the database.
- **Query Parameters**:
  - `key`: The key of the key-value pair to delete.
- **Responses**:
  - **200 OK**: The key-value pair was successfully deleted.
    ```json
    {
      "message": "Key-value pair deleted successfully."
    }
    ```
  - **400 Bad Request**: The key parameter is missing from the request.
    ```json
    {
      "error": "Key is required."
    }
    ```
  - **404 Not Found**: The specified key does not exist in the database.
    ```json
    {
      "error": "Key not found."
    }
    ```

## Error Codes

The following HTTP status codes may be returned, indicating that an error has occurred:
- `400 Bad Request`: The request was invalid or cannot be served. Check the message for more details.
- `404 Not Found`: The requested resource was not found.
- `500 Internal Server Error`: The server encountered an unexpected condition.






# Exercise 4: 

## Overview
The following documentation details the API endpoints designed for storing and retrieving key-value pairs with caching functionality to enhance performance. The `SaveViewCashe` endpoint allows clients to store a key-value pair in the database and cache, and the `GetViewCashe` endpoint attempts to retrieve the value from the cache before falling back to the database if necessary.

## Endpoints

### 1. Save to Cache and Database Endpoint

- **URL:** `/cache/save`
- **Method:** `POST`
- **Auth required:** No *(Authentication may be added as per API security requirements)*
- **Permissions:** None *(Permissions may be set according to the API's privacy policy)*
- **CSRF Token:** Exempt

#### Request
- **Body (JSON):**
  ```json
  {
    "key": "exampleKey",
    "value": "exampleValue"
  }
  ```

#### Response

##### Success Response
- **Condition:** If both key and value are provided and successfully stored.
- **Code:** `201 Created`
- **Content example:**
  ```json
  {
    "success": true,
    "key": "exampleKey",
    "value": "exampleValue"
  }
  ```

##### Error Response
- **Condition:** If either key or value is missing.
- **Code:** `400 Bad Request`
- **Content:**
  ```json
  {
    "error": "Key and value are required."
  }
  ```

### 2. Get from Cache or Database Endpoint

- **URL:** `/cache/get/<str:key>`
- **Method:** `GET`
- **Auth required:** No *(Authentication may be added as per API security requirements)*
- **Permissions:** None *(Permissions may be set according to the API's privacy policy)*
- **CSRF Token:** Exempt

#### Request
- **URL Parameters:**
  - `key`: The key whose value is to be retrieved.

#### Response

##### Success Response
- **Condition:** If the key is found in the cache or database.
- **Code:** `200 OK`
- **Content example:**
  ```json
  {
    "key": "exampleKey",
    "value": "exampleValue"
  }
  ```

##### Error Response
- **Condition:** If the key is not found in both the cache and database.
- **Code:** `404 Not Found`
- **Content:**
  ```json
  {
    "error": "Key not found."
  }
  ```

## Usage Examples

### Save to Cache and Database
Here is an example using `curl` for the `/cache/save` endpoint:

```sh
curl -X POST http://localhost:8000/cache/save \
     -H "Content-Type: application/json" \
     -d '{"key": "exampleKey", "value": "exampleValue"}'
```

### Get from Cache or Database
Here is an example using `curl` for the `/cache/get/exampleKey` endpoint:

```sh
curl -X GET http://localhost:8000/cache/get/exampleKey
```

**Notes:**
- The `/cache/save` endpoint is used to store a new key-value pair or update an existing pair in both the database and the cache.
- The `/cache/get/<str:key>` endpoint is used to retrieve the value of an existing key, preferably from the cache to minimize database lookups and enhance performance. If the value is not found in the cache, it is then retrieved from the database and subsequently stored in the cache for future access.
- CSRF protection is exempt for these endpoints, which might be necessary if the endpoints are consumed by non-browser clients or if cross-origin requests are expected.
- Ensure that appropriate security measures such as authentication and authorization are implemented as per the application's requirements.




# Exercise 5:

## Overview

This documentation covers the test cases implemented for the Key-Value Store API. The API provides endpoints for authorizing users, saving, retrieving, and deleting key-value pairs. The tests are written using `pytest` and Django's testing utilities to ensure the functionality of each endpoint.

## Test Environment Setup

Before running the tests, ensure that the following fixtures are set up to provide a test client and test users:

- `api_client`: Returns an instance of `APIClient` for making requests.
- `user`: Creates a normal user in the database.
- `superuser`: Creates a superuser in the database.
- `get_or_create_token`: Generates or retrieves a token for the superuser.

## Test Cases

### Authorization Tests

- **test_authorize_view_success**: Ensures that a superuser with a valid token can access the authorize endpoint successfully.
- **test_authorize_view_failure**: Checks that the authorize endpoint fails without a valid token, returning `HTTP_401_UNAUTHORIZED`.

### Save View Tests

- **test_save_key_value_pair**: Tests that a key-value pair can be saved successfully and verifies its existence in the database.
- **test_save_without_key_or_value**: Verifies that attempting to save a key-value pair without a key or a value results in `HTTP_400_BAD_REQUEST`.

### Get Value View Tests

- **test_get_existing_key**: Confirms that the get value endpoint correctly retrieves a value for an existing key.
- **test_get_non_existing_key**: Ensures that the get value endpoint returns `HTTP_404_NOT_FOUND` for a key that does not exist in the database.

### End-to-End Tests

- **test_end_to_end_save_and_retrieve**: Executes a save followed by a retrieve operation to ensure end-to-end functionality works as expected.

### Save View Tests (exercise3/ test.py)

- **TestSaveView.test_save_key_value_pair**: Ensures that the save view correctly saves a key-value pair.
- **TestSaveView.test_save_without_key_or_value**: Tests that the save view rejects requests without a key or a value.

### Get View Tests (exercise4/ test.py)

- **TestGetView.test_get_existing_key**: Confirms that the get view returns the correct value for an existing key.
- **TestGetView.test_get_non_existing_key**: Ensures that the get view returns a not found status for a non-existing key.

### End-to-End Tests (exercise4/ test.py)

- **TestKeyValueEndToEnd.test_save_and_retrieve_key_value**: Checks end-to-end functionality of saving and then retrieving a key-value pair.

## Running the Tests

To run the tests, execute the following command in the terminal:

```bash
pytest
```

Replace `path/to/test_file.py` with the actual path to the test files. 

## Note

- The tests assume that the respective URL patterns and views (`'authorize'`, `'save'`, `'get_value'`, etc.) are correctly set up in the Django project.
- Replace placeholder URL names (`'cashesave'`, `'casheget'`) with the actual URL names used in the project.

# NVishTest Django Project Code Structure Documentation

This documentation outlines the code structure and the organization of the NVishTest Django project, which includes various exercises demonstrating different functionalities such as API listening, authentication, database operations, and caching.

## Project Layout

The project is structured into multiple Django apps, each serving different exercises as per the given tasks. The main project directory is `nvishtest`, and it includes the primary URL configurations and settings.

### Main Project: `nvishtest`

- **URLs:** `nvishtest/urls.py`
  - This file includes all the URL route definitions for the exercises.
  - Routes are included from each exercise app to the main URL configuration.

### Exercise 1: Simple API Endpoint

- **Django App Directory:** `exercise1`
- **Purpose:** Responds to unauthenticated `/ping` requests.
- **Views:**
  - `views.py`: Contains the `PingView` class which handles GET requests and returns a "pong" response.
- **URLs:**
  - Included in the main project `urls.py` with the path `ping`.

### Exercise 2: Authentication with Pre-shared Secrets

- **Django App Directory:** `exercise2`
- **Purpose:** Provides authentication using pre-shared secrets and includes `/authorize` and `/generate-token` endpoints.
- **Views:**
  - `views.py`: Contains the `AuthorizeView` and `GenerateTokenView` classes for authorization and token generation.
- **Models:**
  - `models.py`: (If required) to support the views, although actual secrets are typically not stored in models.
- **Authentication:**
  - `authentication.py`: Contains the `PreSharedKeyAuthentication` custom authentication class.
- **URLs:**
  - Included in the main project `urls.py` with paths `authorize` and `generate-token`.
- **Tests:**
  - `tests.py`: Contains test cases to verify the functionality and logic of the authorization process.

### Exercise 3: Database Operations

- **Django App Directory:** `exercise3`
- **Purpose:** Allows posting of key/value pairs to a database and retrieving them.
- **Views:**
  - `views.py`: Contains the `SaveView` and `GetValueView` classes for saving and retrieving key-value pairs.
- **Models:**
  - `models.py`: Defines the `KeyValue` model for storing the key-value pairs.
- **URLs:**
  - Included in the main project `urls.py` with paths `save` and `get`.
- **Tests:**
  - `tests.py`: Contains test cases for database operations.

### Exercise 4: Caching Mechanism

- **Django App Directory:** `exercise4`
- **Purpose:** Implements caching to speed up operations on `/save` and `/get`.
- **Views:**
  - `views.py`: Contains `SaveViewCashe` and `GetViewCashe` classes, which include logic for caching alongside database operations.
- **URLs:**
  - Included in the main project `urls.py` with paths `cache/save` and `cache/get/<str:key>`.
- **Tests:**
  - `tests.py`: Contains test cases to verify caching operations.

### Exercise 5: Test Cases

- **Purpose:** Writing unit and end-to-end test cases using `pytest`.
- **Test Files:**
  - `exercise2/tests.py`
  - `exercise3/tests.py`
  - `exercise4/tests.py`
  - Each of these test files contains relevant test cases for their respective exercises.

## Testing

- Tests are written within each exercise app under the `tests.py` file.
- `pytest` configurations and fixtures are to be defined as needed to support the test cases.
- The test suite covers both unit tests (testing individual components) and end-to-end tests (testing the entire application flow).

## How to Run Tests

Tests can be run using the following command from the root of the project:

```bash
pytest
```

Ensure that `pytest-django` is installed and properly configured in your project.

**Note:** This documentation assumes that the developer is familiar with the Django framework and its conventions for projects, apps, views, models, and tests. Adjustments to file paths and configurations may be necessary depending on the specific implementation details and requirements of the NVishTest project.






