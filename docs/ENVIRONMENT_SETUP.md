# Environment Setup Guide

## 🔧 Environment Variables Configuration

This project uses environment variables to configure the three main services:
- **Backend** (FastAPI)
- **Frontend** (React + Vite)
- **ML Engine** (RL Training & Inference)

## ✅ Already Configured

Environment files have been created for you:
- `backend/.env` - Backend API configuration
- `frontend/.env` - Frontend application configuration
- `ml-engine/.env` - ML Engine training & serving configuration

## 📝 Configuration Details

### Backend Configuration (`backend/.env`)

```env
MONGODB_URL=mongodb://admin:disaster2024@localhost:27017
MONGODB_DB_NAME=disaster_prep
ML_ENGINE_URL=http://localhost:8001
ENVIRONMENT=development
DEBUG=true
PORT=8000
```

**Key Variables:**
- `MONGODB_URL`: Connection string for MongoDB database
- `ML_ENGINE_URL`: URL where the ML Engine API is running
- `CORS_ORIGINS`: Allowed frontend origins (includes Vite's default port 5173)

### Frontend Configuration (`frontend/.env`)

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

**Key Variables:**
- `VITE_API_URL`: Backend API base URL
- `VITE_WS_URL`: WebSocket URL for real-time updates

> **Note:** Vite requires all environment variables to be prefixed with `VITE_`

### ML Engine Configuration (`ml-engine/.env`)

```env
MODEL_PATH=./models/disaster_agent_final.zip
TOTAL_TIMESTEPS=500000
N_ENVS=4
PORT=8001
```

**Key Variables:**
- `MODEL_PATH`: Path to save/load trained models
- `TOTAL_TIMESTEPS`: Number of training steps
- `N_ENVS`: Number of parallel environments for training

## 🔄 Customization

### For Production Deployment

1. **Update MongoDB credentials:**
   ```env
   MONGODB_URL=mongodb://your_user:your_password@your_host:27017
   ```

2. **Update frontend URL:**
   ```env
   VITE_API_URL=https://your-domain.com
   ```

3. **Enable production mode:**
   ```env
   ENVIRONMENT=production
   DEBUG=false
   ```

### For Different Ports

If you need to use different ports:

```env
# Backend
PORT=8080

# Frontend (edit vite.config.ts to change dev server port)

# ML Engine
PORT=8002
```

Remember to update the corresponding URLs in other services!

## 🐳 Docker Compose

When using Docker Compose, environment variables are already configured in `docker-compose.yml`. The services will automatically discover each other using Docker networking:

- MongoDB: `mongodb://admin:disaster2024@mongodb:27017` (internal)
- Backend: `http://backend:8000` (internal)
- ML Engine: `http://ml-engine:8001` (internal)

## ⚠️ Security Notes

1. **Don't commit `.env` files** - They're already in `.gitignore`
2. **Change default passwords** before deploying to production
3. **Use strong credentials** for MongoDB
4. **Enable HTTPS** in production

## ✨ Next Steps

Now that environment variables are set up, you can:

1. **Start MongoDB:**
   ```bash
   # Option 1: Using Docker
   docker run -d -p 27017:27017 --name mongodb \
     -e MONGO_INITDB_ROOT_USERNAME=admin \
     -e MONGO_INITDB_ROOT_PASSWORD=disaster2024 \
     mongo:6.0

   # Option 2: Using Docker Compose (recommended)
   docker-compose up mongodb -d
   ```

2. **Install dependencies and start services** (see main README.md)

3. **Train the ML model** (see ML Engine documentation)

## 🆘 Troubleshooting

### Connection Refused Errors

- Ensure MongoDB is running: `docker ps` or check Windows Services
- Verify ports are not in use: `netstat -ano | findstr :8000`

### Environment Variables Not Loading

- Restart the development server after changing `.env` files
- For Vite, variables must start with `VITE_`
- Check for typos in variable names

### CORS Errors

- Ensure frontend URL is in `CORS_ORIGINS` in backend `.env`
- Default includes ports 3000, 5173, and 3001
