# Nagashbayev Al-Farabi
''' --------------------------------------------------------------------------------------------------
    Homework 1. 12-05-2025
------------------------------------------------------------------------------------------------------ '''

from flask import Flask, render_template

app = Flask(__name__)


# Task 2.2 - Создание базового Flask-приложения:
@app.route('/')
def home():
    return render_template('hw01-12_05-home.html')


# Task 2.3 - Расширение функциональности + 2.4 - Запуск и тестирование приложения:
@app.route('/user/<string:username>')
def get_username(username):
    return render_template('hw01-12_05-username.html', username=username)
    # return f'<h2>Hello, {username}!</h2>'



if __name__ == '__main__':
    app.run(debug=True)