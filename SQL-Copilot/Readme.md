# SQL-Copilot
---

# How to Run the Application

## Installation

1. **Create a Python virtual environment** and install the required packages listed in the `requirements.txt` file:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

---

## Backend Setup

1. **Set up environment variables**:

    - In the `.env` file, replace `your_google_gemini_api_key` with your actual Google Gemini API key.

2. **Start the backend server**:

    - Navigate to the `backend` folder:

        ```bash
        cd backend
        ```

    - Run the following command to start the backend server with `uvicorn`:

        ```bash
        uvicorn backend_7:app --reload
        ```

    This will run the `backend.py` script.

---

## Frontend Setup

1. **Install frontend dependencies**:

    - Navigate to the `frontend` folder:

        ```bash
        cd frontend
        ```

    - Run the following command to install the required dependencies:

        ```bash
        npm install  # or npm i
        ```

2. **Start the frontend server**:

    - Run the following command to start the development server:

        ```bash
        npm run dev
        ```

3. **Access the application**:
    - Open your browser and go to `http://localhost:3000` to access the application.

