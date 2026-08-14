# Project step to Create
- Install: pip install virtualenv
- Create: python -m venv env
- Go TO env : env\Scripts\activate
- Install to run server: pip install uvicorn
- install fast api : pip install fastapi uvicorn
- to check the package list: pip freeze

# Packages list to install
- pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic pydantic-settings python-dotenv python-jose[cryptography] passlib[bcrypt] python-multipart httpx redis loguru pytest pytest-asyncio

# Package list with Version
pip freeze > requirements.txt

# Folder and file Creates
- .env
- core
    - config.py
    - logger.py :
        - pip install loguru
        - use for request log, error log and file logging
        - ceate app/logs/ to save all logs files

# Data Base
- install packages: pip install sqlalchemy asyncpg alembic
- app/
    - └── db/
        - ├── base.py
        - ├── database.py
        - ├── models/
        - └── migrations/
    - create base file
    - crete model

- psql --version
- DATABASE_URL=postgresql+asyncpg://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/workflow_db
- pip install sqlalchemy asyncpg alembic
- app/models/user.py
- app/models/project.py
- check all version:
    - pip show sqlalchemy
    - pip show asyncpg
    - pip show alembic
- pip install "psycopg[binary]"
- pip install sqlalchemy asyncpg alembic
- for now use : https://console.neon.tech/app/org-still-grass-48589901/projects
- Databse: workflow-management
-           FastAPI
                ↓
        SQLAlchemy Async
                ↓
            asyncpg
                ↓
        ☁️ Neon PostgreSQL

- run : alembic init app/db/migrations
- alembic.ini

- first migration of User and Project: alembic revision --autogenerate -m "create users and projects tables"
- after migration done: alembic upgrade head

- app/core/dependency.py

# Authentication
- Password hashing
    - pip install "pwdlib[argon2]"
    - app/core/security.py
- schema/auth.py
- repository/auth.py
- service/auth.py
- routes/auth.py

- JWT package install : pip install PyJWTc
- app/core/security.py
- app/core/dependency: get_current_user
- app/service: refresh_token: process
- RBAC: add new field in user model for role
- alembic revision --autogenerate -m "add role column to user table"
- alembic upgrade head :  this commond will run after every migration run
- work on role checking : app/core/dependency: require_role
- create model for porject : app/schema/project.py







Phase 1

✅ Project setup
✅ Virtual environment
✅ Folder structure
✅ Configuration
✅ Logging
✅ Environment variables

Phase 2

✅ PostgreSQL
✅ SQLAlchemy
✅ Alembic
✅ Database connection

    Step 1: 
        Database Setup
        PostgreSQL install (agar already nahi hai)
        workflow_db database create karna
    Step 2: 
        SQLAlchemy Configuration
        db/database.py
        Async Engine
        Session
        Base Model
    Step 3: 
        First Model
        User model
        Relationships ka introduction
    Step 4: 
        Alembic
        Migration setup
        First migration
        Create tables

    ├── db/
    │   ├── database.py
    │   ├── base.py
    │   ├── session.py
    │   ├── models/
    │   │     └── user.py
    │   └── migrations/
    │
    ├── schemas/
    ├── repository/
    ├── services/
    │
    └── main.py

Phase 3

✅ Authentication
✅ JWT
✅ Refresh token
✅ RBAC

Phase 4

✅ User Module
✅ Department Module
✅ Project Module

Phase 5

✅ Task Module
✅ Approval Module
✅ File Upload

Phase 6

✅ Redis
✅ Cache
✅ Rate Limiting

Phase 7

✅ Reports
✅ Dashboard
✅ Background Jobs

Phase 8

✅ Testing
✅ Docker
✅ Deployment