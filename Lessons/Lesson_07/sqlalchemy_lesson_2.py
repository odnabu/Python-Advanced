from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import aliased
from tabulate import tabulate
import os

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

engine = create_engine('sqlite:///example_Les07_L8.db')
Session = sessionmaker(bind=engine)
session = Session()

if os.path.exists("example_Les07_L8.db"):
    os.remove("example_Les07_L8.db")

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

new_user = User(name="Alice", age=30)

session.add(new_user)
session.commit()

# Добавление записей
session.add_all([User(name='Bob', age=22), User(name='David', age=27),
User(name='Alice', age=30), User(name='Ann', age=17), User(name='Ann', age=27)])
session.commit()

#Read data
user = session.get(User, 1)
print(user.name, user.age)

#filter
print('\nФильтрация по имени Alice')
users = session.query(User).filter(User.name ==
                                   "Alice").all()
for user in users:
    print(user.id, user.name)

# Changing parameters
user = session.get(User, 1)
if user:
    user.age = 35  # Изменяем возраст
    session.commit()

user = session.get(User, 1)
print(user.id, user.name, user.age)

# user delete
user = session.get(User, 1)
if user:
    session.delete(user)
    session.commit()
    print(f"User with id {user.id} deleted")
else:
    print("User with id 1 isn't found")

query = session.query(User)
print('\nСодержание query:')
print(f'{query}\n')
for user in query.all():
    print(user.name, user.age)

print('\nПостроение запроса для выборки всех пользователей')
users = session.query(User).all()
print()
for user in users:
    print(user.name, user.age)

print('\nвозвращает первый объект из результата запроса или None, если результат пуст'
      'возвращает первый объект результата сортировки, если она была')
user = session.query(User).first()
print(user.id, user.name)

print('\nвозвращает ровно один объект: если в результате'
      'нет объектов или их более одного, генерирует'
      'исключение. Это пример, как исключать ошибки.')
user = session.query(User).filter(User.id == 3).one()
print(user.name)

print('\nвозвращает один объект или None, если объектов нет.'
      'Если объектов более одного, генерирует исключение')
user = session.query(User).filter(User.id == 3).one_or_none()
print(user.name)

# Фильтрация: выборка пользователей старше 25 лет
users = session.query(User).filter(User.age > 25).all()
print('\n# Фильтрация: выборка пользователей старше 25 лет')
for user in users:
    print(user.id, user.name, user.age)

print('\nПоиск пользователей, чье имя начинается на "A"')
users = session.query(User).filter(User.name.like('A%')).all()
for user in users:
    print(user.id, user.name)

print('\nПоиск пользователей с ID между 2 и 4')
users = session.query(User).filter(User.id.between(2, 4)).all()
for user in users:
    print(user.id, user.name)

print('\nПоиск пользователей, чьи имена находятся в списке')
names = ["Alice", "Bob"]
users = session.query(User).filter(User.name.in_(names)).all()
for user in users:
    print(user.id, user.name)

from sqlalchemy import and_, or_, not_
print('\nand_, or_, not_ необходимо дополнительно импортировать! from sqlalchemy import and_, or_, not_ ')
print('Выборка пользователей старше 20 лет и младше 23 лет:')
users = session.query(User).filter(and_(User.age > 20, User.age < 23)).all()
# альтернативный вариант:  Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
for user in users:
    print(user.id, user.name, user.age)

print('\nВыборка пользователей старше 30 или с именем David')
users = session.query(User).filter(or_(User.age > 30, User.name == 'David')).all()
for user in users:
    print(user.id, user.name, user.age)

print('\nВыборка пользователей не с именем David')
users = session.query(User).filter(not_(User.name == 'David')).all()
for user in users:
    print(user.id, user.name, user.age)

print('\nСортировка пользователей по возрасту от меньшего к большему')
users = session.query(User).order_by(User.age).all()
for user in users:
 print(user.id, user.name, user.age)

print('\nСортировка пользователей по возрасту от большего к меньшему')
from sqlalchemy import desc
users = session.query(User).order_by(desc(User.age)).all()
for user in users:
 print(user.id, user.name, user.age)

