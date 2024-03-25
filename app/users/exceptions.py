from fastapi import HTTPException, status


class MyBookingException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(MyBookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже существует.'


class IncorrectEmailOrPasswordException(MyBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверная почта или пароль.'


class TokenExpiredException(MyBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен истек.'


class TokenAbsentException(MyBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен отсутствует.'


class IncorrectTokenFormatException(MyBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Некорректный формат токена.'


class TokenInvalidDataException(MyBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Переданные данные некорректны.'
