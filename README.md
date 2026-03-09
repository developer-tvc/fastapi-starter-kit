# FastAPI Skeleton
A production-ready backend foundation built with FastAPI, implementing Clean Architecture, modular design, and Docker-based development environments.

Technology Stack:
-Python 3.12
-FastApi
-PostgreSQL
-Docker

## Overview
    This repository provides a structured backend architecture with:

        -Clean Architecture principles

        -Modular feature-based structure

        -Separation of domain, infrastructure, and API layers

        -Production-ready Docker setup

        -Database migrations

        -Testable use cases

        -Repository pattern implementation

    The goal is to provide a scalable and maintainable backend foundation that can be reused across multiple services.

### Architecture
    This project follows Clean Architecture principles.

    Layers are separated to ensure:

        -Business logic is independent of frameworks

        -Infrastructure can be replaced without affecting domain logic

        -High testability

        -Clear separation of concerns

    Architecture layers:

        API Layer (FastAPI routes)
                ↓
        Application Layer (Use Cases)
                ↓
        Domain Layer (Entities + Repository Interfaces)
                ↓
        Infrastructure Layer (Database / ORM Implementation)

### Project Structure

    ├── alembic.ini
    ├── app
    │   ├── core
    │   │   ├── config.py                                       # Application configuration
    │   │   ├── database.py                                     # Database connection setup
    │   │   ├── dependencies.py                                 # Shared FastAPI dependencies
    │   │   └── security.py                                     # Authentication & security utilities
    │   ├── db
    │   │   └── base.py                                         # Base SQLAlchemy models import
    │   ├── main.py                                             #FastAPI entry point
    │   └── modules
    │       └── users                                           #user module
    │           ├── api
    │           │   ├── routes.py                               # User API endpoints
    │           │   └── schemas.py                              # Pydantic request/response schemas
    │           ├── domain                                      #Business Logic
    │           │   ├── entities.py                   
    │           │   └── repositories.py
    │           ├── infrastructure
    │           │   ├── models.py                               #Database models
    │           │   └── sqlalchemy_repository.py                #Database operations
    │           └── use_cases
    │               ├── create_users.py                         # Create user use case
    │               └── list_users.py                           # List users use case
    ├── docker-compose.local.yml                                # Local development services
    ├── docker-compose.yml                                      # Main docker compose configuration
    ├── Dockerfile                                              # Docker image definition
    ├── migrations                                              # Alembic migrations
    │   ├── env.py
    │   ├── README
    │   ├── script.py.mako
    │   └── versions
    │       └── 90bd21ec797f_user.py
    ├── poetry.lock                                             # Poetry dependency lock
    ├── pyproject.toml                                          # Project dependencies & config
    ├── README.md                                               # Project documentation
    ├── requirements.txt                                        # Alternative pip dependencies
    ├── start.sh                                                #Container startup script
    └── tests                                                   # Unit tests
        └── users
            ├── fake_repository.py
            ├── test_create_user.py
            └── test_list_users.py


### Layer Responsibilities

-API Layer

    Handles HTTP requests and responses.

        -FastAPI routers

        -Request validation

        -Response serialization

-Use Cases

    Contains application business logic.

    Examples:

        -Create user

        -List users

        -Update user

    Use cases depend only on domain interfaces, not infrastructure.


-Domain Layer

    Defines core business models.

        -Entities

        -Repository interfaces

    This layer must not depend on any framework.


-Infrastructure Layer

    Implements external systems such as:

        -SQLAlchemy models

        -Repository implementations

    Database operations

###  Installation Guide

    Explain how to run the project locally.

        1.Clone the repository:
        
            git clone https://github.com/company-name/project-name.git
            cd project-name
        2.Create a virtual environment:
        
            python -m venv venv
            source venv/bin/activate
        3.Install dependencies:
        
            pip install -r requirements.txt
        4.Run application:
        
            uvicorn app.main:app --reload

    Application will be available at:

        http://localhost:8000

    Swagger documentation:

        http://localhost:8000/docs

    Running with Docker:
    
        docker-compose up --build

    in local environment run:

        docker-compose -f docker-compose.yml -f docker-compose.local.yml up --build

### Environment Configuration
    Configuration is managed in:

        app/core/config.py

    Environment variables should be defined using .env.
    Copy .env.example to .env and fill in the values.
    

### Database Migrations
    Migrations are managed using Alembic.
    migrations are stored in the migrations directory.
    
        migrations/
    
    create new migration:
    
        alembic revision --autogenerate -m "message"
    
    apply migrations:
    
        alembic upgrade head
    
### Testing
    Tests are stored in the tests directory.
    
        tests/
    run tests:
    
        pytest
    Test use FakeRepository to isolate business logic tests from database.

    Example:
    
        pytest tests/users/FakeRepository.py


### Why This Architecture?

    Benefits:

        Scalable for large applications

        Clear code boundaries

        High testability

        Framework independence for business logic

        Easy onboarding for teams