print('\nСортировка пользователей по возрасту от большего к меньшему и по имени по алфавиту')
users = session.query(User).order_by(desc(User.age), User.name).all()
for user in users:
 print(user.id, user.name, user.age)

print('\nСуммирование возрастов пользователей, группировка по именам')
total_ages = session.query(User.name,
func.sum(User.age)).group_by(User.name).all()
print(total_ages)

print('\nПодсчет количества пользователей в каждой возрастной группе')
age_groups = session.query(User.age,
func.count(User.id)).group_by(User.age).all()
print(age_groups)

print('\nИзвлекает первый столбец первой строки из результата SQL запроса'
      ' Возвращает None, если запрос не возвращает результатов')
total_count = session.query(func.count(User.id)).scalar()
print("Users count:", total_count)

# надо импортировать from sqlalchemy.orm import aliased
# Элиас (или псевдоним) в SQLAlchemy определяется с помощью функции aliased()
user_alias = aliased(User, name='user_alias')

# # Присвоение алиаса выражению подсчета количества пользователей в каждой возрастной группе
# age_groups = session.query(User.age,
#                            func.count(User.id).label('total_users')).group_by(User.age).all()

# Тот же запрос, но с обращением к таблице через алиас
age_groups = session.query(user_alias.age,
                           func.count(user_alias.id).label('total_users')).group_by(user_alias.age).all()


# Теперь можно обращаться к присвоенному имени
print()
for group in age_groups:
    print(group.age, group.total_users)

print('\nПодсчет количества пользователей в каждой возрастной группе и исключение групп с количеством меньше двух')
age_groups = session.query(
    User.age,
    func.count(User.id).label('count_users')
).group_by(User.age).having(func.count(User.id) > 1).all()
print(age_groups)

print('\nПодзапрос для вычисления среднего возраста сохраняем в переменную')
average_age_subquery = session.query(func.avg(User.age).label('average_age')).scalar_subquery()
# Основной запрос, использующий подзапрос для фильтрации пользователей
users = session.query(User).filter(User.age > average_age_subquery).all()
# Выполним подзапрос отдельно для проверки результата
print(f"Average age is {session.query(average_age_subquery).scalar()}")
# Выведем отобранные данные
for user in users:
    print(user.id, user.name, user.age)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String)
    user = relationship("User", back_populates="addresses")


User.addresses = relationship("Address", order_by=Address.id, back_populates="user")
# Создание её в базе данных и заполнение данными
Base.metadata.create_all(bind=engine)
session.add_all([Address(user_id=1, description='New York'),
                 Address(user_id=2, description='London'),
                 Address(user_id=4, description='London')])
session.commit()

print('\nПрисоединение таблицы адресов к таблице пользователей с помощью Inner Join')
users = session.query(User).join(Address).all()
# Проверка выборки
for user in users:
    print(user.id, user.name, user.age)
    for address in user.addresses:
        print("Address:", address.id, address.description)

print('\nПрисоединение таблицы адресов к таблице пользователей с помощью Left Outer Join')
users = session.query(User).outerjoin(Address).all()
# Проверка выборки
for user in users:
    print(user.id, user.name, user.age)
    for address in user.addresses:
        print("Address:", address.id, address.description)

print('\nПрисоединение таблицы адресов к таблице пользователей с помощью Left Outer Join')
users = session.query(User).outerjoin(Address).all()

# Формируем таблицу для вывода
table = []
for user in users:
    if user.addresses:
        for address in user.addresses:
            table.append([user.id, user.name, user.age, address.id, address.description])
    else:
        table.append([user.id, user.name, user.age, None, None])

# Печатаем в виде таблицы
headers = ["User ID", "Name", "Age", "Address ID", "Address Description"]
print(tabulate(table, headers=headers, tablefmt="grid"))

print('\nНайти всех пользователей, которые живут в одном городе с другими пользователями '
      'при помощи SELF JOIN (таблица внутри самой себя).')
from sqlalchemy.orm import aliased

address_alias1 = aliased(Address)
address_alias2 = aliased(Address)
users = session.query(address_alias1.user_id, address_alias2.user_id). \
    join(address_alias2, address_alias1.description == address_alias2.description).filter(address_alias1.user_id !=
                                            address_alias2.user_id).all()
print(users)
