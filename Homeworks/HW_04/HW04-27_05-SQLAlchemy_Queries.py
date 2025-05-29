# Müller Alexander
""" --------------------------------------------------------------------------------------------------
    Homework 4: SQLAlchemy: Создание и наполнение базы данных. 27-05-2025
------------------------------------------------------------------------------------------------------ """
# See:
#       Les07-Django_7-SQLAlchemy_SQL_Queries_1.pdf + Conspectus
#       Les07-Django_8-SQLAlchemy_SQL_Queries_2.pdf + Conspectus
#       Les10-Django_PrfS3---.pdf


print('.' * 80)

# Для запуска файла в ТЕРМИНАЛЕ ввести команду:
# python Homeworks/HW_04/HW04-27_05-SQLAlchemy_Queries.py


""" %%%%%%%%   Task 1   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """
# Задача 1: Наполнение данными.
# Добавьте в базу данных следующие категории и продукты:
#   1) Добавление категорий: Добавьте в таблицу categories следующие категории:
#       - Название: "Электроника", Описание: "Гаджеты и устройства."
#       - Название: "Книги", Описание: "Печатные книги и электронные книги."
#       - Название: "Одежда", Описание: "Одежда для мужчин и женщин."
#   2) Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись,
#      что каждый продукт связан с соответствующей категорией:
#       - Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
#       - Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
#       - Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
#       - Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
#       - Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import logging
import os           # Для отладки создания таблицы и наполнения ее данными
from sqlalchemy import (create_engine, Column, Integer, String, Numeric,
                        Boolean, ForeignKey, event, func)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Session
# ______ Модуль rich для красивого вывода в консоли _______________________________
from rich import print  # https://github.com/textualize/rich/blob/master/README.ru.md
from rich.console import Console
from rich.table import Table
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


""" ___ Настройка ЛОГГИРОВАНИЯ ___________________________________________________________________________________ """
    # Создание логгера:
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
    # Создание обработчика для записи в файл:
file_handler = logging.FileHandler('Homeworks/HW_04/db_hw04.log', mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)
    # Формат логов:
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
    # Добавление обработчика к логгеру:
logger.addHandler(file_handler)


""" ___ Проверка наличия БД --> для отладки _____________________________________________________________________ """
path = 'Homeworks/HW_04/hw04_products.db'
l = 80
if os.path.exists(path):
    os.remove(path)
    print(f'\n[grey50]{'=' * l}[/grey50]')
    print(f'   The old version of DB [green4]{path}[/green4] has been deleted.\n'
          f'   Was created DB with the same name and corrected data:   [sea_green2]{path: >{len(path)}}[/sea_green2].\n'
          f'[grey50]{'=' * l}[/grey50]')


""" ___ Создание движка (собственно БД), сессии и ее экземпляра ________________________________________________  """
# Экземпляр движка SQLAlchemy для подключения к SQLite базе данных в памяти:
engine = create_engine('sqlite:///Homeworks/HW_04/hw04_products.db')
Base = declarative_base()       # See Les05-Django_5-SQLAlchemy.pdf, slide 30-33.
# Создание сессии (класс Session) для взаимодействия с базой данных, с использованием созданного движка:
Session = sessionmaker(bind=engine)
# Создание экземпляра сессии:
session = Session()


""" ___ Классы для таблиц и данных в них _______________________________________________________________________  """

# Связь между таблицами в этой задаче - "Одно-ко-многим и многие-к-одному"
# (см. Les05-Django_6 Конспект-SQLAlchemy.pdf, с. 15).

# ______ Класс Category ________________________________________________________________________________________
# Модель  "Category" (для создания таблицы категорий). Связь "Одно-ко-многим".
# (See Les05-Django_5-SQLAlchemy.pdf  &  See Les05-Django_6-SQLAlchemy.pdf).
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    # Relationship:     See Les05-Django_6-SQLAlchemy.pdf, slide 32-33, 42.
    #   ● первый параметр в relationship — таблица, с которой будет связь.
    #   ● в back_populates — ссылочное имя с другой таблицы на текущую.
    goods = relationship('Product', back_populates='category')      # Одна категория - несколько продуктов.

    # ___ Для красивой печати в терминале:
    def __str__(self):
        return f"{self.name} — {self.description[:40]}..."  # Обрезка описания, чтобы не было слишком много текста в консоли.

    # ___ Для записи логов:
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


