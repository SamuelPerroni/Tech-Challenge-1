from datetime import datetime, timedelta
from passlib.context import CryptContext
from zoneinfo import ZoneInfo
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Security

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
security = HTTPBearer()

SECRET_KEY = 'my-secret-key'


def verify_password(password: str, hash_password: str):
    retorno = pwd_context.verify(password, hash_password)
    return retorno


def get_hash_password(password: str):
    if password is None:
        return None
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encoded_jwt


def decode_token(token):
    try:
        payload = decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token has expired')
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid Token')


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return decode_token(auth.credentials)
