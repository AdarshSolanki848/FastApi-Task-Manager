# FastAPI Task Manager

A simple full-stack Task Manager application built with FastAPI, MySQL, HTML, CSS, and JavaScript.

## Features

- Add new tasks
- Delete tasks
- Mark tasks as completed
- Persistent storage using MySQL
- Responsive user interface
- RESTful API

## Tech Stack

### Backend
- FastAPI
- Python
- MySQL
- Jinja2 Templates

### Frontend
- HTML
- CSS
- JavaScript

## Project Structure

```
TaskManager/
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── main.py
├── requirements.txt
└── README.md
```

## Installation

### Clone the repository

```bash
git clone https://github.com/AdarshSolanki848/FastApi-Task-Manager.git
```

### Move into the project

```bash
cd FastApi-Task-Manager
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Configure MySQL

Create a database

```sql
CREATE DATABASE TaskManager;
```

Create the tasks table

```sql
CREATE TABLE tasks(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    completed BOOLEAN DEFAULT FALSE
);
```

Update the database credentials in `main.py`.

## Run the project

```bash
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | Get all tasks |
| POST | /tasks | Add a new task |
| PUT | /tasks/{id} | Update task status |
| DELETE | /tasks/{id} | Delete task |

## Future Improvements

- User Authentication
- Due Dates
- Task Categories
- Search and Filter
- SQLAlchemy ORM
- Docker Support
- Deployment

## Author

Adarsh Solanki