# ______ Класс Product __________________________________________________________________________________________
# Модель "Product" (для создания таблицы товаров). Связь "Многие-к-Одному".
# Класс `Product`, так же наследуется от базового класса `Base`.
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, nullable=False)                      # See Les05-Django_6-SQLAlchemy.pdf, slide 20, 53.
    category_id = Column(Integer, ForeignKey('categories.id'))               # Создаём связь --> Одна связь!
    category = relationship('Category', back_populates='goods')  #  Обратная связь.

    # ___ Для красивой печати в терминале:
    def __str__(self):
        return (f"{self.name} | {self.price} € | "
                f"Наличие на складе: {'Да' if self.in_stock else 'Нет'} | "
                f"Категория: {self.category.name if self.category else 'Нет'}")

    # ___ Для записи логов:
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, in_stock={self.in_stock})>"


# ______ Создание таблиц в БД ___________________________________________________________________________________
# Для появления таблиц в БД `hw04_products.bd` нужно вызвать метод `create_all()` объекта `metadata` базового класса `Base`.
# Создание таблиц на основании моделей (Les05-Django_5-SQLAlchemy.pdf, slide 33):
Base.metadata.create_all(bind=engine)


""" ___ Логирование изменений в файл логов ______________________________________________________________________ """
# Событие - объект добавлен / изменен / удален:
@event.listens_for(Session, "after_flush")
def log_changes(session, flush_context):
    for obj in session.new:
        logger.info(f"✅ Добавлен: {obj}")
    for obj in session.dirty:
        logger.info(f"➡️ Изменён: {obj}")
    for obj in session.deleted:
        logger.info(f"❌ Удалён: {obj}")


""" ___ Добавление категорий и продуктов в таблицы ______________________________________________________________ """

# ______ Категории и их описания _________________________________________________________________________________
# Описания категорий:
descriptions_all = {
    "descript_1": "Гаджеты и устройства.",
    "descript_2": "Печатные книги и электронные книги.",
    "descript_3": "Одежда для мужчин и женщин."
}
categories_all = {
    "category_1": Category(name='Электроника', description=descriptions_all.get("descript_1")),
    "category_2": Category(name='Книги', description=descriptions_all.get("descript_2")),
    "category_3": Category(name='Одежда', description=descriptions_all.get("descript_3"))
}


# ______ Новые товары ____________________________________________________________________________________________
# Добавление новых продуктов в таблицу "products":
goods_all = {
"product_1": Product(name='Смартфон', price=299.99, in_stock=True, category=categories_all.get("category_1")),
"product_2": Product(name='Ноутбук', price=499.99, in_stock=True, category=categories_all.get("category_1")),
"product_3": Product(name='Научно-фантастический роман', price=15.99, in_stock=True, category=categories_all.get("category_2")),
"product_4": Product(name='Джинсы', price=40.50, in_stock=True, category=categories_all.get("category_3")),
"product_5": Product(name='Футболка', price=20.00, in_stock=True, category=categories_all.get("category_3"))
}

# Добавление объектов в сессию с помощью метода `add()`:   (Les05-Django_5-SQLAlchemy.pdf, slide 33)
for key, c in categories_all.items():
    session.add(c)
for key, a in goods_all.items():
    session.add(a)

# Вызов метода `commit()` для фиксирования все изменений в БД (Les05-Django_5-SQLAlchemy.pdf, slide 33):
session.commit()


""" ___ Печать содержимого таблиц из БД ________________________________________________________________________ """
# Простой вывод:
# print(list(session.query(Product)))
# print('category.name: ', session.query(Product).first().category.name)
# category = session.query(Category).first()
# for product in category.goods:
#     print(product.name)

