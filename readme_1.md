# Disaster Preparedness Simulator

An advanced disaster response training platform that combines reinforcement learning with interactive simulation to help emergency planners practice and optimize their disaster response strategies.

## 🎯 Overview

This system allows users to:
- Design custom disaster scenarios (earthquakes, floods, cyclones)
- Make real-time resource allocation decisions
- Compare their strategies against AI-trained agents
- Learn from AI recommendations and improve response effectiveness

## 🏗️ Architecture

```
disaster-preparedness-simulator/
├── backend/          # FastAPI backend services
├── frontend/         # React + TypeScript UI
├── ml-engine/        # RL agent training & inference
└── docs/             # Documentation
```

## 🚀 Technology Stack

- **Backend**: FastAPI (Python)
- **RL Framework**: Stable-Baselines3 + Custom OpenAI Gym Environment
- **Frontend**: React + TypeScript + Leaflet.js
- **Database**: MongoDB
- **Deployment**: Docker + Docker Compose

## 📦 Prerequisites

- Python 3.9+
- Node.js 18+
- MongoDB 6.0+
- Docker & Docker Compose

## 🛠️ Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### ML Engine Setup
```bash
cd ml-engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train_agent.py
```

## 📚 Documentation

See the [docs](./docs) directory for detailed documentation on:
- System architecture
- API specifications
- RL environment design
- Deployment guides

## 🎮 Features

- **Interactive Simulation**: Real-time disaster response decisions
- **AI Assistance**: Get recommendations from trained RL agents
- **Performance Analytics**: Compare your strategy with AI
- **Scenario Builder**: Create custom disaster scenarios
- **Leaderboards**: Compete with other users

## 📈 Project Status

Currently in active development. See [task.md](../brain/a10f8e80-a783-4cb3-b276-767dbf554ba1/task.md) for progress tracking.

## 📄 License

MIT License - see LICENSE file for details
