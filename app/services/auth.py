from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (hash_password,
                               verify_password ,
                               create_access_token ,
                               create_refresh_token ,
                               decode_refresh_token)
from app.schemas.auth import Auth
from app.repository.auth import get_user_by_email, create_user
from app.db.models import User
from app.repository.department import department_get_by_name_or_id

async def singup(
        db:AsyncSession,
        data: Auth.SignupRequest
)->User:

   # check user email first to create for unqiue email
   exsisting_user =  await get_user_by_email(db,data.email)


    # check for unique email check
   if exsisting_user is not None:
      raise HTTPException(
                      status_code=400,
                      detail="Email is already exist."
                   )

   # check department exist or not
   if data.department_id in None:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail="department id is required"
      )
   
   department = await department_get_by_name_or_id(db=db, department_id=data.department_id)

   if department is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="Selected department is not found"
      )
   try:

      # convert password into hash password
      pasword_hash = hash_password(data.password)
       # create new object with hash password
      user_data_dict  = User(
         name=data.username,
         email=data.email,
         password_hash=pasword_hash,
         department_id = data.department_id
      )

      user = await create_user(db,user_data_dict )
      await db.commit()
      await db.refresh(user)
      
      return user
   
   except Exception:
        await db.rollback()
        raise

async def login_request(db:AsyncSession,
                        data:Auth.LoginRequest):
   # get user detail
   is_exsist = await get_user_by_email(db,data.email)

   # check user exsist
   if is_exsist is None:
      return None

   # check password with hased password
   password_verified = verify_password(data.password, is_exsist.password_hash)

   if not password_verified:
      return None

   # generate access token
   access_token = create_access_token(
      user_id=is_exsist.id
   )

   # generate refresh token
   refresh_token  = create_refresh_token(
      user_id=is_exsist.id
   )

   return {
      "access_token":access_token,
      "refresh_token":refresh_token,
      "token_type":'bearer'
   }


def refresh_access_token(
      refresh_token:str
):
   payload = decode_refresh_token(refresh_token)

   user_id = payload.get('sub') 

   if not user_id:
      raise HTTPException(
                 status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Invaild Resfresh Token"
             )

   # generate refresh token
   refresh_token  = create_refresh_token(
         user_id=user_id
      )
   user_token = create_access_token(user_id)
   
   return Auth.RefreshToken(
           access_token=user_token,
           refresh_token=refresh_token,
           token_type="bearer"
       )

