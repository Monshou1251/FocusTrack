# FocusTrack: Personal Productivity Tracker

FocusTrack is a personal productivity app that helps users manage their time effectively using the Pomodoro technique. It provides in-depth focus session tracking with a GitHub-like calendar view. In future versions, it will include a secure online chat, possibly utilizing Web3 technology.

## Features
- **Focus Session Tracking**: Start, pause, and track Pomodoro-like sessions.
- **GitHub-like Calendar**: Visualize your focus sessions in an interactive heatmap.
- **Detailed Statistics**: Analyze your productivity with session logs and insights.
- **Secure Authentication**: Login and register with JWT authentication.
- **Future Feature**: Secure online chat (possibly with Web3 integration).

## Tech Stack
- **Backend**: FastAPI (Python), PostgreSQL, SQLAlchemy ORM, Alembic (migrations)
- **Frontend**: Vue 3 (Vite), Pinia (state management), Axios
- **Authentication**: JWT-based authentication
- **Task Queue**: RabbitMQ + Celery for background task processing
- **Caching**: Redis (session storage and quick data access)
- **Deployment**: Docker, Nginx, CI/CD pipeline

## Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL
- Redis
- RabbitMQ
- Docker

### Backend Setup
```bash
git clone https://github.com/yourusername/focustrack.git
cd focustrack/backend

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend

npm install

npm run dev
```

## Usage
- Start and track focus sessions.
- View your productivity heatmap.
- Analyze detailed statistics of past sessions.

## API Documentation
API documentation is available at [`http://localhost:8000/docs`](http://localhost:8000/docs) (Swagger UI).

## Deployment
To deploy using Docker:
```bash
docker-compose up --build -d
```

## Contribution
Feel free to submit issues and pull requests to improve the project!

## License
This project is licensed under the **MIT License**.

---

### Contact
For any inquiries or if you want to give me money, reach out to `grigory.urchenko@gmail.com`.
