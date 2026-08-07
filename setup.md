# Project set up steps
- install virtual env package if not have : pip install virtulenv
- create venv :
        - python -m venv venv
        - venv\Scripts\activate
- install server uvicorn: pip install uvicorn
- install fast api : pip install fastapi uvicorn
- to check the package list: pip freeze

# To run server
- uvicorn app.main:app --reload

# For env setting
- for interface : pip install pydantic-settings

# Connect with mongo db
- for mongo db :  pip install pymongo
- for using EmailStr in service need: pip install email-validator

# Authentication
- Password hashing : pip install "pwdlib[argon2]"
- Auth schemas 
- Register API 
- Login API 
- JWT generation : pip install PyJWT
- JWT verification dependency 
- Current user 
- Protected routes 
- Logout/token expiry

# File Uploading & Serving Static Files
- pip install python-multipart

# Third Party API integration
- pip install httpx

# Implementing Caching
- pip install redis




Future me hum is logger ko aur improve karenge

Production level features add karenge:

✅ Request ID
✅ User ID
✅ API execution time
✅ Client IP
✅ HTTP Method
✅ Status Code
✅ Separate error.log
✅ Middleware integration
✅ JSON logging (optional, ELK/OpenSearch compatible)



database, Redis, scheduler, background workers
