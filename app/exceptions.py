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


class RoomNotAvailableException(MyBookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Не осталось свободных номеров.'


class NotFoundException(MyBookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Объект не найден.'


class NegativeTimeDeltaException(MyBookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Дата въезда не может быть позже даты выезда.'


class NegativeArivalException(MyBookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Дата въезда не может быть меньше текущей даты.'


class StayLimitException(MyBookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Время бронирования не может быть больше 30 дней'


class HotelsNotAvailableException(MyBookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Нет достуных отелей по данному запросу.'
