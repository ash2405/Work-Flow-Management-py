# FastAPI + PostgreSQL + SQLAlchemy + Alembic + Authentication — Complete Setup Notes

> **Language:** Hindi + English mix  
> **Goal:** `.env` se start karke PostgreSQL, SQLAlchemy, Alembic migrations, Auth, Password Hashing, JWT, Refresh Token aur RBAC tak complete foundation.

---

# 0. Final Architecture

Hum project ko roughly is structure mein organize karenge:

```text
app/
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── dependency.py
│   └── security.py
│
├── db/
│   ├── __init__.py
│   ├── base.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── project.py
│   │
│   └── migrations/
│       ├── env.py
│       ├── script.py.mako
│       ├── README
│       └── versions/
│
├── features/
│   ├── __init__.py
│   │
│   └── auth/
│       ├── __init__.py
│       ├── repository.py
│       ├── service.py
│       ├── routes.py
│       └── schemas.py
│
├── main.py
│
├── .env
├── .env.example
├── .gitignore
└── alembic.ini
```

### Architecture ka simple idea

```text
UI / Client
    ↓
Routes
    ↓
Service
    ↓
Repository
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

Authentication:

```text
Login
  ↓
Password Verify
  ↓
Access Token + Refresh Token
```

Protected API:

```text
JWT
 ↓
get_current_user()
 ↓
User
```

Authorization:

```text
User
 ↓
Role
 ↓
RBAC
 ↓
Allow / 403 Forbidden
```

---

# 1. Python Virtual Environment Create Karo

Project folder ke andar:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### Why?

Virtual environment project ke packages ko isolated rakhta hai.

```text
Project A → apne packages
Project B → apne packages
```

Ek project ka package version dusre project ko disturb nahi karega.

---

# 2. Required Packages Install Karo

Humare setup ke liye main packages:

```bash
pip install fastapi uvicorn
```

Database / ORM:

```bash
pip install sqlalchemy asyncpg
```

Migration:

```bash
pip install alembic
```

Environment variables:

```bash
pip install pydantic-settings
```

Password hashing:

```bash
pip install "pwdlib[argon2]"
```

JWT:

```bash
pip install PyJWT
```

Email validation ke liye:

```bash
pip install email-validator
```

### Ek saath install karna ho:

```bash
pip install fastapi uvicorn sqlalchemy asyncpg alembic pydantic-settings "pwdlib[argon2]" PyJWT email-validator
```

---

# 3. Package Ka Kaam Kya Hai?

| Package | Purpose |
|---|---|
| `fastapi` | API framework |
| `uvicorn` | FastAPI application server |
| `sqlalchemy` | ORM + database abstraction |
| `asyncpg` | Async PostgreSQL driver |
| `alembic` | Database migrations |
| `pydantic-settings` | `.env` / configuration management |
| `pwdlib[argon2]` | Password hashing |
| `PyJWT` | JWT create/decode |
| `email-validator` | `EmailStr` validation |

### Important

Agar tum `postgresql+asyncpg://...` use kar rahe ho, to SQLAlchemy async PostgreSQL communication ke liye `asyncpg` use karega.

---

# 4. `.gitignore` Create Karo

Project root mein `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc

.env

.pytest_cache/
.mypy_cache/

.idea/
.vscode/
```

### Why?

`.env` mein secrets hote hain, jaise:

```text
DATABASE_URL
JWT_SECRET_KEY
```

Isliye `.env` ko GitHub par push nahi karna chahiye.

---

# 5. `.env` File Create Karo

Project root:

```text
.env
```

Example:

```env
DEBUG=True

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/my_database

JWT_SECRET_KEY=change-this-to-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### `.env` ka purpose

Sensitive/configurable values ko code ke andar hard-code nahi karna.

Instead:

```text
.env
 ↓
config.py
 ↓
Application
```

---

# 6. `.env.example` Banao

Actual secrets ke bina:

```env
DEBUG=True

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/my_database

JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Ye file Git mein commit ki ja sakti hai.

---

# 7. `core/config.py`

Create:

```text
app/core/config.py
```

Code:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
```

### Easy language

Ye file `.env` se values read karti hai.

Example:

```text
.env
  ↓
DATABASE_URL
  ↓
