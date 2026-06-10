# Retail Analytics Platform

A Flask-based microservice for real-time store aisle foot-traffic monitoring, suspicious activity detection, and automated reporting.

## Features

- 📹 **Live Video Analysis** — Upload two video feeds and monitor frame by frame in real time
- 🚨 **Suspicious Activity Detection** — Flags shoppers dwelling beyond threshold time
- 🤖 **YOLO AI Detection** — Detects persons and shopping carts using YOLOv8
- 📊 **Congestion Monitoring** — RED/YELLOW/GREEN aisle status dashboard
- 📈 **Peak Hour Analytics** — Pandas-powered traffic analysis
- 📝 **AI Executive Reports** — Auto-generated business reports via Groq AI
- 🐳 **Docker Ready** — Fully containerized for any platform

## Setup (Local)

```bash
git clone https://github.com/mallikkarishma/retail-analytics
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## Setup (Docker)

```bash
docker build -t retail-analytics .
docker run -p 5000:5000 --env-file .env retail-analytics
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/upload | Upload store image |
| POST | /api/analyze | Analyze two video feeds |
| POST | /api/detect-video | YOLO detection on video |
| GET | /api/detect/result/:id | Get YOLO result |
| GET | /api/congestion | Get aisle congestion status |
| GET | /api/analytics/peak-hours | Get peak traffic hours |
| GET | /api/reports/executive | Generate AI report |
| GET | /api/reports/list | List all reports |

## Environment Variables

| Variable | Description |
|----------|-------------|
| GROQ_API_KEY | Groq API key for AI reports |
| FLASK_DEBUG | Enable debug mode |
| SECRET_KEY | Flask secret key |

## Tech Stack

- **Backend** — Flask, Python
- **Computer Vision** — OpenCV, YOLOv8
- **Database** — SQLite
- **Analytics** — Pandas
- **AI Reports** — Groq (Llama 3)
- **Frontend** — Vanilla JS, HTML, CSS
- **DevOps** — Docker
