# E-Learning Platform Deployment Guide

## Quick Deploy Options

### Option 1: Render (Recommended - Free Tier Available)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to https://render.com and sign up
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file
   - Click "Apply" to deploy both frontend and backend

3. **Access your app**
   - Backend API: `https://learnflow-api.onrender.com`
   - Frontend: `https://learnflow-web.onrender.com`

### Option 2: Railway (Alternative)

1. **Push code to GitHub** (same as above)

2. **Deploy on Railway**
   - Go to https://railway.app and sign up
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect and deploy

### Option 3: Local Network Access

If you just want others on your local network to access:

1. **Find your local IP address**
   ```bash
   # On Linux/Mac
   ifconfig | grep "inet "
   # On Windows
   ipconfig
   ```

2. **Update CORS in server/app/main.py**
   Add your IP to allowed origins:
   ```python
   allow_origins=[
       "http://YOUR_IP:5174",
       "http://localhost:5174",
   ]
   ```

3. **Start both servers**
   ```bash
   # Terminal 1 - Backend
   cd server
   python3 start_server.py

   # Terminal 2 - Frontend
   cd client
   npm run dev -- --host 0.0.0.0
   ```

4. **Share the URL**
   Others can access at: `http://YOUR_IP:5174`

## Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///./learnflow.db
JWT_SECRET=your-secret-key-here
FRONTEND_ORIGIN=http://localhost:5174
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000
```

## Test Accounts

After deployment, you can use these accounts:
- **Instructor**: sarah@example.com / password (any 6+ chars when registering)
- **Student**: student@example.com / password (any 6+ chars when registering)

## Features

✅ 8 courses across multiple categories
✅ 36 detailed lessons
✅ Role-based access (Instructor/Student)
✅ Course creation and management
✅ Student enrollment system
✅ Course player with lesson navigation

## Support

For issues or questions, check the logs in your deployment platform.
