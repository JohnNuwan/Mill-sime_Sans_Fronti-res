### **Development Environment Setup - Millésime Sans Frontières Backend**

**Version:** 1.0
**Date:** 08/27/2025

**1. Purpose**

This document provides step-by-step instructions for setting up the local development environment for the Millésime Sans Frontières backend. It covers installing prerequisites, configuring the database, and launching the FastAPI application.

**2. Prerequisites**

Before you begin, ensure you have the following tools installed on your machine:

*   **Python 3.9+:** Download from [python.org](https://www.python.org/downloads/).
*   **pip:** Usually included with Python.
*   **Docker Desktop:** For managing the PostgreSQL database and other services (e.g., Redis for Celery).
    *   Download from [docker.com](https://www.docker.com/products/docker-desktop).
*   **Git:** For cloning the project repository.
    *   Download from [git-scm.com](https://git-scm.com/downloads).
*   **A code editor:** Visual Studio Code (VS Code) is recommended.
    *   Download from [code.visualstudio.com](https://code.visualstudio.com/).

**3. Project Setup**

1.  **Clone the Git repository:**
    Open your terminal or command prompt and run:
    ```bash
    git clone [GIT_REPOSITORY_URL]
    cd millesime-sans-frontieres-backend # or the project folder name
    ```

2.  **Create and activate a virtual environment:**
    It is highly recommended to use a virtual environment to isolate project dependencies.
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    Once the virtual environment is activated, install all required libraries:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: The `requirements.txt` file will be created during the initial project development.)*

**4. Database Configuration (PostgreSQL with Docker)**

1.  **Start Docker Desktop:** Ensure Docker Desktop is running on your machine.

2.  **Start the PostgreSQL database:**
    The project will include a `docker-compose.yml` file to facilitate starting the necessary services (database, Redis).
    ```bash
    docker-compose up -d postgres redis # or simply 'docker-compose up -d' if other services are defined
    ```
    *(Note: The exact services will depend on the final `docker-compose.yml`.)*

3.  **Run database migrations:**
    Once the database is started, apply the migrations to create the database schema.
    ```bash
    alembic upgrade head
    ```
    *(Note: `alembic` will be installed via `requirements.txt`.)*

**5. Launching the Backend Application**

1.  **Set environment variables:**
    Create a `.env` file at the project root and define the necessary environment variables (e.g., `DATABASE_URL`, `SECRET_KEY`). An `.env.example` file will be provided as a guide.
    ```ini
    # Example content for .env
    DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
    SECRET_KEY="your_very_long_and_complex_jwt_secret_key"
    # ... other variables
    ```

2.  **Start the FastAPI application:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    *(Note: The `app.main:app` path may vary depending on the final project structure.)*

    The API will be accessible at `http://localhost:8000`.

3.  **Access the API documentation:**
    *   **Swagger UI:** `http://localhost:8000/docs`
    *   **ReDoc:** `http://localhost:8000/redoc`

**6. Running Tests**

*   To run unit and integration tests:
    ```bash
    pytest
    ```

**7. Common Development Commands**

*   **Linter (e.g., Ruff):**
    ```bash
    ruff check .
    ```
*   **Code formatter (e.g., Black):**
    ```bash
    black .
    ```
*   **Stop Docker services:**
    ```bash
    docker-compose down
    ```