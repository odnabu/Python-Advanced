# Müller Alexander
""" --------------------------------------------------------------------------------------------------
    Homework 3: SQLAlchemy: Создание и наполнение базы данных. 21-05-2025
------------------------------------------------------------------------------------------------------ """

print('.' * 80)



""" ______  Task 1  ______________________________________________________________________________________________ """
# Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.
# Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.
# Задача 3: Определите модель продукта Product со следующими типами колонок:
#   id: числовой идентификатор
#   name: строка (макс. 100 символов)
#   price: числовое значение с фиксированной точностью
#   in_stock: логическое значение
# Задача 4: Определите связанную модель категории Category со следующими типами колонок:
#   id: числовой идентификатор
#   name: строка (макс. 100 символов)
#   description: строка (макс. 255 символов)
# Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id.

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from sqlalchemy import (create_engine, Column, Integer, String, Numeric, Boolean,
                        ForeignKey, event)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Session
from sqlalchemy import event
import logging
# Модуль rich для красивого вывода в консоли:
from rich import print              # https://github.com/textualize/rich/blob/master/README.ru.md
from rich.console import Console
from rich.table import Table
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


""" ___ Настройка ЛОГГИРОВАНИЯ _________________________________________________________ """
# Создание логгера:
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создание обработчика для записи в файл:
file_handler = logging.FileHandler('db.log', mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Формат логов:
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)

# Добавление обработчика к логгеру:
logger.addHandler(file_handler)



""" ___ Проверка наличия БД --> для отладки _________________________________________________ """
# Пояснение этого кода в конце файла:
import os
path = 'hw03_product.db'
l = 80
if os.path.exists(path):
    os.remove(path)
    print(f'[purple4]{'\\\\' * l}[/purple4]')
    print(f'\tThe database {path} has been deleted.\n'
          f'\tNow will be created the new database with the same name:\n{path: >{len(path)+20}}.\n'
          f'[purple4]{'/' * l}[/purple4]')


# ________________________________________________________________________________________________
# Задача 1: Создайте экземпляр движка SQLAlchemy для подключения к SQLite базе данных в памяти:
engine = create_engine('sqlite:///hw03_product.db')

#  Чтобы создать БД в памяти, а не в файле, можно использовать команду:
# engine = create_engine('sqlite:///:memory:', echo=True)
#   :memory: — создаёт временную БД, которая исчезает после завершения программы.
#   echo=True — показывает все SQL-запросы в консоли (очень удобно для отладки!).
Base = declarative_base()       # See Les05-Django_5-SQLAlchemy.pdf, slide 30-33.


# ________________________________________________________________________________________________
# Задача 2: Создайте сессию (класс Session) для взаимодействия с базой данных, используя созданный движок:
Session = sessionmaker(bind=engine)
# Создаем экземпляр сессии:
session = Session()

# ________________________________________________________________________________________________
# Задача 3: Определите модель продукта Product со следующими типами колонок:
# Определяем класс `Product`, который наследуется от базового класса `Base`.
# Этот класс представляет собой сущность базы данных.
# (See Les05-Django_5-SQLAlchemy.pdf  &  See Les05-Django_6-SQLAlchemy.pdf).
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, nullable=False)                      # See Les05-Django_6-SQLAlchemy.pdf, slide 20, 53.
    category_id = Column(Integer, ForeignKey('categories.id'))               # Создаём связь --> Одна связь!
    category = relationship('Category', back_populates='product')  #  Обратная связь.

    # ___ Для красивой печати в терминале:
    def __str__(self):
        return (f"{self.name} | {self.price} € | "
                f"In stock: {'Yes' if self.in_stock else 'No'} | "
                f"Category: {self.category.name if self.category else 'No'}")

    # ___ Для записи логов:
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, in_stock={self.in_stock})>"


# ________________________________________________________________________________________________
# Задача 4: Определите связанную модель категории Category со следующими типами колонок:
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)      # Crossover, Sedan, Hatchback, Station Wagon, Coupe, Convertible, Minivan
    description = Column(String(255), nullable=False)
    # Relationship:     See Les05-Django_6-SQLAlchemy.pdf, slide 32-33, 42.
    #   ● первый параметр в relationship — таблица, с которой будет связь.
    #   ● в back_populates — ссылочное имя с другой таблицы на текущую.
    product = relationship('Product', back_populates='category')      # "Один ко многим".
    # "Один ко многим" - тк категория, например, Crossover, может относиться к моделям разных характеристик
    # например, года выпуска, типа двигателя и тд и тп.

    # ___ Для красивой печати в терминале:
    def __str__(self):
        return f"{self.name} — {self.description[:40]}..."  # Обрезаем, чтобы не было слишком длинно

    # ___ Для записи логов:
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"



# Car body style: https://en.wikipedia.org/wiki/Car_body_style.
# Crossover cars, also known as crossover utility vehicles (CUVs), are a type of Sedan (SUV) that combines
# the features of a car with those of an SUV.


# Чтобы в БД появилась таблицы, вызываем метод `create_all()` объекта `metadata` базового класса `Base`.
# SQLAlchemy автоматически анализирует классы моделей данных и создает соответствующие таблицы в БД `hw03_product`.
Base.metadata.create_all(bind=engine)       # создаем таблицы на основании моделей, Les05-Django_5-SQLAlchemy.pdf, slide 33.