# Форматирование вывода в виде таблицы:
def print_products(products, table_title, col1=None, col2=None, col3=None, col4=None, col5=None):
    print()
    console = Console(force_terminal=True)
    table = Table(title=table_title, title_style="bold magenta", border_style="purple4")

    if col1:
        table.add_column(col1, header_style="purple", style="white", justify="center")
    if col2:
        table.add_column(col2, header_style="purple", style="white")
    if col3:
        table.add_column(col3, header_style="purple", style="white", justify="right")
    if col4:
        table.add_column(col4, header_style="purple", style="yellow", justify="center")
    if col5:
        table.add_column(col5, header_style="purple", style="white")

    if col1 and col2 and col3 and col4 and col5:
        for p in products:
            table.add_row(
                str(p.id),
                p.name,
                f"{float(p.price):,.2f}",
                "[green]Да[/green]" if p.in_stock else "[red]Нет[/red]",
                p.category.name if p.category else "—"
            )
    elif col1 or col2 or col3 or col4 or col5:
        for p in products:
            # print(str(p[0]), str(p[1]))
            # table.add_row(str(p[0]), str(p[1]))
            table.add_row(*(str(item) for item in p))

    console.print(table)

# Печать таблиц по ВЫЗОВУ функции print_products() в конце этого файла с кодом.

# Чтобы увидеть красивый вывод, нужно вызвать файл со скриптом в ТЕРМИНАЛЕ:
# python Homeworks/HW_03/HW03-21_05-SQLAlchemy.py




""" %%%%%%%%   Task 2   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """
# Задача 2: Чтение данных.
# Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все
# связанные с ней продукты, включая их названия и цены.

print(f"\n[grey50]{'%%%   Task 2: SELECT data from "categories" and "products"   ':%<{l}}[/grey50]")
products = session.query(Product).all()
print_products(products, "PRODUCTS CATALOG", "ID", "Название", "Цена (€)", "На складе", "Категория")


""" %%%%%%%%   Task 3   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """
# Задача 3: Обновление данных
# Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.

print(f"\n[grey50]{'%%%   Task 3: UPDATED data in "products"   ':%<{l}}[/grey50]")
# See:
#       - Les07-Django_7 Конспект-SQLAlchemy_SQL_Queries_1.pdf, p. 4.
#       - Les10-Django_PrfS3.pdf, p. 3.
product_name = 'Смартфон'
new_price = 349.99
changed_product = session.query(Product).filter(Product.name == product_name).first()
if changed_product:
    changed_product.price = new_price
    session.commit()
    print(f"\tUpdated price for [khaki1]{product_name}[/khaki1] to [medium_spring_green]{new_price}[/medium_spring_green].")
else:
    print(f"Product [/gold3]{product_name}[/gold3] not found.")

products_upd = session.query(Product).all()
print_products(products_upd, "PRODUCTS CATALOG upd", "ID", "Название", "Цена (€)", "На складе", "Категория")


""" %%%%%%%%   Task 4   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """
# Задача 4: Агрегация и группировка
# Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.

print(f"\n[grey50]{'%%%   Task 4: COUNT goods in "products"   ':%<{l}}[/grey50]")
# Смотри Les10-Django_Pr3 (1) (1).pdf, с. 10 -- ЗАДАЧА 18:
goods_group = (session.query(Category.name, func.count(Product.id))
               .join(Product.category).group_by(Category.name).all())
# print('/'* l, goods_group, '/'* l, sep="\n")
print_products(goods_group, "GOODS AMOUNT", col2="Category", col4="Amount")


""" %%%%%%%%   Task 5   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """
# Задача 5: Группировка с фильтрацией
# Отфильтруйте и выведите только те категории, в которых более одного продукта.

print(f"\n[grey50]{'%%%   Task 5: GROUP and HAVING for data in "products"   ':%<{l}}[/grey50]")
# Смотри Les10-Django_Pr3 (1) (1).pdf, с. 8 -- ЗАДАЧА 14:
goods_group_1 = (session.query(Category.name, func.count(Product.id))
                 .join(Product.category).group_by(Category.name)
                 .having(func.count(Product.id) > 1).all())
print_products(goods_group_1, f"Goods Amount more than 1", col2="Category", col4="Amount")




def main():
    absolute_path = __file__
    project_root = os.getcwd()  # Текущая рабочая директория (в PyCharm — корень проекта).
    relative_path = os.path.relpath(absolute_path, project_root)
    print(f"\nВыполнен код из файла: [medium_purple4]{relative_path}[/medium_purple4]."
          f"\n[white]{'':.<{l}}[/white]")

if __name__ == '__main__':
    main()
