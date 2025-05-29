# Müller Alexander
""" --------------------------------------------------------------------------------------------------
    Lesson 10. 27-05-2025
    Flask Practice 03: SQLAlchemy.
------------------------------------------------------------------------------------------------------ """

print('.' * 80)


""" ______  Task 1  ______________________________________________________________________________________________ """
# Задача 1: Поиск пользователя по имени.
# Напишите запрос, который возвращает пользователя с конкретным именем (например, "Alice").

#  \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\      СИНТАКСИЧЕСКИЕ ЗАПРОСЫ     ///////////////////////////////////

user_name = "Alice"
user = session.query(User).filter(User.name == user_name).first()
if user:
    print(f"Found user: {user.name}")
else:
    print("User not found.")

""" ______  Task 2  ______________________________________________________________________________________________ """
# Задача 2: Вывод пользователей с определённым возрастом.
# Напишите запрос для вывода всех пользователей, возраст которых больше 20 лет.

users = session.query(User).filter(User.age > 20).all()
print('Users older than 20 years:')
if users:
    print(f"Found users: {len(users)}")
    for user in users:
        print(user.name)
else:
    print("Users not found.")


""" ______  Task 3  ______________________________________________________________________________________________ """
# Задача 3: Обновление данных пользователя.
# Допустим, вы хотите обновить возраст пользователя "Bob" до 25 лет. Напишите запрос для обновления данных.

user_name = "Bob"
new_age = 25
user = session.query(User).filter(User.name == user_name).first()
if user:
    user.age = new_age
    session.commit()
    print(f"Updated {user.name}'s age to {new_age}.")
else:
    print("User not found.")


""" ______  Task 4  ______________________________________________________________________________________________ """
# Задача 4: Вывод пользователей моложе 30 лет.
# Напишите запрос для вывода всех пользователей, возраст которых меньше 30 лет. Выведите их имена и возраст.

users = session.query(User).filter(User.age < 30).all()     # Выбираем (селектим) либо ВСЕХ, как тут, либо
                                                            # можно выбрать только 2 колонки User.name, User.age.
print('Users younger than 30 years:')
if users:
    print(f"Found users: {len(users)}")
    for user in users:
        print(f"User: {user.name}, Age: {user.age}")
else:
    print("Users not found.")


""" ______  Task 5  ______________________________________________________________________________________________ """
# Задача 5: Добавление пользователя.
# Напишите запрос, который добавляет пользователя с именем "Charlie".

new_user = User(name="Charlie", age=40)
session.add(new_user)
session.commit()
print(f"Created new user: {new_user.name}")


""" ______  Task 6  ______________________________________________________________________________________________ """
# Задача 6: Удаление пользователя.
# Напишите запрос, который удаляет пользователя с определённым именем "Charlie". Выведите информацию о том, был ли он удален.

user_name = "Charlie"
user_to_delete = session.query(User).filter(User.name == user_name).first()
if user_to_delete:
    session.delete(user_to_delete)
    session.commit()
    print(f"Deleted user: {user_to_delete.name}")
else:
    print("User not found.")


""" ______  Task 7  ______________________________________________________________________________________________ """
# Задача 7: Сортировка пользователей по возрасту.
# Создайте запрос, который выводит всех пользователей, отсортированных по возрасту в порядке убывания.

sorted_users = session.query(User.name, User.age).order_by(User.age.desc()).all()   # или так: desc(User.age)
print(f"Users sorted by age descending: ")
if sorted_users:
    for name, age in sorted_users:
        print(f'User: {name}, Age: {age}')


""" ______  Task 8  ______________________________________________________________________________________________ """
# Задача 8: Вывод пользователей с ограничением количества.
# Напишите запрос, который выводит первые 4 пользователя, отсортированных по имени в алфавитном порядке.

