

class CoreException(Exception):
    detail = 'System error'
    def __init__(self, *args):
        super().__init__(self.detail)

class RecordNotFoundException(CoreException):
    detail = 'Запись не найдена'

class UserAlreadyExistException(CoreException):
    detail = "Пользователь с таким именем уже существует"

class DateFromMoreToException(CoreException):
    detail = "Дата заезда позже дата выезда"