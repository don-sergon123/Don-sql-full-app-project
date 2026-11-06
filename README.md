# Don-SQL-Final-Project
# Task Manager RESTful API

A robust Flask-based RESTful API that provides secure, user-specific task management features with session-based authentication, password hashing, and resource pagination.

---

## 🛠️ Tech Stack

* **Backend Framework:** Flask
* **Database & ORM:** SQLite, Flask-SQLAlchemy
* **Authentication:** Flask-Bcrypt, Flask-Session
* **Database Migrations:** Flask-Migrate (Alembic)
* **Python Version:** Python 3.12+

---

## 🚀 Features

* **User Authentication:** Password hashing using Bcrypt, user registration (`/signup`), login (`/login`), logout (`/logout`), and session verification (`/check-session`).
* **Task CRUD Operations:** Authenticated users can create, read, update, and delete their own tasks.
* **Pagination:** Resource list endpoints (`GET /tasks`) support page and per-page parameters for optimized data delivery.
* **Database Version Control:** Migration scripts managed via Alembic for seamless schema updates.

---

## 📁 Project Structure

```text
final_project/
├── instance/          # SQLite database storage (app.db)
├── migrations/        # Alembic migration scripts
├── .gitignore         # Version control exclusion rules
├── app.py             # Main application entry point & API routes
├── models.py          # SQLAlchemy models (User, Task)
├── requirements.txt   # Project dependencies
├── seed.py            # Database seeding script
