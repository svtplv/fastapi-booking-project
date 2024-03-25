from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from app.config import settings
from app.users.exceptions import (IncorrectTokenFormatException,
                                  TokenAbsentException, TokenExpiredException,
                                  TokenInvalidDataException)
from app.users.service import UsersService


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get('sub')
    if not user_id:
        raise TokenInvalidDataException
    print(user_id)
    user = await UsersService.get_by_id(int(user_id))
    if not user:
        raise TokenInvalidDataException
    return user