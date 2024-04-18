```markdown
# FastAPI CRUD Application with Authentication

This is a simple CRUD (Create, Read, Update, Delete) application built using FastAPI, a modern web framework for building APIs with Python. It includes endpoints that require user authentication.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shrikant3004/DBMS.git
   ```
2. Navigate to the project directory:
   ```bash
   cd DBMS
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the FastAPI server:
   ```bash
    uvicorn app.main:app --host 0.0.0.0 --reload
   ```
   This will start the FastAPI server on `http://localhost:8000` by default.

2. Open your web browser and go to `http://localhost:8000/docs` to access the Swagger UI for testing the API endpoints.

3. You can also use tools like [Postman](https://www.postman.com/) or [curl](https://curl.se/) for testing the API endpoints.
