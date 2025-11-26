# 🔗 URL Shortener Microservice (Flask/Docker)

This project implements a simple, robust URL shortener microservice using the **Flask** web framework, **SQLAlchemy** for database interactions, and is containerized using **Docker** and managed with **Docker Compose**. It also includes a robust **CI/CD pipeline** using **GitHub Actions** to automate testing, building, and pushing the Docker image to Docker Hub.

## 🚀 Features

* **URL Shortening:** Generate a short, unique ID for any long URL.
* **Custom IDs:** Users can specify a custom short ID instead of a random one.
* **Redirection:** Short URLs redirect to the original long URL (HTTP 302).
* **Database:** Uses SQLite (development/local) or PostgreSQL (production) for persistence.
* **Containerized:** Fully containerized with Docker for easy deployment.
* **Testing:** Comprehensive unit and integration tests using `pytest`.
* **CI/CD:** Automated workflow for testing, building, and deployment via GitHub Actions.

## 🛠️ Local Development Setup

The easiest way to run the application locally is by using Docker Compose.

### Prerequisites

* Docker
* Docker Compose

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd url-shortener-repo
    ```

2.  **Create a `.env` file:**
    The application requires environment variables defined in a `.env` file for configuration, specifically the **`SECRET_KEY`** for Flask sessions and the database connection details.

    Create a file named `.env` in the root directory:
    ```env
    # .env
    SECRET_KEY=a-strong-random-secret-key-for-flask
    # Note: DATABASE_URL is typically overridden in compose.yml for local use.
    # The compose.yml specifies sqlite:///data/shorty.db for local volume mounting.
    ```

3.  **Create the local data directory:**
    The `compose.yml` mounts a local `./data` directory to persist the SQLite database.
    ```bash
    mkdir data
    ```

4.  **Build and Run the application:**
    Use Docker Compose to build the image and start the service.

    ```bash
    docker compose up --build
    ```
    The application will be accessible at `http://localhost:5000`.

## ⚙️ Docker and Docker Compose

### `Dockerfile`

* Based on `python:3.11-slim` for a small image size.
* Sets the working directory to `/url_shortener_app`.
* Installs dependencies from `requirements.txt`.
* Exposes port `5000`.
* Runs the Flask application using `flask run` on host `0.0.0.0`.

### `compose.yml`

| Key | Description |
| :--- | :--- |
| `build: .` | Builds the Docker image from the local `Dockerfile`. |
| `ports: "5000:5000"` | Maps the container's port 5000 to the host's port 5000. |
| `volumes: ./data:/url_shortener_app/data` | Persists the SQLite database file (`shorty.db`) from the container's data directory to the local `./data` directory. |
| `environment: ...` | Overrides the `FLASK_APP` and explicitly sets the `DATABASE_URL` to the local SQLite file. |
| `env_file: .env` | Loads additional environment variables (like `SECRET_KEY`) from the local `.env` file. |

## ✅ Testing

The project includes unit and integration tests written with **`pytest`** to ensure core functionality (short ID generation, URL creation, custom IDs, error handling, and redirection) is correct.

### Test Configuration (`config.py` & `test_app.py`)

* **`TestingConfig`**: Defines a configuration that sets `TESTING = True` and uses an **in-memory SQLite database** (`sqlite:///:memory:`). This ensures tests are fast, isolated, and leave no permanent traces on the filesystem.
* **`test_client` fixture**: This pytest fixture manages the testing lifecycle:
    1.  Configures the Flask app with `TestingConfig`.
    2.  Creates all database tables (`db.create_all()`) within the application context.
    3.  Yields the `app.test_client()` for tests to interact with.
    4.  Tears down the environment by dropping all tables (`db.drop_all()`).

### Running Tests Locally

To run the tests before CI/CD, you can use the following command (assuming dependencies are installed):

```bash
# From the directory containing test_app.py and core/
pytest
