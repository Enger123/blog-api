# BLOG API

REST API for a blog application with FastAPI.

## Features:

- User registration and authentication
- JWT authentication
- Posts CRUD
- Comments
- Likes
- Tags
- Statistics
- Redis caching
- PostgreSQL database
- Alembic migrations

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pytest
- Docker
- Docker Compose
- Redis

## Architecture

The project uses a layered architecture:

Routes -> Services -> Repositories -> PostgreSQL

Redis is used as a cache layer for frequently requested data.

You can use docker compose up --build to run a project with Docker.
The project will be launched on localhost:8080