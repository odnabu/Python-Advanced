# Nagashbayev Al-Farabi
""" --------------------------------------------------------------------------------------------------
    Lesson 3. 15-05-2025
------------------------------------------------------------------------------------------------------ """


""" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%_________   Pydantic: Применение etc.   ________%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """

# +++++++++++++++++++++++++++++++
from pydantic import BaseModel, Field, EmailStr, ConfigDict
# from Maksym Poliakov 10:11
from typing import List, Any
# +++++++++++++++++++++++++++++++

# class Address(BaseModel):
#     street: str
#     city: str
#     state: str
#     house_number: int
#     # zipcode: int
#
# class User(BaseModel):
#     # id: int
#     # id: int = Field(default_factory=int)
#     id: int = Field(default=0)
#     name: str
#     age: int
#     # city: str = 'Dessau'
#     address: Address
#     # tel: list[str] = []       # Такой синтаксис НЕкорректный, если так делать то может возникнуть проблема.
#     tel: list[str] = Field(default_factory=list)        # Так КОРРЕКТНО.
#     # ------------ # Maksym Poliakov --------------------------------
#     # tel: List[str] = []
#     # tel: List[str] = Field(default_factory=List)        # Так НЕ работает - ERROR.
#     # ----------------------------------------------------------------
#
# # user1 = User(id=0, name='John', age='22')
# # print(user1)
#
# # user1 = User(id=0, name='John', age=22,
# #              address=Address(street='Wasserwerkstrasse', city='Dessau', state='Deutschland', house_number='19'))
# # print(user1)
#
# user1 = User(id=0, name='John', age=22,
#              address=Address(street='Wasserwerkstrasse', city='Dessau', state='Deutschland', house_number='19'))
# user1.tel.append('123456')
# user2 = User(id=0, name='Alla', age=42,
#              address=Address(street='Kavalierstrasse', city='Dessau', state='Deutschland', house_number='4'))
# print(user1)
# print(user2)
#
# # # Пример добавления в список:
# # def test(lst=[]):
# #     lst.append(1)
# #     print(lst)
# #
# # test()
# # test()


""" ______  Task 1  ______________________________________________________________________________________________ """
# Создать класс, который принимает данные пользователя в формате JSON и валидирует их на уровне типов данных.
# Данные включают:
#   ● имя пользователя
#   ● возраст
#   ● email
#   ● адрес (город, улица, номера дома)


# class Address(BaseModel):
#     street: str
#     city: str
#     state: str
#     house_number: int
#
# class User(BaseModel):
#     id: int = Field(default=0)
#     name: str
#     age: int
#     address: Address
#     phones: list[str] = Field(default_factory=list)
#
# json_string_user = """
# {
#     "id":0,
#     "name":"UserName",
#     "age":18,
#     "address": {
#         "street":"Street",
#         "city":"City",
#         "state":"State",
#         "house_number":1
#     },
#     "phones":[ "123456789"]
# }
# """
#
# user1 = User.model_validate_json(json_string_user)
# print(user1)
#
# user1.address = Address(street="Street2", city="City", state="State", house_number=1)
# print(user1)


""" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%___________   Наследование в Pydantic   __________%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """


# class Address(BaseModel):
#     street: str
#     city: str
#     state: str
#     house_number: int
#
# class User(BaseModel):
#     id: int = Field(default=0)
#     name: str
#     age: int
#     address: Address
#     phones: list[str] = Field(default_factory=list)
#     model_config = ConfigDict(validate_assignment=True)
#     # -------- Year of Birth Validator ----------------------------------------
#     # year_of_birth: str = ''
#     #
#     # def model_post_init(self, context: Any, /) -> None:
#     #     super().__init__()
#     #     pass
#     # -------------------------------------------------------------------------
#
#     # -------- Email Validator -----------------------------------------------
#     email: EmailStr
#     # -------------------------------------------------------------------------
#
#     def __str__(self):
#         return f'id: {self.id}, name: {self.name}, age: {self.age}, address: {self.address}, phones: {self.phones}'
#
#
#
# json_string_user = """
# {
#     "id":0,
#     "name":"UserName",
#     "age":18,
#     "address": {
#         "street":"Street",
#         "city":"City",
#         "state":"State",
#         "house_number":1
#     },
#     "phones":[ "123456789"],
#     "email": "od@gmal.com"
# }
# """
#
# user1 = User.model_validate_json(json_string_user)
# print(user1)
#
# # user2 = User(id=0, name='OD', age=49, _________ )       # Это было для валидатора ГОДА рождения.
# user1.address = Address(street="New Street", city="City", state="State", house_number=1)
# print(user1)


""" __________ Пример наследования __________ """

# # Основная модель пользователя
# class User(BaseModel):
#     name: str
#     email: EmailStr
#
# # Расширенная модель пользователя с дополнительными полями
# class AdminUser(User):
#     is_superuser: bool
#     access_level: int
#
# user = User(name='ali', email='test@test.com')
# admin = AdminUser(name='admin', email='admin@test.com', is_superuser=True, access_level=10)
# print(user)
# print(admin)


""" __________ Конфигурирование сохранения данных __________ """

# from datetime import datetime
#
# class User(BaseModel):
#     signup_ts: datetime
#     age: int
#
#     class Config:
#         json_encoders = {
#             datetime: lambda v: v.strftime('%d-%m-%Y %H:%M'),
#             int: lambda v: f"{v} years old",
#         }
#
# user = User(signup_ts=datetime.now(), age=10)
# print(user)
# print(user.model_dump_json())

""" __________ --- __________ """

# from pydantic import BaseModel, EmailStr, Field
#
# class User(BaseModel):
#     email: EmailStr
#     # username: str = Field(default_factory=lambda data: data['email']) #
#     username: str = Field(default_factory=lambda data: data['email'])
#
# user = User(email='user@example.com')
# print(user.username)
# #> user@example.com




""" ______  Task 2  ______________________________________________________________________________________________ """
# Реализовать систему пользователей:
# ● базовые пользователи имеют базовые атрибуты и возможности,
# ● администраторы наследуют все атрибуты пользователей и имеют дополнительные привилегии.







""" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%___________   ---   __________%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """


""" __________ --- __________ """
#       ●
# ___ EXAMPLE __________________________________________________
# ___ END of Example __________________________________________________


""" ______  Task 1  ______________________________________________________________________________________________ """
#



