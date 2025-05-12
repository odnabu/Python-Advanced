# Nagashbayev Al-Farabi

from flask import Flask, request
import uuid
app = Flask(__name__)


# @app.route('/')
# In browser, you should change address to http://127.0.0.1:5000/home to updating:
@app.route('/home')
def hello_world():  # put application's code here
    return '<h1>Hello World with FRAMEWORKS!</h1>'

# -----------------------------------------------
# In browser, you should change address to http://127.0.0.1:5001/profile/Olga to updating:
# @app.route('/profile/<string:username>')
# def get_profile(username):  # put application's code here
#     return f'<h2>My profile username: {username}<h2>'

# -----------------------------------------------
# In browser, you should change address to http://127.0.0.1:5001/profile_id/2002 to updating:
@app.route('/profile_id/<int:user_id>')       # for user ID.
def get_profile(user_id):  # put application's code here
    return f'<h2>My profile user_id: {user_id}<h2>'

# -----------------------------------------------
# In browser, you should change address to http://127.0.0.1:5001/profile_uuid/1976 to updating:
@app.route('/profile_uuid/<uuid:user_uuid>')       # for user ID.
def get_profile_uuid(user_uuid):  # put application's code here
    print(uuid.uuid4())
    return f'<h2>My profile user_uuid: {user_uuid}! Try next: {uuid.uuid4()}<h2>'
# Для генерации uuid нужно использовать библиотеку в Питоне.

# -----------------------------------------------
@app.route('/number/<float:number>')
def get_number(number):
    typ_numb = str(type(number))
    print(typ_numb)
    return f'<h1>Number: {number}</h1>\nType: {typ_numb}'

# -----------------------------------------------
@app.route('/square/<int:number>', methods=['GET', 'POST'])
def get_square(number):
    squared_numb = number * number
    return f'<h1>Squared number: {squared_numb}</h1>'

# -----------------------------------------------
@app.route('/send_password', methods=['POST'])
def get_password():
    password = request.form.get('password')
    print("Password: ", password)
    return f'This is secret password: "{password}"'


if __name__ == '__main__':
    # app.run()
    app.run(port=5001,debug=True)

# host - сервер.
# port - порт, на котором слушает все запросы.
# debug - этап дебага Video 1, 1:23:00.
# load_dotenv - адрес.

