# Multi-Container Flask Application (Flask + PostgreSQL + Redis + Nginx)

This is a small Docker Compose project built to practice running a multi-container application.
It includes:

- **Flask** web app
- **PostgreSQL** database
- **Redis** cache
- **Nginx** reverse proxy

The app exposes a simple page that checks connectivity to Redis and Postgres, updates counters, and shows the results in the browser.

---

## 📦 Services Overview

### **web (Flask)**
- Main application container.
- Connects to Redis and Postgres using environment variables.
- Redis: increments a cached hit counter.
- Postgres: updates a persistent counter stored in a `hits` table.

### **postgres**
- Stores persistent data for the hit counter.
- Runs initialization SQL from `postgres_db/init.sql`.
- Uses a Docker volume to persist data.

### **redis**
- Acts as a cache layer.
- Stores a key named `web_hits`.
- Password-protected.

### **nginx**
- Reverse proxy running on port **80**.
- Forwards traffic to the Flask app running at **web:8000**.

---

## 🚀 Running the Project

```bash
docker compose up --build
