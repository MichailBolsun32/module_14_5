import sqlite3

# connection = sqlite3.connect('products.db')
# cursor = connection.cursor()

#initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:
    # id - целое число, первичный ключ
    # username - текст (не пустой)
    # email - текст (не пустой)
    # age - целое число (не пустой)
    # balance - целое число (не пустой)

def initiate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')

    connection.commit()
    connection.close()


#add_user(username, email, age), которая принимает: имя пользователя, почту и возраст.
# Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
# Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.
# is_included(username) принимает имя пользователя и возвращает True,
# если такой пользователь есть в таблице Users, в противном случае False.
# Для получения записей используйте SQL запрос.

def is_include(username_):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username=?', (username_,))

    if check_user.fetchone() is None:
        connection.close()
        return True
    else:
        connection.close()
        return False


def add_user(username_, email, age):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (username_, email, age, 1000))

    connection.commit()
    connection.close()


# get_all_products, которая возвращает все записи из таблицы Products,
# полученные при помощи SQL запроса.

def get_all_products():
    initiate_db()
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    connection.commit()
    connection.close()
    return products

# initiate_db()
# заполнили таблицу
# for i in range(4):
#     cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
#                     (f'Продукт {i + 1}', f'Описание {i + 1}', f'{(i + 1) * 100}'))
# connection.commit()
# connection.close()