settings.DATABASE_URL
```

---

# 8. PostgreSQL Database Create Karo

PostgreSQL mein database create karo.

Example:

```sql
CREATE DATABASE my_database;
```

Tum pgAdmin ya `psql` se bhi create kar sakte ho.

Connection URL:

```text
postgresql+asyncpg://postgres:password@localhost:5432/my_database
```

Breakdown:

```text
postgresql  → database type
asyncpg     → async driver
postgres    → username
password    → password
localhost   → host
5432        → PostgreSQL port
my_database → database name
```

---

# 9. SQLAlchemy Database Setup

Create:

```text
app/db/database.py
```

Code:

```python
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

---

# 10. `create_async_engine()`

```python
engine = create_async_engine(...)
```

Engine ko simple language mein database communication manager samajh sakte ho.

Flow:

```text
FastAPI
   ↓
SQLAlchemy
   ↓
Engine
   ↓
asyncpg
   ↓
PostgreSQL
```

---

# 11. `AsyncSessionLocal`

```python
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

Ye **database session factory** hai.

Jab actual session chahiye:

```python
AsyncSessionLocal()
```

---

# 12. `expire_on_commit=False`

```python
expire_on_commit=False
```

Commit ke baad SQLAlchemy object ke already-loaded attributes ko expire na karne ke liye useful hai.

Async application mein commonly convenient setting hai.

---

# 13. SQLAlchemy Base Create Karo

Create:

```text
app/db/base.py
```

Code:

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

Ab saare SQLAlchemy models:

```python
class User(Base):
    ...
```

ke through `Base.metadata` ka part banenge.

---

# 14. Models Folder

Create:

```text
app/db/models/
```

Aur:

```text
app/db/models/__init__.py
```

---

# 15. User Model

Example:

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="user",
        nullable=False,
    )
```

### Important

Database mein password plain text nahi jayega.

Instead:

```text
password
   ↓
hash
   ↓
password_hash
```

---

# 16. Project Model

Example:

```python
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
```

`owner_id` ka purpose:

```text
Project
   ↓
owner_id
   ↓
User
```

Yani project kis user ka hai, ye database mein store hoga.

---

# 17. `models/__init__.py`

Models ko package ke through import karna useful hai:

```python
from app.db.models.user import User
from app.db.models.project import Project
```

### Why?

Alembic ko models metadata mein register karne ke liye imports ensure karne padte hain.

Har model ko `env.py` mein manually import karna preferred approach nahi hai.

Better:

```text
models/__init__.py
        ↓
all model imports
        ↓
Base.metadata
        ↓
Alembic
```

---

# 18. Alembic Initialize Karo

Command:

```bash
alembic init app/db/migrations
```

Structure:

```text
app/db/migrations/
├── versions/
├── env.py
├── script.py.mako
└── README
```

Aur root mein:

```text
alembic.ini
```

---

# 19. `alembic.ini`

Alembic ka configuration file hai.

Database URL ko `.env` mein rakhna better hai, isliye `alembic.ini` mein real password hard-code karne ki zarurat nahi.

---

# 20. Alembic `env.py`

`app/db/migrations/env.py` mein SQLAlchemy metadata configure karna important hai.

Simplified setup:

```python
from app.db.base import Base
from app.db.models import User, Project

target_metadata = Base.metadata
```

Full Alembic-generated `env.py` mein ye `target_metadata` appropriate location par set karna hota hai.

### Important

Agar models import nahi hue, Alembic ko unke tables ka metadata nahi milega.

---

# 21. Migration Generate Karo

Models ready hone ke baad:

```bash
alembic revision --autogenerate -m "create user and project tables"
```

Alembic migration file generate karega:

```text
app/db/migrations/versions/
    <revision>_create_user_and_project_tables.py
```

---

# 22. Migration Apply Karo

```bash
alembic upgrade head
```

Ab PostgreSQL mein actual tables create/update honge.

---

# 23. Migration ka Simple Concept

```text
SQLAlchemy Model
       ↓
Alembic autogenerate
       ↓
Migration File
       ↓
alembic upgrade head
       ↓
PostgreSQL Schema
```

Migration file ko blindly copy-paste/change karne ki jagah pehle generated diff review karna good practice hai.

---

# 24. Database Dependency

Create/update:

```text
app/core/dependency.py
```

Code:

```python
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

---

# 25. `get_db()` Exactly Kya Karta Hai?

Request:

```text
API Request
    ↓
get_db()
    ↓
Create AsyncSession
    ↓
yield session
    ↓
Endpoint uses DB
    ↓
