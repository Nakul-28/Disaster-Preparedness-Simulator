# 🚀 Quick Start Guide

## ✅ Environment Setup Complete!

All environment variables have been configured. Here's what's ready:

### Files Created:
- ✅ `backend/.env` - Backend API configuration
- ✅ `frontend/.env` - Frontend application configuration  
- ✅ `ml-engine/.env` - ML Engine configuration
- ✅ `docs/ENVIRONMENT_SETUP.md` - Detailed setup guide
- ✅ `verify_setup.py` - Setup verification script

---

## 📋 Next Steps

### Step 1: Verify Setup
```bash
python verify_setup.py
```

### Step 2: Start MongoDB
```bash
# Option A: Using Docker Compose (Recommended)
docker-compose up mongodb -d

# Option B: Using Docker directly
docker run -d -p 27017:27017 --name mongodb ^
  -e MONGO_INITDB_ROOT_USERNAME=admin ^
  -e MONGO_INITDB_ROOT_PASSWORD=disaster2024 ^
  mongo:6.0
```

### Step 3: Install Dependencies

**Backend:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**ML Engine:**
```bash
cd ml-engine
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Step 4: Train the ML Model
```bash
cd ml-engine
.\venv\Scripts\activate
python train_agent.py --timesteps 100000
```
⏱️ Training will take 15-30 minutes depending on hardware.

### Step 5: Start All Services

**Option A: Using Docker Compose (Recommended)**
```bash
docker-compose up --build
```

**Option B: Start Each Service Individually**

Terminal 1 - Backend:
```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

Terminal 2 - ML Engine:
```bash
cd ml-engine
.\venv\Scripts\activate
uvicorn serve:app --host 0.0.0.0 --port 8001 --reload
```

Terminal 3 - Frontend:
```bash
cd frontend
npm run dev
```

---

## 🌐 Access the Application

Once all services are running:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ML Engine**: http://localhost:8001

---

## 🔍 Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
docker ps | findstr mongodb

# View MongoDB logs
docker logs dps-mongodb
```

### Port Already in Use
```bash
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :8001
netstat -ano | findstr :5173
```

### CORS Errors
- Ensure frontend is running on port 5173 (or update backend `.env` CORS_ORIGINS)
- Restart backend after changing CORS settings

---

## 📚 Additional Resources

- **Environment Setup**: `docs/ENVIRONMENT_SETUP.md`
- **Full README**: `README.md`
- **Docker Compose**: `docker-compose.yml`

---

## 🎯 Test the Application

1. **Create a Scenario**: Go to "Scenario Builder"
2. **Run Simulation**: Execute disaster response simulation
3. **Get AI Help**: Request AI recommendations during simulation
4. **View Analytics**: Check performance metrics and leaderboard

---

**Need help?** Check the documentation in the `docs/` directory!
