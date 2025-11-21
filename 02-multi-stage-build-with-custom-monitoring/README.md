# Optimized Flask Microservice with Prometheus & Grafana

This is a small monitoring-focused project that runs a Flask
microservice, exposes Prometheus metrics, and visualizes them using
Grafana. Everything is wired together with Docker Compose and built
using a multi-stage Dockerfile for a lightweight final image.

## Features

-   **Flask API** with two endpoints:
    -   `/` → returns a simple message
    -   `/metrics` → exposes Prometheus metrics
-   **Custom Prometheus Counter** tracking request counts by method and
    endpoint
-   **Multi-stage Docker build** for clean and optimized images
-   **Prometheus** configured to scrape the API
-   **Grafana** pre-provisioned with a Prometheus data source

## Project Structure

    .
    ├── app.py
    ├── Dockerfile
    ├── compose.yml
    ├── Docker/
    │   ├── prometheus.yml
    │   └── grafana.yml
    └── requirements.txt

## How to Run

Make sure Docker and Docker Compose are installed, then run:

``` bash
docker compose up --build
```

## Service Endpoints

  Service      URL                             Description
  ------------ ------------------------------- --------------------
  Flask API    http://localhost:8000           Main app endpoint
  Metrics      http://localhost:8000/metrics   Prometheus metrics
  Prometheus   http://localhost:9090           Prometheus UI
  Grafana      http://localhost:3000           Dashboards

**Grafana Login**\
- Username: `admin`\
- Password: `P@ssw0rd`

## Prometheus Scraping

Prometheus scrapes your app using the config in `Docker/prometheus.yml`:

``` yaml
scrape_configs:
  - job_name: myapp
    static_configs:
      - targets: ["api:8000"]
```

## Multi-Stage Docker Build

-   **Stage 1:** Install dependencies\
-   **Stage 2:** Run minimal Python Alpine image as a non-root user\
-   Reduces image size and improves security\
-   Final container only contains dependencies + `app.py`

## Health Check

The API includes a healthcheck in `compose.yml`:

``` yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
```

(You can add a `/health` endpoint if needed.)

## Summary

This project is a simple but practical example of:

-   Microservice development\
-   Container optimization\
-   Observability using Prometheus\
-   Dashboarding with Grafana\
-   End-to-end Docker Compose workflow

It's a great foundation for experimenting, learning, or scaling up into
something bigger.
