# Shopify FastAPI Integration

A robust FastAPI application that integrates with Shopify to manage customers and orders, and fetch products. This service provides a RESTful API for creating, retrieving, updating, and deleting customers and orders, as well as fetching products directly from Shopify. Additionally, it includes comprehensive unit and integration tests to ensure reliability and maintainability.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Configure Environment Variables](#4-configure-environment-variables)
  - [5. Initialize the Database](#5-initialize-the-database)
- [Running the Project](#running-the-project)
  - [Start the FastAPI Server](#start-the-fastapi-server)
  - [Access API Documentation](#access-api-documentation)
- [Running Tests](#running-tests)
  - [Execute All Tests with Coverage](#execute-all-tests-with-coverage)
  - [Run Specific Test Files](#run-specific-test-files)
  - [View Coverage Reports](#view-coverage-reports)
- [Assumptions and Design Decisions](#assumptions-and-design-decisions)
  - [Architecture](#architecture)
  - [Database Choice](#database-choice)
  - [Dependency Injection](#dependency-injection)
  - [Testing Strategy](#testing-strategy)
  - [Pydantic Models](#pydantic-models)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Customer Management:** Create, retrieve, update, and delete customers.
- **Order Management:** Create, retrieve, update, and delete orders.
- **Shopify Integration:** Fetch products directly from Shopify.
- **Authentication:** OAuth flow with Shopify for secure API interactions.
- **Testing:** Comprehensive unit and integration tests with coverage reports.
- **API Documentation:** Interactive Swagger UI for exploring and testing endpoints.

## Prerequisites

- **Python 3.10+**
- **PostgreSQL 12+** (Alternatively, SQLite is used for testing)
- **Git**

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/shopify-fastapi-integration.git
cd shopify-fastapi-integration
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Ensure `pip` is up to date, then install the required packages.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory based on the provided `.env.example`.

```bash
cp .env.example .env
```

Open the `.env` file and configure the following variables:

```dotenv
# Database Configuration
POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=shopify_db
DB_HOST=localhost
DB_PORT=5432

# Shopify Configuration
SHOPIFY_API_KEY=your_shopify_api_key
SHOPIFY_API_SECRET=your_shopify_api_secret
SHOPIFY_SCOPES=read_products,write_products,read_orders
SHOPIFY_REDIRECT_URI=https://yourdomain.com/auth/callback

# Other Configurations
SECRET_KEY=your_secret_key
```

**Note:** Replace placeholders like `your_postgres_username` and `your_shopify_api_key` with your actual credentials.

### 5. Initialize the Database

Apply the database migrations to set up the required tables.

```bash
# Ensure the PostgreSQL server is running and accessible

# Create the database if it doesn't exist
psql -U your_postgres_username -c "CREATE DATABASE shopify_db;"

# Run migrations (if using Alembic)
alembic upgrade head
```

_If you haven't set up Alembic for migrations yet, refer to the [Database Migrations](#database-migrations) section._

## Running the Project

### Start the FastAPI Server

Activate your virtual environment if not already active, then run:

```bash
uvicorn main:app --reload
```

**Parameters:**

- `main:app`: Refers to the `app` instance in `main.py`.
- `--reload`: Enables auto-reloading on code changes (useful for development).

**Expected Output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using StatReload
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Access API Documentation

Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the interactive Swagger UI. Here, you can explore and test all available API endpoints.

## Running Tests

Comprehensive testing ensures the reliability and robustness of your application. This project includes both unit and integration tests.

### Execute All Tests with Coverage

Run all tests and generate a coverage report:

```bash
pytest --cov=.
```

**Explanation:**

- `pytest`: Executes the test suite.
- `--cov=.`: Measures code coverage for the entire project.

**Sample Output:**

```
============================= test session starts ==============================
platform win32 -- Python 3.10.14, pytest-8.3.4, pluggy-1.5.0
rootdir: C:\Users\Joshua_zza\Desktop\shopify\shopify-fastapi-integration
plugins: anyio-4.7.0, asyncio-0.25.0, cov-6.0.0, mock-3.14.0, requests-mock-1.12.1
collected 10 items

tests/test_customers.py FF.                                                                                                                    [ 30%]
tests/test_integration.py FF                                                                                                                   [ 50%]
tests/test_orders.py .....                                                                                                                     [100%]

===================================================================== FAILURES =====================================================================
...
============================================================== short test summary info ==============================================================
FAILED tests/test_customers.py::test_get_customers - AssertionError: assert [] == [{'first_name...me': 'Smith'}]
FAILED tests/test_customers.py::test_get_customer - assert 404 == 200
FAILED tests/test_integration.py::test_shopify_oauth_callback - AssertionError: assert None == {'detail': 'OAuth callback processed successfully'}
FAILED tests/test_integration.py::test_shopify_api_fetch_products - assert 404 == 200
======================================================== 4 failed, 6 passed, 13 warnings in 0.78s ============================================================
```

### Run Specific Test Files

To run tests from a specific file, use:

```bash
pytest tests/test_customers.py
pytest tests/test_orders.py
pytest tests/test_integration.py
```

### View Coverage Reports

Generate an HTML coverage report for a detailed view:

```bash
pytest --cov=. --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the coverage report.

## Assumptions and Design Decisions

### Architecture

- **FastAPI Framework:** Chosen for its high performance, ease of use, and automatic documentation generation.
- **Modular Design:** The application is divided into routers (`customers`, `orders`, `shopify`), models, schemas, and database configurations to promote maintainability and scalability.

### Database Choice

- **PostgreSQL:** Selected for its robustness, scalability, and compatibility with SQLAlchemy.
- **SQLAlchemy ORM:** Utilized for database interactions, providing an abstraction layer over SQL queries.

### Dependency Injection

- **FastAPI's Dependency Injection:** Used to manage database sessions (`get_db`), ensuring efficient resource management and testability.

### Testing Strategy

- **Unit Tests:** Focus on individual components and routes, ensuring they behave as expected in isolation.
- **Integration Tests:** Test the interaction between different parts of the application and external services like Shopify by mocking API responses.
- **Test Database:** An in-memory SQLite database is used during testing to ensure tests do not interfere with production data.

### Pydantic Models

- **Schemas Separation:** Pydantic models are organized in a separate `schemas.py` file to avoid circular imports and promote reusability.
- **`orm_mode`:** Enabled in Pydantic models to allow seamless interaction with SQLAlchemy ORM objects.

### Handling Circular Imports

- **Refactored Imports:** Moved Pydantic schemas to `schemas.py` and adjusted route imports to prevent circular dependencies between `main.py` and route modules.

### Addressing Deprecation Warnings

- **Pydantic Updates:** The codebase uses `model_dump()` instead of the deprecated `dict()` method and considers migrating from class-based `Config` to `ConfigDict` in Pydantic V2 to future-proof the application.

## Project Structure

```
shopify-fastapi-integration/
├── main.py
├── schemas.py
├── routes/
│   ├── __init__.py
│   ├── customers.py
│   ├── orders.py
│   └── shopify.py
├── models.py
├── database.py
├── requirements.txt
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_customers.py
│   ├── test_orders.py
│   └── test_integration.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── .env.example
├── README.md
└── ...
```

## Troubleshooting

- **Circular Import Errors:**
  - Ensure that Pydantic schemas are imported from `schemas.py` and not from `main.py` or route modules.
- **Database Connection Issues:**
  - Verify that PostgreSQL is running and accessible with the provided credentials.
  - Ensure that the `.env` file has the correct database configurations.
- **Pydantic Deprecation Warnings:**

  - Update Pydantic models to use `model_dump()` instead of `dict()`.
  - Consider migrating from class-based `Config` to `ConfigDict` as per Pydantic V2 guidelines.

- **Test Failures:**
  - Ensure that the test database is correctly set up and that fixtures are properly configured.
  - Verify that mocks in integration tests are correctly patching the intended targets.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a New Branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m "Add feature X"
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/YourFeatureName
   ```
5. **Open a Pull Request**

## License

This project is licensed under the [MIT License](LICENSE).

```

```
````