limited_users = session.query(User.name).order_by(User.name.desc()).limit(4).all()   # или так: desc(User.age)
print("First 4 users alphabetically: ")
for name in limited_users:
    print(name)


""" ______  Task 9  ______________________________________________________________________________________________ """
# Задача 9: Обновление данных пользователя по ID.
# Напишите запрос для обновления данных пользователя, используя его id.
# Предположим, нужно обновить возраст пользователя с id равным 5 до 35 лет.
# Напишите функцию, которая у пользователя с арг id меняет возраст пользователя на аргумент new_age.

# ___ 1-st Variant __________________
user_id = 5
new_age = 49
user = session.get(User, user_id)
if user:
    user.age = new_age
    session.commit()
    print(f"Updated {user.name}'s age updated to {new_age}.")
else:
    print("User not found.")

# ___ 2-nd Variant __________________
def age_update(id, new_age):
    user = session.get(User, id)
    if user:
        user.age = new_age
        session.commit()
        return f"Updated {user.name}'s age updated to {new_age}."
    else:
        return f"User not found."

updated_user = age_update(5, 49)


""" ______  Task 10  ______________________________________________________________________________________________ """
# Задача 10: Проверка существования пользователя.
# Напишите запрос, который проверяет, существует ли пользователь с заданным name.
# Проверьте наличие пользователя с name равным "Charlie".

# ___ 1-st Variant __________________ --> Dima
user_name = "Charlie"
user = session.query(User).filter(User.name == user_name).first()

# ___ 2-nd Variant __________________
user_name = "Charlie"
# Подзапрос в запросе:
sub_query = session.query(User).filter_by(name=user_name).exists()      # .exists() возвращает True/False.
exists = session.query(sub_query).scalar()                              # .scalar() преобразует в булевый тип.
if exists:
    print(f"User with name {user_name} already exists.")
else:
    print(f"NO user found with that name.")


""" ______  Task 11  ______________________________________________________________________________________________ """
# Задача 11: Среднее значение возрастов.
# Напишите запрос, который находит средний возраст всех пользователей, и выведите результат.

# +++++++++++++++++++++++++++++
from sqlalchemy import funk
# +++++++++++++++++++++++++++++

result = session.query(func.avg(User.age)).scalar()
print(f"Average age: {result}.")


""" ______  Task 12  ______________________________________________________________________________________________ """
# Задача 12: Максимальный и минимальный возраст.
# Создайте запрос, который найдет максимальный и минимальный возраст среди пользователей.
# Используйте функции func.max() и func.min().

# +++++++++++++++++++++++++++++
from sqlalchemy import funk
# +++++++++++++++++++++++++++++

# ___ 1-st Variant __________________
max_age = session.query(func.max(User.age)).scalar()
min_age = session.query(func.min(User.age)).scalar()
print(f"Max age: {max_age}.")
print(f"Min age: {min_age}.")

# ___ 2-nd Variant __________________
min_max_age = session.query(
    func.min(User.age),
    func.max(User.age)
).one()
print(f"Минимальный возраст: {min_max_age[0]}")
print(f"Максимальный возраст: {min_max_age[1]}")


""" ______  Task 13  ______________________________________________________________________________________________ """
# Задача 13: Группировка пользователей по возрасту.
# Напишите запрос, который группирует пользователей по возрасту и подсчитывает количество пользователей
# в каждой возрастной группе.

# +++++++++++++++++++++++++++++
from sqlalchemy import funk
# +++++++++++++++++++++++++++++

age_groups = session.query(User.age, func.count(User.id)).group_by(User.age).all()
for age, count in age_groups:
    print(f"Age: {age}, Count: {count}")



""" ___________________________________  Review of previously covered material  ___________________________________ """

""" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%___________   ---   __________%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """


""" __________ --- __________ """
#       ●
# ___ EXAMPLE __________________________________________________
# ___ END of Example __________________________________________________


""" ______  Task 1  ______________________________________________________________________________________________ """
#