""" ___ Логгирование изменений в файл логов _____________________________________________________ """
# Событие: объект добавлен
@event.listens_for(Session, "after_flush")
def log_changes(session, flush_context):
    for obj in session.new:
        logger.info(f"✅ Добавлен: {obj}")
    for obj in session.dirty:
        logger.info(f"➡️ Изменён: {obj}")
    for obj in session.deleted:
        logger.info(f"❌ Удалён: {obj}")



""" ___ Создание нового продукта и категории, добавление их в таблицу ____________________________________________ """

# Создание описания категорий:
descriptions_all = {
    "descript_1": ('A mid-size crossover SUV known for its stylish design, comfortable interior, and '
                   'advanced technology. It is a type of Sedan (SUV) that combines the features of '
                   'a car with those of an SUV.'),
    "descript_2": 'Car with a hatch-type rear door that is hinged at the roof and opens upwards.',
    "descript_3": 'Car with a roofline that slopes continuously down at the back. '
                  'The design features a single unbroken convex curve from the roof to the rear.'
}
categories_all = {
    "category_1": Category(name='Crossover', description=descriptions_all.get("descript_1")),
    "category_2": Category(name='Hatchback', description=descriptions_all.get("descript_2")),
    "category_3": Category(name='Fastback', description=descriptions_all.get("descript_3"))
}
# Создание новых продуктов:
autos = {
"product_1": Product(name='Peugeot 3008, GT Hybrid, 2024', price=40000, in_stock=True,
                     category=categories_all.get("category_1")),
"product_2": Product(name='Peugeot 3008, Allure Hybrid, 2024', price=35000, in_stock=False,
                     category=categories_all.get("category_1")),
"product_3": Product(name='Peugeot 5008, GT Hybrid, 2024', price=47000, in_stock=True,
                     category=categories_all.get("category_1")),
"product_4": Product(name='Peugeot 5008, Allure Hybrid, 2024', price=41000, in_stock=False,
                     category=categories_all.get("category_1")),
"product_5": Product(name='Peugeot 308, GT Hybrid, 2024', price=43000, in_stock=True,
                     category=categories_all.get("category_2")),
"product_6": Product(name='Peugeot 408, GT Hybrid, 2024', price=48000, in_stock=True,
                     category=categories_all.get("category_3"))
}


# Добавляем объекты в сессию с помощью метода `add()`:   (Les05-Django_5-SQLAlchemy.pdf, slide 33)
for key, c in categories_all.items():
    session.add(c)
for key, a in autos.items():
    session.add(a)

# Вызываем метод `commit()`, чтобы зафиксировать все изменения в базе данных:
# (Les05-Django_5-SQLAlchemy.pdf, slide 33)
session.commit()



""" ___ Проверка того, что получилось: _______________________________________________________ """
# Простой вывод:
# print(list(session.query(Product)))
# print('category.name: ', session.query(Product).first().category.name)

# ИЛИ таким образом:
# category = session.query(Category).first()
# for product in category.product:
#     print(product.name)

# ИЛИ в виде таблицы:
def print_products():
    print()
    console = Console(force_terminal=True)
    table = Table(title="Peugeot catalog", title_style="bold magenta")

    table.add_column("ID", style="white", justify="center")
    table.add_column("Name", style="bold white")
    table.add_column("Price (€)", style="white", justify="right")
    table.add_column("In stock", style="yellow", justify="center")
    table.add_column("Category", style="white")

    products = session.query(Product).all()
    for p in products:
        table.add_row(
            str(p.id),
            p.name,
            f"{float(p.price):,.2f}",
            "[green]Yes[/green]" if p.in_stock else "[red]No[/red]",
            p.category.name if p.category else "—"
        )

    console.print(table)

# # Вызов:
# print_products()



# ___ БЫЛА ПРОБЛЕМА: _______________________________________________________________________________________
# Использование sqlite:///hw03_product.db приводит к тому, что файл базы данных сохраняется на диск.
# Если раньше запускался скрипт без какого-либо поля (у меня было category_id), то SQLAlchemy создаст таблицу
# (products) без этой колонки.
# После корректировки кода и добавления колонки SQLite не обновляет таблицу автоматически,
# даже после Base.metadata.create_all() — он не делает миграции, а просто игнорирует, если таблица уже есть.

# Чтобы устранить проблему, нужно Удалить файл БД и пересоздать его.
# Для этого можно просто удалить файл hw03_product.db, чтобы SQLAlchemy создала всё заново с правильными колонками:
#   1) Закрыть все сессии с базой.
#   2) Удалить файл hw03_product.db вручную (или в коде, см. ниже).
#   3) Запустить скрипт заново.
#
# Можно добавить код на удаление БД в начало файла Python, чтобы удалять автоматически при тестировании:
# import os
# path = 'Homeworks/HW_03/hw03_product.db'
# if os.path.exists(path):
#     os.remove(path)
#     print('.' * 40)
#     print(f'The database {path.split('/')[2]} has been deleted.')
# _____________________________________________________________________________________________________________


# Чтобы увидеть красивый вывод, нужно вызвать файл со скриптом в ТЕРМИНАЛЕ:
# python Homeworks/HW_03/HW03-21_05-SQLAlchemy.py

if __name__ == '__main__':
    print_products()
