from fastapi import HTTPException
from datetime import date


class CoreException(Exception):
    detail = 'System error'
    def __init__(self, *args):
        super().__init__(self.detail)

class RecordNotFoundException(CoreException):
    detail = 'Запись не найдена'

class RecordAlreadyExistException(CoreException):
    detail = "Запись с таким именем уже существует"

class UserAlreadyExistException(CoreException):
    detail = "Пользователь с таким именем уже существует"

class DateFromMoreToException(CoreException):
    detail = "Дата заезда позже дата выезда"

class CoreHttpException(HTTPException):
    status_code = 500
    detail = 'System error'
    def __init__(self, *args):
        super().__init__(status_code=self.status_code, detail=self.detail)

class DateToAfterDateHttpException(CoreHttpException):
    status_code = 422
    detail = "Дата заезда не может быть позже даты выезда"

def check_date_to_after_date_from(date_from:date, date_to:date) -> None:
    if date_from >= date_to:
        raise DateToAfterDateHttpException
    
class HotelNotFoundException(CoreException):
    detail = "Отель не найдено"

class UserNotExistException(CoreException):
    detail = "Пользователь с таким именем не существует"

class WrongUserPasswordException(CoreException):
    detail = "Неверный пароль"

class IncorrectTokenException(CoreException):
    detail = "Срок токена истек"

class HttpHotelNotFoundException(CoreHttpException):
    status_code = 404
    detail = "Отель не найдено"

class RoomNotFoundException(CoreException):
    detail = "Команты в этом отеле нет"

class InccorectFacilityException(CoreException):
    detail = "Неизвестная удобства"

class HttpRoomNotFoundException(CoreHttpException):
    status_code = 404
    detail = "Команты в этом отеле нет"

class HttpInccorectFacilityException(CoreHttpException):
    status_code = 403
    detail = "Неизвестная удобства"

class HttpUserAlreadyExistException(CoreHttpException):
    status_code = 429
    detail = "Пользователь с таким именем уже существует"

class IncorrectTokenHTTPException(CoreHttpException):
    status_code = 400
    detail = "Некорректный токен"