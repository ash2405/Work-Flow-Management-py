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
