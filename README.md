# E-Learning Platform (LearnFlow)

A full-stack e-learning web application inspired by modern online learning platforms.  
The project provides course discovery, enrollment, learning progress tracking, and an instructor studio for course management.

This repository is hosted and maintained by the project lead and serves as the final consolidated version of the group work.

---

## 🚀 Features

### 👨‍🎓 Student Features
- Browse course catalog with search and category filters
- View course details and syllabus
- Enroll in courses
- Learn through a course player with lessons and videos
- Mark lessons as complete
- Track learning progress in a personalized dashboard
- Account settings and password recovery

### 👩‍🏫 Instructor Features
- Instructor dashboard (Studio)
- Create new courses
- Edit existing courses
- Add, update, and delete lessons
- Organize lessons by sections

### 🔐 Authentication & Security
- User registration and login
- JWT-based authentication
- Protected routes for students and instructors
- Password reset and recovery flow

---

## 🧱 Tech Stack

### Frontend
- React (Vite)
- React Router (SPA navigation)
- Zustand (state management)
- TailwindCSS (styling)
- Axios / Fetch (API communication)

### Backend
- FastAPI (REST API)
- SQLite (local development database)
- SQLAlchemy ORM
- JWT authentication (python-jose)
- Password hashing (passlib / bcrypt)

---

## 📁 Project Structure

E-Learning-Platform/
├── client/ # React frontend
│ └── src/
│ ├── api/
│ ├── components/
│ ├── layouts/
│ ├── pages/
│ ├── store/
│ └── mocks/
├── server/ # FastAPI backend
│ └── app/
│ ├── api/
│ ├── core/
│ ├── db/
│ ├── models/
│ ├── schemas/
│ └── main.py
└── README.md

yaml
Copy code

---

## ⚙️ Environment Setup

### Backend (.env example)
Create `server/.env`:
```env
SECRET_KEY=dev-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
Frontend (.env example)
Create client/.env:

env
Copy code
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_USE_MOCK_API=true
VITE_USE_MOCK_API=true allows the frontend to run using mock data if the backend is unavailable.

▶️ Running the Project
Backend
bash
Copy code
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Backend available at:

http://127.0.0.1:8000

http://127.0.0.1:8000/docs (Swagger API docs)

Frontend
bash
Copy code
cd client
npm install
npm run dev -- --host 0.0.0.0 --port 5173
Frontend available at:

http://localhost:5173

🧪 Demo Credentials (Mock or Seed Data)
Student
makefile
Copy code
Email: student@example.com
Password: Password123!
Instructor
makefile
Copy code
Email: instructor@example.com
Password: Password123!
📊 API Overview (Backend)
POST /auth/register

POST /auth/login

POST /auth/request-password-reset

POST /auth/reset-password

GET /users/me

PUT /users/me

GET /courses

GET /courses/{id}

POST /courses

PUT /courses/{id}

DELETE /courses/{id}

GET /courses/{id}/lessons

POST /courses/{id}/lessons

PATCH /enrollments/{id}/progress

GET /dashboard

⚠️ Development Note (Project Challenge)
During the final stages of development, one of the group members experienced a laptop failure, which prevented them from successfully pushing and merging their latest changes to the shared repository. This also affected their local development environment, where the application could no longer run correctly.

As the GitHub repository host and project maintainer, I consolidated, reviewed, and validated the available contributions to ensure the project meets all functional and technical requirements. The core application is complete, functional, and represents the intended final outcome of the group effort.

✅ Project Status
✔ Core functionality completed

✔ Frontend and backend implemented

✔ Authentication and authorization working

✔ Mock data available for frontend testing

✔ Ready for demonstration and evaluation

👤 Maintainer
Project Host & Maintainer:
Derrick Wilson
