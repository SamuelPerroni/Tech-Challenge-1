from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from .schemas import UserIn, UserOut, UserUpdate, Token
from .models import User
from ..database import SessionLocal
from .utils import get_hash_password, verify_password, create_access_token

# rotas de exportacao
security_router = APIRouter()


# CREATE USER
@security_router.post("/create",
                      response_model=UserOut,
                      status_code=status.HTTP_201_CREATED)
async def create_User(user_create: UserIn):

    async with SessionLocal() as session:
        user_obj = await User.get(session, user_create.user_name)
        if user_obj is None:
            user_to_create = User(**user_create.model_dump())
            hash_pass = get_hash_password(user_to_create.user_pass)
            setattr(user_to_create, 'user_pass', hash_pass)
            response = await User.create(session, user_to_create)
            return response
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User name already exists")


# UPDATE USER
@security_router.put("/", response_model=UserOut,
                     status_code=status.HTTP_200_OK)
async def update(user_update: UserUpdate):

    async with SessionLocal() as session:
        user_obj = await User.get(session, user_update.user_name)
        if user_obj:
            if verify_password(user_update.user_pass, user_obj.user_pass):
                return await User.update(session,
                                         user_obj,
                                         **{'user_name': user_update.new_user_name,
                                            'user_pass': get_hash_password(user_update.new_user_pass)})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User name or password are incorrect")


# DELETE USER
@security_router.delete('/', status_code=status.HTTP_200_OK)
async def delete_user_object(user_name: Annotated[str | None,
                                                  Query(description="Query for user_name")] = None,
                             user_pass: Annotated[str | None,
                                                  Query(description="Query for password")] = None):

    async with SessionLocal() as session:
        user_obj = await User.get(session, user_name)
        if user_obj:
            if verify_password(user_pass, user_obj.user_pass):
                await User.delete(session, user_obj)
                return {"message": "deleted"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User name or password are incorrect")


# GET ID USER
@security_router.get('/{user_name}',
                     response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user_id_object(user_name: Annotated[str,
                                                  Path(title="The user name of the item to get")]):

    async with SessionLocal() as session:
        user_obj = await User.get(session, user_name)
        if user_obj:
            return user_obj
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User name doesn't exist")


# CREATE TOKEN
@security_router.post('/token',
                      response_model=Token)
async def login_for_access_token(user_token: UserIn):

    async with SessionLocal() as session:
        user_obj = await User.get(session, user_token.user_name)
        if user_obj:
            if verify_password(user_token.user_pass, user_obj.user_pass):
                access_token = create_access_token(
                    data={'sub': user_token.user_name})
                return {'access_token': access_token, 'token_type': 'bearer'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User name or password are incorrect")