Context closes session
```

Endpoint:

```python
db: AsyncSession = Depends(get_db)
```

FastAPI automatically dependency execute karega.

---

# 26. Password Hashing Package

Install:

```bash
pip install "pwdlib[argon2]"
```

`security.py`:

```text
app/core/security.py
```

Code:

```python
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )
```

### Signup

```text
password
   ↓
hash_password()
   ↓
password_hash
   ↓
database
```

### Login

```text
password
   ↓
verify_password()
   ↓
True / False
```

---

# 27. Auth Feature Structure

Create:

```text
app/features/auth/
```

Files:

```text
auth/
├── __init__.py
├── repository.py
├── service.py
├── routes.py
└── schemas.py
```

Responsibilities:

| File | Work |
|---|---|
| `schemas.py` | Request/response validation |
| `repository.py` | DB queries |
| `service.py` | Business/auth logic |
| `routes.py` | API endpoints |

---

# 28. Auth Schemas

`app/features/auth/schemas.py`:

```python
from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

---

# 29. Repository Layer

`app/features/auth/repository.py`

Example:

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:

    result = await db.execute(
        select(User).where(User.email == email)
    )

    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    user: User,
) -> User:

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user
```

Repository ka simple rule:

> Database se data read/write karna.

---

# 30. Service Layer

Service business logic handle karega.

Signup flow:

```text
Request
  ↓
Check existing user
  ↓
Hash password
  ↓
Create User object
  ↓
Repository
  ↓
Database
```

Example:

```python
from fastapi import HTTPException

from app.core.security import hash_password
from app.db.models.user import User
from app.features.auth import repository


async def signup(
    db,
    data,
):
    existing_user = await repository.get_user_by_email(
        db,
        data.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    hashed_password = hash_password(
        data.password
    )

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hashed_password,
    )

    return await repository.create_user(
        db,
        user,
    )
```

---

# 31. JWT Setup

Install:

```bash
pip install PyJWT
```

`app/core/security.py`:

```python
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


def create_access_token(user_id: int) -> str:
    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
```

---

# 32. JWT Payload

Example:

```text
{
    "sub": "1",
    "exp": "...",
    "type": "access"
}
```

Meaning:

```text
sub  → user ID
exp  → expiry
type → access token
```

---

# 33. Login Service

Basic login:

```python
from fastapi import HTTPException

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.features.auth import repository


async def login(
    db,
    data,
):
    user = await repository.get_user_by_email(
        db,
        data.email,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user.id
    )

    refresh_token = create_refresh_token(
        user.id
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
```

---

# 34. Refresh Token

`security.py`:

```python
def create_refresh_token(user_id: int) -> str:
    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh",
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
```

Access token:

```text
15 minutes
```

Refresh token:

```text
7 days
```

Actual expiry values tum apni requirement ke according change kar sakte ho.

---

# 35. Decode Access Token

```python
from fastapi import HTTPException, status


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

        return payload

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
```

---

# 36. Decode Refresh Token

```python
def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token",
            )

        return payload

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token",
        )
```

### Why `type` check?

Access token ko refresh token ki jagah use nahi karna chahiye.

```text
access token
type = access

refresh token
type = refresh
```

---

# 37. OAuth2PasswordBearer

`dependency.py`:

```python
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
```

Iska important kaam:

Request header:

```text
Authorization: Bearer <JWT>
```

se JWT token extract karna.

---

# 38. `get_current_user()`

`dependency.py`:

```python
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.core.security import decode_access_token


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:

    payload = decode_access_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    result = await db.execute(
        select(User).where(
            User.id == int(user_id)
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
```

---

# 39. Nested Dependency Chain

Ye concept very important hai.

Endpoint:

```python
current_user: User = Depends(
    require_role("admin")
)
```

`require_role()` ke andar:

```python
current_user: User = Depends(
    get_current_user
)
```

`get_current_user()` ke andar:

```python
token: str = Depends(
    oauth2_scheme
)
```

So complete chain:

```text
Endpoint
   ↓
require_role()
   ↓
get_current_user()
   ↓
oauth2_scheme
   ↓
Authorization Header
   ↓
JWT
```

FastAPI automatically ye dependencies resolve karta hai.

---

# 40. Protected `/auth/me`

`routes.py`:

```python
@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
    }
```

Request:

```text
GET /auth/me
```

Valid JWT:

```text
200 OK
```

Missing/invalid JWT:

```text
401 Unauthorized
```

---

# 41. Refresh Endpoint

`service.py`:

```python
from app.core.security import (
    create_access_token,
    decode_refresh_token,
)


async def refresh_access_token(
    refresh_token: str,
) -> str:

    payload = decode_refresh_token(
        refresh_token
    )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    return create_access_token(
        user_id=int(user_id)
    )
```

`routes.py`:

```python
@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
)
async def refresh_token(
    data: RefreshTokenRequest,
):
    access_token = await refresh_access_token(
        data.refresh_token
    )

    return AccessTokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
