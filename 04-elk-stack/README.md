# ELK Stack + Flask App Logging Pipeline (Docker Compose)

This project sets up a full **ELK stack (Elasticsearch, Logstash, Kibana)** integrated with a **Flask application** and **Filebeat** for log shipping — all orchestrated with Docker Compose.

It’s a compact, hands-on setup to understand how logs flow from a running app → Filebeat → Logstash → Elasticsearch → Kibana.

---

## 🧱 What This Stack Includes

### **1. Elasticsearch**
- Stores logs sent from Logstash
- Single-node mode
- No security (for local development)
- Java memory reduced for lightweight usage

### **2. Logstash**
- Receives logs from Filebeat
- Parses logs using a custom `grok` filter
- Drops invalid/unparsable logs
- Sends structured logs to Elasticsearch

### **3. Kibana**
- Web UI to visualize logs stored in Elasticsearch
- Accessible on **localhost:5601**

### **4. Flask App**
- A simple Python application running via Gunicorn
- Logs are captured by Filebeat and shipped into the pipeline

### **5. Filebeat**
- Reads Docker container logs
- Ships them to Logstash
- Uses `filebeat.yml` for configuration

---

## 📂 Project Structure

    04-elk-stack/
    │
    ├── docker-compose.yml
    ├── Dockerfile.flask
    ├── Dockerfile.logstash
    ├── logstash.conf
    ├── filebeat.yml
    ├── README.md
    ├── requirements.txt
    ├── board/

---

## 🚀 Running the Stack

1. Make sure Docker & Docker Compose are installed.
2. Start everything:
```
    docker compose up --build
```
3. Access the services:
- **Kibana** → http://localhost:5601
- **Flask App** → http://localhost:8000
- **Elasticsearch API** → http://localhost:9200

---
