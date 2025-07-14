# Production Traveler Slip System

A system for tracking production lots through various manufacturing processes with defect logging and oven control capabilities.

## Features

- Lot traveler creation and tracking
- Process workflow management
- Defect logging and reporting
- Oven loading/unloading control
- Employee authentication and authorization
- Real-time dashboard

## Technologies

- Backend: Python, Flask, SQLAlchemy, PostgreSQL
- Frontend: React, Redux, Tailwind CSS
- Deployment: Docker, Docker Compose

## Setup

1. Clone the repository
2. Create `.env` file based on `.env.example`
3. Run database migrations:
   ```bash
   docker-compose run backend python scripts/init_db.py