```

Flow:

```text
Access Token expires
       ↓
POST /auth/refresh
       ↓
Refresh Token
       ↓
Verify
       ↓
New Access Token
```

---

# 42. RBAC

RBAC = Role Based Access Control.

User model mein:

```python
role: Mapped[str] = mapped_column(
    String(50),
    default="user",
    nullable=False,
)
```

Example roles:

```text
admin
manager
user
```

---

# 43. Role Migration

Agar `role` field model mein baad mein add kiya hai:

```bash
alembic revision --autogenerate -m "add role to users"
```

Then:

```bash
alembic upgrade head
```

---

# 44. `require_role()`

`dependency.py`:

```python
def require_role(required_role: str):
    async def role_checker(
        current_user: User = Depends(
            get_current_user
        ),
    ) -> User:

        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource",
            )

        return current_user

    return role_checker
```

Usage:

```python
current_user: User = Depends(
    require_role("admin")
)
```

---

# 45. Multiple Roles

Production mein often ek endpoint ko multiple roles access karte hain.

```python
def require_roles(*required_roles: str):
    async def role_checker(
        current_user: User = Depends(
            get_current_user
        ),
    ) -> User:

        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource",
            )

        return current_user

    return role_checker
```

Usage:

```python
current_user: User = Depends(
    require_roles("admin", "manager")
)
```

Result:

```text
admin    → allowed
manager  → allowed
user     → 403
```

---

# 46. Test RBAC Endpoint

Temporary testing endpoint:

```python
@router.get("/admin-only")
async def admin_only(
    current_user: User = Depends(
        require_role("admin")
    ),
):
    return {
        "message": "Welcome Admin",
        "user_id": current_user.id,
    }
```

Ye mainly RBAC test karne ke liye hai.

Real project mein RBAC ko actual business endpoints ke saath use karna better hai.

---

# 47. Real Project Endpoint Example

Suppose actual project endpoint:

```python
@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(
        require_role("admin")
    ),
):
    ...
```

UI:

```text
DELETE /projects/10
```

Backend:

```text
JWT
 ↓
get_current_user()
 ↓
require_role("admin")
 ↓
Role check
 ↓
delete project
```

UI `require_role()` ko directly call nahi karti.

---

# 48. Authentication vs Authorization

### Authentication

Question:

> Who are you?

```text
JWT
 ↓
get_current_user()
 ↓
User
```

### Authorization

Question:

> What are you allowed to do?

```text
User
 ↓
Role
 ↓
RBAC
 ↓
Allow / Deny
```

---

# 49. Frontend/UI Role

Frontend se actual API call hoti hai.

Example:

```javascript
fetch(
  "http://localhost:8000/projects/10",
  {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  }
);
```

Frontend button hide/show kar sakta hai, but backend security mandatory hai.

> UI decides what to show.  
> Backend decides what is actually allowed.

---

# 50. FastAPI Main App

`app/main.py`:

```python
from fastapi import FastAPI

from app.features.auth.routes import router as auth_router


app = FastAPI(
    title="My API",
)


app.include_router(auth_router)


@app.get("/")
async def root():
    return {
        "message": "API is running"
    }
```

Run:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

Swagger UI se APIs test kar sakte ho.

---

# 51. Complete Authentication Flow

## Signup

```text
POST /auth/signup
       ↓
Schema validation
       ↓
Service
       ↓
Hash password
       ↓
Repository
       ↓
PostgreSQL
```

## Login

```text
POST /auth/login
       ↓
Find user
       ↓
Verify password
       ↓
Access Token
       ↓
Refresh Token
```

## Protected API

```text
Request
       ↓
Bearer Access Token
       ↓
oauth2_scheme
       ↓
get_current_user()
       ↓
User
       ↓
Endpoint
```

## Authorization

```text
User
 ↓
require_role()
 ↓
Role check
 ↓
Allowed / 403
```

## Refresh

```text
Access Token expired
       ↓
