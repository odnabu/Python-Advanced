# Müller Alexader
""" --------------------------------------------------------------------------------------------------
    Lesson 5. 19-05-2025
    Flask: SQLAlchemy. Создание и наполнение базы данных и работа с моделями и полями
------------------------------------------------------------------------------------------------------ """


""" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%____________   Flask: SQLAlchemy   ___________%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """



""" ______  Task 1  ______________________________________________________________________________________________ """
# 1 -- Создание движка подключения: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.
# 2 -- Создание сессии: Создайте сессию в продолжение к предыдущему коду.

# # ++++++++++++++++++++++++++++++++++++++++
# from sqlalchemy import create_engine, Column, Integer, String, Text
# from sqlalchemy.orm import sessionmaker, declarative_base
# # ++++++++++++++++++++++++++++++++++++++++
#
#
# # Установить библиотеку через КОНСОЛЬ:
# #  pip install pymysql
#
#
# # Создаем экземпляр движка SQLAlchemy:
# # engine = create_engine('mysql+pymysql://user:password@localhost:3306/mydatabase')
# engine = create_engine('mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de:3306/group_111124_fp_Dvornyk_Olha')
#
# Base = declarative_base()
# class Test(Base):
#     __tablename__ = 'test'
#     id = Column(Integer, primary_key=True)
#     fullname = Column(String(255))           # Varchar default 255
#     age = Column(Integer)
#
# # Создаем класс Session, который будет использоваться для взаимодействия с БД:
# Session = sessionmaker(bind=engine)
# # Создаем экземпляр сессии:
# session = Session()
#
# Base.metadata.create_all(engine)
# nee_user = Test(fullname='New User', age=20)
# session.add(nee_user)
# session.commit()


# ---------------------------------------------------
# Hanna Kulykovska 10:56 (Edited)
# с спользованием UUID

# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.dialects.mysql import CHAR
# import uuid
#
# engine = create_engine('mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de:3306/group_111124_fp_Dvornyk_Olha')
#
# Base = declarative_base()
# class Test(Base):
#     __tablename__ = 'test'
#     id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     fullname = Column(String(255))            # varchar default
#     age = Column(Integer)
#
# Session = sessionmaker(bind=engine)
# session = Session()
#
# Base.metadata.create_all(engine)
# new_user = Test(fullname='олваормироив', age=25)
# session.add(new_user)
# session.commit()
# ---------------------------------------------------


""" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%___________   Внешний ключ SQLAlchemy   __________%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """

# Установка sqlite -- с сайта
# pip install sqlite3


""" __________ Пример использования relationship __________ """

""" ------  по прямым ссылкам  ------------------------------------------------------------ """

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, create_engine
# from sqlalchemy.orm import relationship, declarative_base, sessionmaker
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# С подключением ich1 НЕ сработает, т.к. на этом сервере стоит ограничение на ForeignKey:
# engine = create_engine('mysql+pymysql://ich1:ich1_password_ilovedbs@'
#                        'ich-edit.edu.itcareerhub.de:3306/group_111124_fp_Dvornyk_Olha')

# engine = create_engine("sqlite:///test.db")
# Base = declarative_base()
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(30))               # , unique=True
#     posts = relationship("Post", back_populates="author")
#
# class Post(Base):
#     __tablename__ = 'posts'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(30))
#     user_id = Column(Integer, ForeignKey('users.id'))
#     author = relationship("User", back_populates="posts")
#
# Session = sessionmaker(bind=engine)
# session = Session()
#
# Base.metadata.create_all(bind=engine) # создаем таблицы на основании моделей
# user1 = User(name='David')
# post1 = Post(title="How does AI work?", author=user1, user_id=user1.id)
#
# session.add(user1)
# session.add(post1)
#
# session.commit()
#
# print(session.query(User).first().posts[0].title)
#
# ---------------------------------------------------------------------------------------


""" ------  с backref  ------------------------------------------------------------------ """

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
# from sqlalchemy.orm import relationship, declarative_base, sessionmaker
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# engine = create_engine("sqlite:///test.db")
# Base = declarative_base()
# class User(Base):
#     tablename = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(30), unique=True)
#     posts = relationship("Post", backref="author")
#
# class Post(Base):
#     tablename = 'posts'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(30))
#     user_id = Column(Integer, ForeignKey('users.id'))
#
# Session = sessionmaker(bind=engine)
# session = Session()
#
# Base.metadata.create_all(bind=engine) # создаем таблицы на основании моделей
# user1 = User(name='David')
# post1 = Post(title="How does AI work?", author=user1, user_id=user1.id)
#
# session.add(user1)
# session.add(post1)
#
# session.commit()
# print(list(session.query(User)))
# ---------------------------------------------------------------------------------------


""" ______  Task 2  ______________________________________________________________________________________________ """
# ___ Pydantic ___
# Определение модели события: Создайте модель Event, которая включает поля:
#   ● title (строка),
#   ● date (дата и время события),
#   ● location (строка).
# Добавьте валидацию, чтобы дата события не была в прошлом.

# ++++++++++++++++++++++++++++++++++++++++++
from pydantic import BaseModel, field_validator, ValidationError
from datetime import datetime
# ++++++++++++++++++++++++++++++++++++++++++

class Event(BaseModel):
    title: str
    date: datetime
    location: str

    # @classmethod          # Здесь НЕ нужен, те его можно НЕ прописывать в НОВОЙ версии Питона.
    @field_validator('date')
    def validate_date(cls, value):
        print(value)
        if value < datetime.now():
            raise ValueError('Date must be in the future!')
        return value

test_date = datetime.fromisoformat('2023-01-10T13:45:30.391125')
print(datetime.now())

try:
    event1 = Event(title='Konzert 1', date=test_date, location='Dessau')
    print(event1)
except ValidationError as e:
    print(e)



""" ______  Task 3  ______________________________________________________________________________________________ """
#


""" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%___________   ---   __________%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """


""" __________ --- __________ """
#       ●
# ___ EXAMPLE __________________________________________________
# ___ END of Example __________________________________________________


""" ______  Task 1  ______________________________________________________________________________________________ """
#





