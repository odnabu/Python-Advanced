# Müller Alexander
""" --------------------------------------------------------------------------------------------------
    Homework 2. 12-05-2025
------------------------------------------------------------------------------------------------------ """

print('.' * 80)



""" ______  Task 1  ______________________________________________________________________________________________ """
# Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных,
# обработки вложенных структур и сериализации. Система должна обрабатывать данные в формате JSON.
#   Задачи:
#       1) Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
#       2) Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic,
#          валидирует данные, и в случае успеха сериализует объект обратно в JSON и возвращает его.
#       3) Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
#       4) Написать несколько примеров JSON строк для проверки различных сценариев валидации:
#          успешные регистрации и случаи, когда валидация не проходит (например, возраст не соответствует
#          статусу занятости).
#   Модели:
#       Address: Должен содержать следующие поля:
#           - city: строка, минимум 2 символа.
#           - street: строка, минимум 3 символа.
#           - house_number: число, должно быть положительным.
#       User: Должен содержать следующие поля:
#           - name: строка, должна быть только из букв, минимум 2 символа.
#           - age: число, должно быть между 0 и 120.
#           - email: строка, должна соответствовать формату email.
#           - is_employed: булево значение, статус занятости пользователя.
#           - address: вложенная модель адреса.
#   Валидация:
#       Проверка, что если пользователь указывает, что он занят (is_employed = true),
#       его возраст должен быть от 18 до 65 лет.

# Пример JSON данных для регистрации пользователя:
# #  NOT valid: name, age
# json_input = """
# {
#     "name": "John Doe",
#     "age": 70,
#     "email": "john.doe@example.com",
#     "is_employed": True,
#     "address": {
#         "city": "New York",
#         "street": "5th Avenue",
#         "house_number": 123
#     }
# }
# """

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++
from pydantic import (BaseModel, Field, EmailStr,
                      field_validator, # ValidationInfo,
                      model_validator,
                      ValidationError)
import json
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Вложенная в User модель Address:
class Address(BaseModel):
    city: str = Field( ..., min_length=2, description='Name of city should have minimum 2 symbols.')        # ... - ОБЯЗАТЕЛЬНОЕ ПОЛЕ для заполнения в JSON.
    street: str = Field( ..., min_length=3, description='Name of street should have minimum 3 symbols.')
    house_number: int = Field( ..., gt=0, description='House number can\'t be equal 0.')

# Модель User:
class User(BaseModel):
    # name: строка, должна быть только из букв, минимум 2 символа:
    # ___ 1-st Variant ___ - через pattern:  -----------------------------
    name: str = Field( ..., min_length=2, pattern=r"^[a-zA-Zа-яА-Я]+$")
    # name: str = Field(..., pattern=r"^[A-Za-z]{2,}$", description='Name consists the lettres only and should have minimum 2 letters.')      # или так - как в примере решения: regex="^[A-Za-z]{2,}$"
    # ___ 2-nd Variant ___ - через validator:  -------------------------
    @field_validator('name')
    def validate_name(cls, value):
        if len(value) < 2:
            # Здесь почему-то НЕ рейзит ошибку. И я не понимаю, почему.
            raise ValueError(f'\033[33mName must be at least 2 characters long.\033[0m')
        if not value.isalpha():
            raise ValueError(f'\033[33mName must contain only letters.\033[0m')
        return value
    # --------------------------------------------------------------------
    age: int = Field( ..., gt=0, le=140, description='Age must be between 1 and 140 years.')
    email: EmailStr
    is_employed: bool
    address: Address

    # ----  @field_validator  здесь НЕ работает!  -----------------------------------------------------------------
    # # @classmethod                  # Питон подсвечивает предупреждение, хотя по ссылке выше в документации рекомендуют его использовать.
    # @field_validator('age')         # https://pydantic.com.cn/ru/concepts/validators/#_2
    # def validate_employment_age(cls, v, info: ValidationInfo):
    #     print(ValidationInfo.data.fget('is_employed'))
    #     # if 'is_employed' in values and values.get('is_employed') not in (18 <= v <= 65):      # _values_ НЕ соответствует версии Pydantic.
    #     # if 'is_employed' in info.data and info.data.get('is_employed') not in (18 <= v <= 65):
    #     if info.data.get('is_employed') and not (18 <= v <= 65):
    #         # assert info.data.get('is_employed') is False and info.data.get('age') in (18 <= v <= 65), f'{info.field_name} - Age must be between 18 and 65 years.'
    #         raise ValueError('Employed users must be between 18 and 65 years old.')
    #     return v
    # ---------------------------------------------------------------------------------------------------------------

    @model_validator(mode='after')          # model_validator с mode='after' — кастомная логика на весь объект.
    def check_employment_age(cls, values):
        if values.is_employed and not (18 <= values.age <= 65):
            raise ValueError(f"\033[33mEmployed users must be between 18 and 65 years old.\033[0m")
        return values


def process_user_registration(json_data: str):
    try:
        user = User.model_validate_json(json_data)      # Десериализация + валидация
        return user.model_dump_json(indent=4)           # Сериализация обратно в JSON
    except ValidationError as e:
        # return f"\033[31mValidation Error:\033[m\n{e}"      # Возвращает сообщение об ошибке.
        return e


bound = f'\033[38m{'-' * 60}\033[0m\n'


print(bound, '✅ Правильно заполненные данные --> Успешная регистрация:')
json_input_valid_f = """
{
    "name": "Falkor",
    "age": 4,
    "email": "falkor@nabu.com",
    "is_employed": false,
    "address": {
        "city": "Dessau-Rosslau",
        "street": "Wasserwerkstrasse",
        "house_number": 19
    }
}
"""
# Обработка и вывод результатов для ПРАВИЛЬНО заполненного json:
print(process_user_registration(json_input_valid_f))


print(bound, 'JSON из ЗАДАНИЯ. ❌ Ошибка. NOT valid: name, age.')
json_input = """
{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": True,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""
# Обработка и вывод результатов из JSON в ЗАДАНИИ - NOT valid:
print(process_user_registration(json_input))


print(bound, '❌ Ошибка (возраст не подходит для занятости):')
json_invalid_age = """
{
    "name": "Bob",
    "age": 75,
    "email": "bob@example.com",
    "is_employed": true,
    "address": {
        "city": "London",
        "street": "Baker Street",
        "house_number": 221
    }
}
"""
print(process_user_registration(json_invalid_age))


print(bound, '❌ Ошибка (имя содержит цифры):')
json_invalid_name = """
{
    "name": "John123",
    "age": 25,
    "email": "john@example.com",
    "is_employed": false,
    "address": {
        "city": "Paris",
        "street": "Champs Elysees",
        "house_number": 50
    }
}
"""
print(process_user_registration(json_invalid_name))

print(bound, '❌ Ошибка (имя меньше 2 букв):')
json_invalid_name = """
{
    "name": "J",
    "age": 25,
    "email": "john@example.com",
    "is_employed": false,
    "address": {
        "city": "Paris",
        "street": "Champs Elysees",
        "house_number": 50
    }
}
"""
print(process_user_registration(json_invalid_name))


