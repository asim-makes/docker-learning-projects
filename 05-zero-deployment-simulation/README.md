# Blue-Green Deployment with Docker Compose

This is a simple **blue–green deployment demo** using Docker Compose, Flask, and Nginx.
The idea is to run two versions of the same app (`blue_app` and `green_app`) and let Nginx route traffic between them. This setup helps simulate zero-downtime deployments.

---

## 🚀 What This Project Does

-   Spins up **two Flask app versions**:
    -   `blue_app` → Version 1.0 (Blue)
    -   `green_app` → Version 2.0 (Green)
-   Runs an **Nginx reverse proxy** that:
    -   Load-balances (or traffic-splits) requests
    -   Routes traffic based on the client IP using `split_clients`
-   All containers run inside a shared Docker network.
-   Ideal for learning **zero-downtime deployments** and **release
    switching strategies**.

## 📂 Project Structure

    05-zero-deployment-simulation/
    │
    ├── compose.yml
    │
    ├── app/
    │   ├── Dockerfile.app
    │   ├── requirements.txt
    │   └── app.py
    │
    └── nginx/
        ├── Dockerfile.nginx
        └── nginx.conf

## 🐳 Running the Project

1.  Make sure Docker & Docker Compose are installed.
2.  Navigate into the project folder.
3.  Run:

```
    docker compose up --build -d
```

4.  Open your browser: http://localhost:8000

Nginx will route you **either to blue or green**, depending on your IP(or based on the split rules).

## 🧪 Testing the Apps

### Hit the main endpoint

    curl http://localhost:8000

You'll get JSON showing version, color, and environment.

### Check health:

    curl http://localhost:8000/health

## ⚙️ How Traffic Splitting Works

Inside `nginx.conf`, `split_clients` decides which upstream handles
traffic.

## 📦 Containers Explained

### blue_app

-   Version 1.0
-   Color blue

### green_app

-   Version 2.0
-   Color green

### nginx

-   Reverse proxy
-   Exposes port 8000

## 🔧 Useful Commands

Stop:

    docker compose down

Rebuild:

    docker compose build blue_app green_app

Logs:

    docker compose logs -f