POST /auth/refresh
       ↓
Refresh Token
       ↓
Verify
       ↓
New Access Token
```

---

# 52. What We Have Completed

Foundation/configuration:

- [x] Virtual environment
- [x] Required packages
- [x] `.env`
- [x] `.env.example`
- [x] `.gitignore`
- [x] `config.py`
- [x] PostgreSQL connection
- [x] SQLAlchemy async engine
- [x] Async session
- [x] Base model
- [x] User model
- [x] Project model
- [x] Alembic
- [x] Migration environment
- [x] Initial migrations
- [x] Database dependency
- [x] Password hashing
- [x] Auth feature structure
- [x] Signup
- [x] Login
- [x] JWT access token
- [x] Refresh token
- [x] Current user dependency
- [x] Protected endpoint
- [x] RBAC
- [x] Multiple-role dependency

---

# 53. What We Have NOT Started Yet

Ab actual business/project work start karna hai.

Next feature:

```text
Project CRUD
```

Recommended endpoints:

```text
POST   /projects
GET    /projects
GET    /projects/{project_id}
PUT    /projects/{project_id}
DELETE /projects/{project_id}
```

Project feature structure:

```text
app/features/project/
├── __init__.py
├── repository.py
├── service.py
├── routes.py
└── schemas.py
```

---

# 54. Project Create Flow

Sabse pehle:

```text
POST /projects
```

Request:

```json
{
  "name": "My First Project",
  "description": "Project description"
}
```

Flow:

```text
UI
 ↓
POST /projects
 ↓
JWT
 ↓
get_current_user()
 ↓
current_user.id
 ↓
Project.owner_id
 ↓
Service
 ↓
Repository
 ↓
PostgreSQL
```

Important:

Frontend se `owner_id` lene ki zarurat nahi.

Backend JWT se logged-in user identify karega.

---

# 55. Important Rules to Remember

### Rule 1

`database.py`:

```text
engine
AsyncSessionLocal
```

### Rule 2

`dependency.py`:

```text
get_db
get_current_user
require_role
require_roles
```

### Rule 3

`repository.py`:

```text
Database queries
```

### Rule 4

`service.py`:

```text
Business logic
```

### Rule 5

`routes.py`:

```text
API endpoints
```

### Rule 6

`schemas.py`:

```text
Request/response validation
```

### Rule 7

Passwords:

```text
Never store plain password.
```

### Rule 8

JWT secret:

```text
Never hard-code production secret.
```

### Rule 9

UI security:

```text
Never rely only on frontend role checks.
```

### Rule 10

Migration:

```text
Model change
 ↓
Alembic migration
 ↓
alembic upgrade head
```

---

# 56. Useful Commands — Quick Reference

Create virtual environment:

```bash
python -m venv .venv
```

Activate Windows:

```bash
.venv\Scripts\activate
```

Install packages:

```bash
pip install fastapi uvicorn sqlalchemy asyncpg alembic pydantic-settings "pwdlib[argon2]" PyJWT email-validator
```

Initialize Alembic:

```bash
alembic init app/db/migrations
```

Create migration:

```bash
alembic revision --autogenerate -m "message"
```

Apply migration:

```bash
alembic upgrade head
```

Run server:

```bash
uvicorn app.main:app --reload
```

---

# 57. Final Mental Model

Pure project ko simple words mein yaad rakho:

```text
                  CLIENT / UI
                       │
                       ↓
                    FastAPI
                       │
                       ↓
                    ROUTES
                       │
                       ↓
                   SERVICES
                       │
                       ↓
                  REPOSITORY
                       │
                       ↓
                   SQLAlchemy
                       │
                       ↓
                  PostgreSQL
```

Authentication:

```text
Signup
 ↓
Hash Password
 ↓
DB

Login
 ↓
Verify Password
 ↓
Access + Refresh Token
```

Protected request:

```text
Bearer Token
 ↓
oauth2_scheme
 ↓
get_current_user()
 ↓
User
```

Authorization:

```text
User
 ↓
Role
 ↓
require_role()
 ↓
Endpoint
```

Migration:

```text
SQLAlchemy Model
 ↓
Alembic
 ↓
Migration File
 ↓
PostgreSQL
```

## Current Status

**Foundation / configuration complete.**

Next actual application development:

```text
PROJECT CRUD
```

Start with:

```text
POST /projects
```

and implement:

```text
schemas
 → repository
 → service
 → routes
 → authentication
 → database
```
