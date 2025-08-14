# Quiz App (Django + React)

A full-stack web application where users can register, verify email, log in, and take & create quizzes.

---

##  Technologies
- **Backend:** Django, Django REST Framework, SimpleJWT
- **Frontend:** React (with Axios for API calls)
- **Authentication:** JWT (Access & Refresh Tokens)

---

## 📂 Project Structure

---

## 🔑 Authentication & User APIs (`/users/`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users/signup/` | `POST` | Register a new user |
| `/users/verify-email/` | `POST` | Verify email with code |
| `/users/resend-vcode/` | `POST` | Resend verification code |
| `/users/login/` | `POST` | Obtain JWT access & refresh tokens |
| `/users/token/refresh/` | `POST` | Refresh JWT access token |
| `/users/logout/` | `POST` | Logout user (blacklist token) |
| `/users/me/update/` | `PUT` | Update own profile |
| `/users/dashboard/` | `GET` | Get logged-in user profile |
| `/users/<username>/` | `GET` | Public profile of a user |

---

## 📝 Quiz APIs (`/quiz/`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/quiz/quizzes/` | `GET` | List all quizzes |
| `/quiz/create-quizz/` | `POST` | Create a new quiz (with questions & answers) |
| `/quiz/<id>/` | `GET` | Get quiz detail (with questions & answers) |
| `/quiz/<id>/submit/` | `POST` | Submit answers for a quiz and get result |

---

## ⚙️ Setup Instructions
### Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # on Linux/Mac
venv\Scripts\activate     # on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
### Open another terminal for frontend
```
cd frontend
npm install
npm start
```
### Or if You have Docker installed 
```
docker-compose up --build
docker-compose down
docker-compose down -v
```

Abdulaziz Toshpulatov – Full Stack Developer )
