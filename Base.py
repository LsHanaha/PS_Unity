# -*- coding: utf-8 -*-

import time
import sqlite3
from sqlite3 import Error

database = "/home/playps/bot/ps_unity.db"


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        with open("log.txt", 'a') as log:
            log.write(str(e))
    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        with open("log.txt", 'a') as log:
            log.write(str(e))


"""##################################################################################################################"""
"""___________________________________________________Games table____________________________________________________"""


def add_new_game(conn, game):
    """
    Add a new game in games
    :param conn:
    :param game: "name-must, description-must, genre-must, date-must, photo-must, price-must, links-variable
    :return: games id
    """
    sql = ''' INSERT INTO games (name, description, genre, date, photo, price, links)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, game)
    return cur.lastrowid


def update_game(conn, game):
    """
    Update information about a game in games
    :param conn:
    :param game: name-must, description-must, genre-must, date-must, photo-must, price-must, links-variable, id
    :return: None
    """
    sql = ''' UPDATE games
              SET name = ? ,
                  description = ? ,
                  genre = ? ,
                  date = ? ,
                  photo = ? ,
                  price = ? ,
                  links = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, game)


def delete_game(conn, game_id):
    """
    Delete a game by game id
    :param conn:  Connection to the SQLite database
    :param game_id: id of the task
    :return:
    """
    sql = 'DELETE FROM games WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (game_id,))


def delete_games(conn):
    """
    remove table top
    :return:
    """
    sql = "DROP TABLE games"
    cur = conn.cursor()
    cur.execute(sql)


def select_in_games(conn, needle):
    """
    search in games name
    :param conn:
    :param needle:
    :return:
    """
    sql = "SELECT * FROM games WHERE name LIKE '%'||?||'%'"
    cur = conn.cursor()
    res = cur.execute(sql, (needle,))
    return res


def select_all_games(conn):
    """
    Return all rows from games
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM games")

    rows = cur.fetchall()
    return rows


def select_game_name_by_id(conn, game_id):
    """
    Return a game by it's id in table games
    :param conn: the Connection object
    :param game_id:
    :return: game with id = game_id
    """
    cur = conn.cursor()
    cur.execute("SELECT name FROM games WHERE id=?", (game_id,))
    return "ggame0" + cur.fetchone()[0]


def select_game_cost_by_id(conn, game_id):
    """
    Return a game's cost by it's id in table games
    :param conn: the Connection object
    :param game_id:
    :return: game with id = game_id
    """
    cur = conn.cursor()
    cur.execute("SELECT price FROM games WHERE id=?", (game_id,))
    return cur.fetchone()[0]


def select_all_genres_from_games(conn):
    """
    Select all available genres from Base
    :param conn: the Connection object
    :param:
    :return: all available genres
    """
    cur = conn.cursor()
    cur.execute("SELECT genre FROM games")
    rows = cur.fetchall()
    res = []
    for row in rows:
        if ('genres' + row[0]) not in res:
            res.append('genres' + row[0])
    return res


def select_games_by_genre(conn, genre):
    """
    Select all games with genre="genre"
    :param conn: the Connection object
    :param genre:
    :return: all games witch is genre-type (in list - format sequence)
    """
    cur = conn.cursor()
    cur.execute("SELECT name FROM games WHERE genre=?", (genre,))
    rows = cur.fetchall()
    res = []
    for row in rows:
        res.append('ggames' + row[0])
    return res


def select_game_by_name(conn, name):
    """
    select game from games where name == name
    :param conn:
    :param name:
    :return res: game with name == name or None
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM games WHERE name=?", (name,))
    res = cur.fetchall()
    return res


def select_games_by_date(conn, year):
    """
    Select all games with date="year"
    :param conn: the Connection object
    :param year:
    :return: all games that released at year
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM games WHERE date=?", (year,))
    rows = cur.fetchall()
    return rows


"""##################################################################################################################"""
"""____________________________________________________Top table_____________________________________________________"""


def add_to_top(conn, rating):
    """
    Add position at top-20 table
    :param conn:
    :param rating:
    :return: None
    """
    sql = ''' INSERT INTO top (games_id)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (rating,))


def update_top(conn, new_pos):
    """
    Update top-list in table top
    :param conn:
    :param new_pos: games_id, id
    :return: None
    """
    sql = ''' UPDATE top
              SET games_id = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, new_pos)


def delete_position_top(conn, top_id):
    """
    Delete a game by game id
    :param conn:  Connection to the SQLite database
    :param top_id: id of the position
    :return:
    """
    sql = '''DELETE FROM top WHERE id=?'''
    cur = conn.cursor()
    cur.execute(sql, (top_id,))


def delete_top(conn):
    """
    remove table top
    :return:
    """
    sql = "DROP TABLE top"
    cur = conn.cursor()
    cur.execute(sql)


def select_all_from_top(conn):
    """
    Select all games id in top
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT games_id FROM top")
    rows = cur.fetchall()
    res = []
    for i in rows:
        res.append(i[0])
    return res


def select_from_top_by_pos(conn, pos):
    """
    Select game id from top
    :param conn: the Connection object
    :param pos:
    :return: game with id = top_id or blank list
    """
    cur = conn.cursor()
    cur.execute("SELECT games_id FROM top WHERE id=?", (pos,))
    try:
        return cur.fetchone()[0][1]
    except Exception:
        return []


"""##################################################################################################################"""
"""___________________________________________________Cart table_____________________________________________________"""


def add_to_cart(conn, chat_id):
    """
    Add new chat_id to cart
    :param conn:
    :param chat_id:
    :return: None
    """
    sql = ''' INSERT INTO cart (chat_id, games_id, time_add)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (chat_id, "", int(time.time() * 100)))


def update_cart(conn, data):
    """
    Update cart
    :param conn:
    :param data: chat_id, games_id, time_add
    :return: None
    """
    sql = ''' UPDATE cart
              SET games_id = ?,
                  time_add = ?
              WHERE chat_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)


def delete_cart(conn):
    """
    remove table
    :return:
    """
    sql = "DROP TABLE cart"
    cur = conn.cursor()
    cur.execute(sql)


def select_all_from_cart(conn):
    """
    select all positions in cart for each customer
    :param conn:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM cart")
    rows = cur.fetchall()
    return rows


def select_cart_for_chat_id(conn, chat_id):
    """
    Select all games in cart for customer
    :param conn: the Connection object
    :param chat_id:
    :return: game with id = top_id or blank list
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM cart WHERE chat_id=?", (chat_id,))
    return cur.fetchone()


"""##################################################################################################################"""
"""__________________________________________________Message table___________________________________________________"""


def add_message(conn, data):
    """
    Add new chat_id in Base
    :param conn:
    :param data:
    :return: None
    """
    sql = ''' INSERT INTO messages (chat_id, message_id_current)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, data)


def update_message(conn, data):
    """
    Update the last message_id for chat_id
    :param conn:
    :param data:
    :return: None
    """
    sql = ''' UPDATE messages
              SET message_id_current = ?
              WHERE chat_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)


def update_message_id_last_current(conn, data):
    """
    Update the last message_id for chat_id
    :param conn:
    :param data:
    :return: None
    """
    sql = ''' UPDATE messages
              SET   message_id_current = ?,
                    message_id_last = ?
              WHERE chat_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)


def update_message_last_command(conn, chat_id, command):
    """
    Update last command and time it was use for chat_id
    :param conn:
    :param chat_id:
    :param command:
    :return:
    """
    time_msg = int(time.time() * 100)
    sql = ''' UPDATE messages
              SET command = ?,
                  time_msg = ?
              WHERE chat_id = ?'''
    cur = conn.cursor()
    data = [command, time_msg, chat_id]
    cur.execute(sql, tuple(data))


def update_callback_data(conn, data):
    """
    Update last command in messages for double-click protection
    :param conn:
    :param data:
    :return:
    """
    sql = ''' UPDATE messages
              SET callback = ?
              WHERE chat_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, tuple(data))


def update_callback_now_data(conn, data):
    """
    add current command for button back
    :param conn:
    :param data:
    :return:
    """
    sql = ''' UPDATE messages
              SET callback_now = ?
              WHERE chat_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, tuple(data))


def update_callback_1_data(conn, data):
    """
    Implementation of button "back" - pre-pre-last command
    :param conn:
    :param data:
    :return:
    """
    sql = ''' UPDATE messages
              SET callback_1 = ?
              WHERE chat_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, tuple(data))


def update_callback_2_data(conn, data):
    """
    Implementation of button "back" - pre-pre-pre-last command
    :param conn:
    :param data:
    :return:
    """
    sql = ''' UPDATE messages
              SET callback_2 = ?
              WHERE chat_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, tuple(data))


def update_messages_flag(conn, data):
    """

    :param conn:
    :param data:
    :return:
    """
    sql = ''' UPDATE messages
              SET flag = ?
              WHERE chat_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)


def delete_all_messages(conn):
    """
    Delete all messages from table
    :param conn:  Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM messages'
    cur = conn.cursor()
    cur.execute(sql)


def delete_messages_table():
    """
    remove table
    :return:
    """
    conn = create_connection(database)
    sql = "DROP TABLE messages"
    cur = conn.cursor()
    cur.execute(sql)


def select_last_command(conn, chat_id):
    """
    Select last command and time from messages for chat_id
    :param conn:
    :param chat_id:
    :return: last command and time if exists or blank list
    """
    cur = conn.cursor()
    cur.execute("SELECT command, time_msg FROM messages Where chat_id=?", (chat_id,))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows
    else:
        return -1


def select_message_id_current(conn, chat_id):
    """
    Select current message_id for chat_id
    :param conn:
    :param chat_id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT message_id_current FROM messages Where chat_id=?", (chat_id,))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return 0


def select_message_id_last(conn, chat_id):
    """
    Select last message id for chat_id
    :param conn:
    :param chat_id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT message_id_last FROM messages Where chat_id=?", (chat_id,))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return 0


def select_callback(conn, chat_id):
    """
    :param conn:
    :param chat_id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT callback FROM messages Where chat_id=?", (chat_id,))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return -1


def select_callback_now(conn, chat_id):
    """
    :param conn:
    :param chat_id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT callback_now FROM messages Where chat_id=?", (chat_id,))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return -1


def select_callback_1(conn, chat_id):
    """
    :param conn:
    :param chat_id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT callback_1 FROM messages Where chat_id=?", (chat_id,))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return -1


def select_callback_2(conn, chat_id):
    """
    :param conn:
    :param chat_id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT callback_2 FROM messages Where chat_id=?", (chat_id,))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return -1


def select_messages_flag(conn, chat_id):
    """
    Flag uses for search and chat with developer. If flag == 1 - search, 2 - developer
    :param conn:
    :param chat_id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT flag FROM messages Where chat_id=?", (chat_id,))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return 0


def select_all_messages(conn):
    """
    Select all messages
    :param conn:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    return cur.fetchall()


"""##################################################################################################################"""
"""_____________________________________________________My ORM_______________________________________________________"""


def show_all_genres():
    conn = create_connection(database)
    with conn:
        res = select_all_genres_from_games(conn)
    return res


def show_games_by_genre(genre):
    conn = create_connection(database)
    with conn:
        res = select_games_by_genre(conn, genre)
        return res


def show_games_by_id(list_game):
    conn = create_connection(database)
    res = []
    with conn:
        for i in list_game:
            if '0' <= str(i) <= '99':
                res.append(select_game_name_by_id(conn, i))
    return res


def show_search_games(list_game):
    conn = create_connection(database)
    res = []
    with conn:
        for i in list_game:
            res.append("ggame0"+select_game_name_by_id(conn, int(i))[6:])
    return res


def show_games_cost_by_id(list_game):
    conn = create_connection(database)
    res = 0
    with conn:
        for i in list_game:
            if '0' <= i <= '99':
                res += (select_game_cost_by_id(conn, i))
    return res


def show_game_by_name(name):
    conn = create_connection(database)
    with conn:
        return select_game_by_name(conn, name)


def search_in_games(needle):
    conn = create_connection(database)
    with conn:
        request = select_in_games(conn, needle)
        res = []
        for i in request:
            res.append(str(i[0]))
        return res


def show_all_top():
    conn = create_connection(database)
    with conn:
        res = select_all_from_top(conn)
        return res


def delete_top_table():
    conn = create_connection(database)
    with conn:
        delete_top(conn)


def delete_games_table():
    conn = create_connection(database)
    with conn:
        delete_games(conn)

def add_new_chat_id(chat_id, message_id):
    conn = create_connection(database)
    with conn:
        add_message(conn, (chat_id, message_id))


def update_message_id_in_chat_id(chat_id, message_id):
    data = [str(message_id), str(chat_id)]
    conn = create_connection(database)
    with conn:
        update_message(conn, tuple(data))


def update_message_id_last_and_current(chat_id, message_id_current):
    conn = create_connection(database)
    with conn:
        message_id_last = select_message_id_current(conn, chat_id)
        if message_id_current > int(select_message_id_current(conn, chat_id)):
            update_message_id_last_current(conn, (message_id_current, message_id_last, chat_id))


def update_callback(chat_id, callback):
    conn = create_connection(database)
    with conn:
        temp = select_callback_now(conn, chat_id)
        temp1 = select_callback(conn, chat_id)
        temp2 = select_callback_1(conn, chat_id)
        if temp != -1:
            update_callback_data(conn, (temp, chat_id))
        if temp1 != -1:
            update_callback_1_data(conn, (temp1, chat_id))
        if temp2 != -1:
            update_callback_2_data(conn, (temp2, chat_id))
        update_callback_now_data(conn, (callback, chat_id))


def remove_callback(chat_id):
    conn = create_connection(database)
    with conn:
        update_callback_now_data(conn, (None, chat_id))
        temp2 = select_callback_2(conn, chat_id)
        temp1 = select_callback_1(conn, chat_id)
        if temp1 == -1:
            update_callback_data(conn, ("/start", chat_id))
        else:
            update_callback_data(conn, (temp1, chat_id))
        if temp2 == -1:
            update_callback_1_data(conn, (None, chat_id))
        else:
            update_callback_1_data(conn, (temp2, chat_id))
            update_callback_2_data(conn, (None, chat_id))


def show_all_messages():
    conn = create_connection(database)
    with conn:
        res = select_all_messages(conn)
        with open("log.txt", 'a') as log:
            for i in res:
                log.write(str(i))


def show_message_current(chat_id):
    conn = create_connection(database)
    with conn:
        return select_message_id_current(conn, str(chat_id))


def show_message_last(chat_id):
    conn = create_connection(database)
    with conn:
        return select_message_id_last(conn, chat_id)


def show_callback(chat_id):
    conn = create_connection(database)
    with conn:
        res = select_callback(conn, str(chat_id))
        if res is None or res == -1 or "Меню:" in res:
            return "/start"
        else:
            return res


def show_last_command_by_chat_id(chat_id):
    conn = create_connection(database)
    with conn:
        return select_last_command(conn, chat_id)


def show_messages_flag(chat_id):
    conn = create_connection(database)
    with conn:
        return select_messages_flag(conn, chat_id)


def update_flag_in_messages(chat_id, flag):
    conn = create_connection(database)
    with conn:
        update_messages_flag(conn, (flag, chat_id))


def delete_messages():
    conn = create_connection(database)
    with conn:
        delete_all_messages(conn)


def double_click_protection(chat_id,  command, message_id=None):
    now = int(time.time() * 100)
    conn = create_connection(database)
    i = show_last_command_by_chat_id(chat_id)
    with conn:
        if len(command) > 6:
            command = command[0:6]
        if i == -1:
            add_message(conn, (chat_id, message_id))
        elif i[0][1] is None:
            update_message_last_command(conn, chat_id, command)
            return 1
        elif now - i[0][1] < 100 and command == i[0][0]:
            update_message_last_command(conn, chat_id, command)
            return 0
        update_message_last_command(conn, chat_id, command)
        return 1


def new_customer(chat_id):
    conn = create_connection(database)
    with conn:
        add_to_cart(conn, chat_id)


def update_customers_cart(chat_id, game_id):
    """
    Обновляемя корзину покупателя. Попадаем сюда либо в случае добавления новых игр либо удаления игр из корзины.

    :param chat_id: Чат айди между ботом и пользователем
    :param game_id: Айди игры.
    :return:
    """
    conn = create_connection(database)
    temp = select_cart_for_chat_id(conn, chat_id)
    time_add = int(time.time() * 100)
    if temp is None:
        data = [game_id, time_add, chat_id]
        time_ = time_add
    else:
        game_id = temp[1] + "," + game_id
        data = [game_id, time_add, chat_id]
        time_ = temp[2]
    with conn:
        if time_add - time_ > 172800:
            update_cart(conn, tuple(["", time_add, chat_id]))
        update_cart(conn, tuple(data))


def show_cart():
    conn = create_connection(database)
    with conn:
        response = select_all_from_cart(conn)
        with open("log.txt", 'a') as log:
            for i in response:
                log.write(str(i))


def show_cart_for_chat_id(chat_id):
    conn = create_connection(database)
    with conn:
        response = select_cart_for_chat_id(conn, chat_id)
        if response is None:
            return [0, "", 0]
        return response


def delete_game_from_cart(chat_id, text):
    conn = create_connection(database)
    with conn:
        response = select_cart_for_chat_id(conn, chat_id)
        if len(text) == 2 and 'A' <= text[1] <= 'Z':
            text = text[0]
        try:
            game_pos_in_text = response[1].rindex(text)

            if game_pos_in_text == 0:
                temp = response[1][game_pos_in_text + 2:]
            else:
                temp = response[1][0:game_pos_in_text - 1] + response[1][game_pos_in_text + 2:]
            j = 0
            for c in temp:
                if c == ",":
                    j += 1
                else:
                    break
            if len(temp) == j:
                temp = ","
            else:
                temp = temp[j:]
            data = (temp, int(time.time() * 100), response[0])
            update_cart(conn, data)
        except Exception:
            pass


def clear_cart_for_chat_id(chat_id):
    conn = create_connection(database)
    time_add = int(time.time() * 100)
    with conn:
        update_cart(conn, tuple([",", time_add, chat_id]))

def delete_cart_table():
    conn = create_connection(database)
    with conn:
        delete_cart(conn)


"""##################################################################################################################"""


def create_tables():
    """
    creating (if needed) and filling db
    :return: None
    """
    sql_create_games_table = """ CREATE TABLE IF NOT EXISTS games (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        description text,
                                        genre text NOT NULL,
                                        date text NOT NULL,
                                        photo text NOT NULL,
                                        price integer NOT NULL,
                                        links text,
                                        tempgames1 text,
                                        tempgames2 text,
                                        tempgames3 text
                                    ); """

    sql_create_message_table = """ CREATE TABLE IF NOT EXISTS messages (
                                        chat_id text PRIMARY KEY NOT NULL,
                                        message_id_current text NOT NULL,
                                        message_id_last text,
                                        command text,
                                        time_msg integer,
                                        callback text,
                                        callback_now text,
                                        callback_1 text,
                                        callback_2 text,
                                        flag integer,
                                        tempmsg1 text,
                                        tempmsg2 text,
                                        tempmsg3 text
                                    ); """

    sql_create_top_table = """CREATE TABLE IF NOT EXISTS top (
                                    id integer PRIMARY KEY,
                                    games_id integer,
                                    temptop1 text,
                                    FOREIGN KEY (games_id) REFERENCES games (id)
                                ); """

    sql_create_cart_table = """ CREATE TABLE IF NOT EXISTS cart (
                                        chat_id integer PRIMARY KEY,
                                        games_id text,
                                        time_add integer,
                                        tempcart1 text,
                                        tempcart2 text,
                                        tempcart3 text
                                    ); """

    # create a database tables
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_games_table)
        create_table(conn, sql_create_top_table)
        create_table(conn, sql_create_cart_table)
        create_table(conn, sql_create_message_table)
    else:
        with open("log.txt", 'a') as log:
            log.write("Error! cannot create the database connection.")


def fill_games():
    conn = create_connection(database)
    with conn:
        try:
            delete_games(conn)
        except sqlite3.OperationalError:
            pass
        create_tables()
        games = (
                ('Anthem',                             'Anthem — это новая постапокалиптическая фантастическая игра от BioWare. В мире, заброшенном ещё при создании, человечество борется за выживание в диких условиях, таящих в себе множество опасностей.',                            'Экшен',            '2019',     'AgADAgADVaoxG5NfcEj2G4q8THxLVqqkOQ8ABE8_AAGRGJMChcCVBQABAg',   2500,     ''),
                ("Assassin's Creed Odyssey",           'Пройдите путь от изгоя до живой легенды: отправьтесь в далекое странствие, чтобы раскрыть тайны своего прошлого и изменить будущее Древней Греции.',                                                                               'Приключения',      '2018',     'AgADAgADQ6oxG4idMUpFQLyx7NDudNpGOQ8ABF7OEe53rIeQftYBAAEC',     2500,     ''),
                ("Assassin's Creed Origins",           'Раскройте тайны Древнего Египта и узнайте, как было создано Братство ассасинов.',                                                                                                                                                  'Приключения',      '2017',     'AgADAgADRKoxG4idMUobP-6e5a_p5J9H8w4ABE5dLaAU9TeNQgIGAAEC',     2500,     ''),
                ('Battlefield 1',                      'Cо всеми DLC. Battlefield 1 — шутер от первого лица. Действие игры разворачивается в ходе Первой мировой войны. В Battlefield 1 представлен широкий арсенал из различного оружия того времени.',                                   'Шутер',            '2016',     'AgADAgADwakxG9UYKEqwic6vMLTqa3bztw4ABN4fECDXjaQ07QgGAAEC',     2000,     ''),
                ('Battlefield 4',                      'Cо всеми DLC. Шутер от первого лица. Действие игры разворачивается в недалеком будущем.',                                                                                                                                          'Шутер',            '2012',     'AgADAgADQqoxG8L6aUiBIh7B4kNHjqZcXw8ABFbQCJkUCo4S-cECAAEC',     1800,     ''),
                ('Battlefield 5',                      'Участвуйте в крупнейшем военном конфликте. Играйте по сети в «Большие операции» и «Совместные бои», а также в «Военные истории» для одного игрока. Сражайтесь по всему земному шару.',                                             'Шутер',            '2018',     'AgADAgADRaoxG4idMUrYDOQHGnEk3OFROQ8ABJBc6rlRFlKYsNcBAAEC',     2500,     ''),
                ('Bloodborne GOTY',                    'Действие Bloodborne происходит в древнем городе Яхарнарме (Yharnarm). Годами люди прибывали в Яхарнарм в поисках помощи, но сейчас город стал проклятым местом, пораженным ужасной эпидемией.',                                    'Боевик',           '2015',     'AgADAgADR6oxG4idMUp7D7AUR7qLmOU8OQ8ABPHBMLdryiU_QdgBAAEC',     1300,     ''),
                ('Call of Duty: Black Ops 3',          'Действие Call of Duty: Black Ops 3 разворачивается в далеком будущем, в мире разрываемом войной. Стороны делят территории и ресурсы, а победа зависит о того, на чьей стороне технологическое превосходство.',                     'Шутер',            '2015',     'AgADAgADVaoxG4idMUqUAAEURfPvxPPeYDkPAAT3r2ofOtRZWeXXAQABAg',   2000,     ''),
                ('Call of Duty: Black Ops 4',          'Продолжение успешной серии Black Ops от команды Treyarch.',                                                                                                                                                                        'Шутер',            '2018',     'AgADAgADOaoxG4idMUofElZOl-agrFWUOQ8ABPx1TEzYwQskquYDAAEC',     2500,     ''),
                ('Call of Duty: WWII',                 'Call of Duty: WWII — шутер от первого лица, разработанный студией Sledgehammer Games. Действие игры разворачивается в ходе Второй мировой войны, а игроки берут на себя роль отважного отряда солдат.',                            'Шутер',            '2017',    'AgADAgADVqoxG4idMUrP6-RKXPT89buXOQ8ABPZ3CfqGtA1Ngt8DAAEC',      2500,     ''),
                ('Dark Souls 3 Deluxe',                'Deluxe-издание DARK SOULS™ III включает полную версию игры и сезонный пропуск, дающий доступ к дополнительным картам, боссам, противникам, новому оружию и броне.',                                                                'Боевик',           '2016',     'AgADAgADXqoxG4idMUri-e3_bHDhSvNcOQ8ABC4rzgJzpAJkcdcBAAEC',     2500,     ''),
                ('Darksiders 3',                       'В Darksiders III вы вернетесь на мертвую Землю в роли ЯРОСТИ, которая намерена найти и уничтожить Семь смертных грехов.',                                                                                                          'РПГ',              '2018',     'AgADAgADX6oxG4idMUpD7-j3pvq-pE5LXw8ABHrcxFpQBPVphw4BAAEC',     2400,     ''),
                ('Dead Cells',                         'В Dead Cells вы — подопытный алхимического эксперимента на проклятом острове, где все меняется и растет. Вы бессмертны, но беспомощны: чтобы передвигаться и сражаться, занимаете чужие тела...',                                  'Боевик',           '2018',     'AgADAgADWqoxG4idMUo9tAAB2lu_QyNDkzkPAAT2QorjZaZ4vALgAwABAg',   900,      ''),
                ('Detroit: Become Human',              'Детройт, 2038 год. Похожие на людей андроиды стали основной рабочей силой на планете. Вам предстоит управлять тремя андроидами, чтобы помочь им понять, кто же они на самом деле.',                                                'Боевик',           '2018',     'AgADAgADWaoxG4idMUrH32TkZwyuIIRJXw8ABLiyYkntGIi8mAsBAAEC',     2500,     ''),
                ('Devil May Cry 5',                    'компьютерная игра в жанре слэшер, разработанная и изданная японской компанией Capcom. Пятая игра в одноимённой серии и пятая же в хронологии.',                                                                                    'Экшен',            '2018',     'AgADAgADVqoxG5NfcEisaxL1ix5PqJQGUg8ABFa9QgxMSjvJLC8BAAEC',     2200,     ''),
                ('Diablo 3',                           'Diablo 3 - продолжение легендарной ролевой игры, разработанное компанией Blizzard Entertainment.',                                                                                                                                 'РПГ',              '2014',     'AgADAgADW6oxG4idMUp1DO6UDhB36K2cOQ8ABDO3AaJwxvD5ZdwDAAEC',     1300,     ''),
                ('Dishonored 2',                       'В игре Dishonored 2 вы снова окажетесь в роли ассасина со сверхъестественными способностями.',                                                                                                                                     'Боевик',           '2016',     'AgADAgADXKoxG4idMUqhLyAWvtzQJ1BrXw8ABE3rlfRjnMwLKAsBAAEC',     1700,     ''),
                ('Divinity: Original Sin II',          'Соберите отряд и отправляйтесь исследовать удивительный мир, в котором единственным ограничением на пути к божественности и спасению всего сущего станет ваше воображение.',                                                       'РПГ',              '2018',     'AgADAgADWKoxG4idMUpoJmmIoNQ2ETBiOQ8ABDwZNsZW2QXTYNcBAAEC',     2300,     ''),
                ('DOOM',                               'Злобные демоны, мощные пушки, стремительное передвижение — вот основа нового DOOM. Во время сражений вам не придётся прятаться или ждать пока восстановится здоровье.',                                                            'Шутер',            '2016',      'AgADAgADXaoxG4idMUqByaVainWBZWNvXw8ABHLgGVqg0d00BRABAAEC',    1300,     ''),
                ('F1 2018',                            'Укрепляйте свою репутацию как на трассе, так и за её пределами: к ключевым событиям вашей карьеры добавляются интервью в СМИ. Покажете ли вы себя сдержанным спортсменом или любителем громких заявлений?',                        'Гонки',            '2018',      'AgADAgADYKoxG4idMUqRwJlxheE6wORTXw8ABEXOFoVzgk9uMQ4BAAEC',    2400,     ''),
                ('Far Cry 5',                          'Добро пожаловать в Монтану - округ Хоуп - земли свободных и смелых, захваченные фанатиками Врат Эдема. Дайте отпор Иосифу Сиду и его сторонникам. Разожгите огонь сопротивления.',                                                 'Боевик',           '2018',      'AgADAgADYaoxG4idMUqsHhPUQMeAzMujOQ8ABO0amHKzwtHftuUDAAEC',    2500,     ''),
                ('Far Cry New Dawn',                   'Far Cry New Dawn — компьютерная игра в жанре шутера от первого лица со структурой открытого мира',                                                                                                                                 'Боевик',           '2019',      'AgADAgADU6oxG5NfcEg0ohmqN3KH6mRSOQ8ABGZNe7smPfGHFY0DAAEC',    1900,     ''),
                ('FIFA 18',                            'В FIFA 18, как и в других играх этой серии, игроки смогут принять участие в футбольном чемпионате, выбрав одну из многих команд или собрав собственную.',                                                                          'Спорт',            '2017',      'AgADAgADY6oxG4idMUoal0COdm41D3NGOQ8ABMw7WPKbN4rJ9dUBAAEC',    1400,     ''),
                ('FIFA 19',                            'Главная футбольная игра Мира',                                                                                                                                                                                                     'Спорт',            '2018',      'AgADAgADZKoxG4idMUomdWTpUZ74cm5aOQ8ABEBY0MjdPpm-5tcBAAEC',    2500,     ''),
                ('For Honor',                          'Побеждайте на полях сражений For Honor.',                                                                                                                                                                                          'Боевик',           '2017',     'AgADAgADYqoxG4idMUof0Yf6SHK_IpxOOQ8ABDcC9-znBtcX_dIBAAEC',     1300,     ''),
                ('God of War',                         'God of War — слэшер от третьего лица. Игра является перезапуском знаменитой серии God of War, рассказывающей о жестоком спартанском войне Кратосе, который перебил всех богов Олимпа и ввергнул мир в хаос.',                      'Боевик',           '2018',     'AgADAgADZaoxG4idMUqGhYZLsoHY-5aiOQ8ABMsUpYQ7wzuir-EDAAEC',     2500,     ''),
                ('Grand Theft Auto V (GTA 5)',         'Grand Theft Auto 5 — продолжение знаменитой серии GTA. В пятой части игроки вернуться в штат Сан-Андреас и знакомый всем город Лос-Сантос.',                                                                                       'Боевик',           '2014',     'AgADAgADZqoxG4idMUo_8PZkzc0lgMZQXw8ABJnNqxeNM4wCUQsBAAEC',     1300,     ''),
                ('Hitman 2. Издание Игра года',        'Путешествуйте по миру и выслеживайте свои цели в экзотических местах. От залитых солнцем улиц до темных и опасных тропических лесов, нигде нельзя спрятаться от Агента 47.',                                                       'Боевик',           '2018',     'AgADAgADZ6oxG4idMUor_TmV9v21FaH_9A4ABN0rFSsZgB12FhsEAAEC',     2700,     ''),
                ('Horizon: Zero Dawn',                 'Действие игры разворачивается в мире, в котором люди и роботы, эволюционировавшие в различных диких животных, живут в хрупкой гармонии.',                                                                                          'РПГ',              '2017',     'AgADAgADaKoxG4idMUoIK4LsPOl4k5WYOQ8ABHAZ8Q2keYqGhOEDAAEC',     1400,     ''),
                ('Injustice 2: Legendary Edition',     'Развивайте любимых героев вселенной DC в INJUSTICE 2 — лучшем файтинге 2017 года по версии IGN.',                                                                                                                                  'Файтинг',          '2018',     'AgADAgADaqoxG4idMUohhatH-gFuDn6dOQ8ABLNUGrVBDHCmCuUDAAEC',     2200,     ''),
                ('Kingdom Come: Deliverance',          'Вы – сын кузнеца, втянутый в водоворот гражданской войны. Отомстите за смерть своих близких и помогите отразить нападение захватчиков.',                                                                                           'РПГ',              '2018',     'AgADAgADa6oxG4idMUoNTTbNMYrpIFBOOQ8ABOcUUvt11gjk7dIBAAEC',     2200,     ''),
                ("Marvel's Spider-Man Расширенное издание", "В Marvel's Spider-Man вы будете играть за одного из самых культовых супергероев мира, мастера паутины, известного своими акробатическими способностями и талантом к импровизации.",                                           'Боевик',           '2019',     'AgADAgADeKoxG4idMUqa7yVMYtGlJ4GcOQ8ABNExtPPd5AxHWeEDAAEC',     2500,     ''),
                ('Metro Exodus',                       'Устрой декоммунизацию всему что стоит. Поглядывай по сторонам, читая надписи на стенах. Это Россия, детка.',                                                                                                                       'Боевик',           '2019',     'AgADAgADQ6oxG8L6aUjnQcoU04CLXlJOUw8ABASOD-vWx6voLzEBAAEC',     2500,     ''),
                ('Monster Hunter: World',              'Monster Hunter: World — это экшен с ролевыми элементами от студии Capcom. Очередная инсталляция в серии игр, в которых игроки берут на себя роли охотников за монстрами.',                                                         'Боевик',           '2018',     'AgADAgADbqoxG4idMUqxylAOGh7LisA_OQ8ABLIyFHOIgU-eRNQBAAEC',     1800,     ''),
                ('Mortal Kombat XL',                   'Сочетая в себе кинематографическую подачу беспрецедентного качества и обновленную игровую механику, Mortal Kombat X являет миру самую брутальную из всех Смертельных битв.',                                                       'Файтинг',          '2016',     'AgADAgADbaoxG4idMUr3bdrgUhRDipN7Xw8ABFVVVDxyosu4XQ8BAAEC',     2200,     ''),
                ('NBA 2K18',                           'NBA 2K18 - это баскетбольный спортивный симулятор, основанный на Национальной Баскетбольной Ассоциации (НБА).',                                                                                                                    'Спорт',            '2017',     'AgADAgADyakxG9UYKEr9s6gxzdhF4KVUOQ8ABGVCqbj17C_14NkBAAEC',     1500,     ''),
                ('NBA 2K19',                           'Вот уже 20 лет серия NBA 2K задает направление развития в спортивных играх — от лучших в своем классе графики и игрового процесса до захватывающих режимов игры и реалистичного открытого мира Neighborhood.',                     'Спорт',            '2018',     'AgADAgADb6oxG4idMUpgXYGH-bAULEbztw4ABEgCKsZzffgxSQUGAAEC',     2500,     ''),
                ('NHL 19',                             'В NHL 19 вы сможете играть на уличных катках, пройти путь от игр на пруду до профессиональных матчей в новых и уже знакомых режимах.',                                                                                             'Спорт',            '2018',     'AgADAgADcKoxG4idMUoR9CWDciEmRXZbXw8ABAS3b6KWTOVg-Q4BAAEC',     2500,     ''),
                ('Overwatch',                          'Сетевой шутер от первого лица, разработанный студией Blizzard Entertainment.',                                                                                                                                                     'Шутер',            '2016',     'AgADAgADcaoxG4idMUoBCCo30mnIuFRL8w4ABJLDGStxXCpo4QUGAAEC',     2050,     ''),
                ("Playerunknown's Battlegrounds (PUBG)", 'Обыграй, ограбь и обхитри противников, чтобы остаться единственным победителем в этой захватывающей игре, полной неожиданностей и волнующих моментов. ',                                                                         'Шутер',            '2018',     'AgADAgADcqoxG4idMUqTdkZYsu6uY4x6Xw8ABH7efhAp4OggTw0BAAEC',     1150,     ''),
                ('Red Dead Redemption 2',              'Игра Red Dead Redemption 2 от создателей GTA V и Red Dead Redemption – это грандиозное повествование о жизни в Америке на заре современной эпохи.',                                                                                'Приключения',      '2018',     'AgADAgADc6oxG4idMUobhbFh9dYNYuFDXw8ABH9e6hy8p7AV1gsBAAEC',     2500,     ''),
                ('Rocket League',                      'На ваш выбор - различные автомобили с огромными ракетными ускорителями, взлетающие в воздух, используйте их чтобы забивать голы, демонстрировать невероятные сейвы и даже крушить соперников на невероятных скоростях!',           'Спорт',            '2015',     'AgADAgADdKoxG4idMUq4Fd9c0K3TqYX_9A4ABEO0O3d6MztExhEEAAEC',     900,      ''),
                ('Shadow of the Colossus',             'Переиздание оригинальной Shadow of the Colossus.',                                                                                                                                                                                 'Приключения',      '2018',     'AgADAgADyqkxG9UYKEpQmV_Bs2bR8KFJXw8ABK-GoJEmq-1veQwBAAEC',     1400,     ''),
                ('Shadow of the Tomb Raider',          'Проникнитесь судьбоносной историей становления Лары Крофт, легендарной расхитительницы гробниц. Спасая мир от гибели, она пройдет немало испытаний и станет настоящей расхитительницей гробниц.',                                  'Боевик',           '2018',     'AgADAgADd6oxG4idMUp68ru6u76iR-9OXw8ABMgbyMcZTWmV9A0BAAEC',     2400,     ''),
                ('SoulCalibur 6',                      'Новая игра в серии SOULCALIBUR! Испытайте новейшую игровую механику с захватывающей графикой, которую вы когда-либо видели!',                                                                                                      'Файтинг',          '2018',     'AgADAgADdaoxG4idMUrKNs0R7LgMP0s-8w4ABEJYW1IcBj1qug8GAAEC',     2500,     ''),
                ('Star Wars: Battlefront 2',           'Star Wars: Battlefront II — шутер от первого лица. Игра основана на вселенной Звездных Войн, в которой силы повстанцев и Империи ведут войны на различных планетах.',                                                              'Боевик',           '2018',     'AgADAgADRqoxG4idMUqg6EcMieU7viw68w4ABPOp8rC42_AC1AABBgABAg',   1000,     ''),
                ('Street Fighter 5 - Arcade Edition',  'Участвуйте в напряженных боях один на один в Street Fighter V — Arcade Edition! Выбирайте из 28 персонажей, каждый из которых обладает собственной историей и уникальными тренировочными испытаниями.',                            'Файтинг',          '2016',     'AgADAgADdqoxG4idMUoDpR4of8lXiatPXw8ABIYJ4FQyFFKWohABAAEC',     800,      ''),
                ('Titanfall 2',                        'Фантастический шутер от первого лица с элементами симулятора меха, разработанный Respawn Entertainment.',                                                                                                                          'Шутер',            '2016',     'AgADAgADRKoxG8L6aUjvsehme8nud1idOQ8ABAx3IwABEL0uL--iBQABAg',   1400,     ''),
                ('The Crew 2',                         'Ворвитесь в мир моторного спорта США. Лидируйте в состязаниях на суше, на море и в небе. Наслаждайтесь азартом американских моторных состязаний в захватывающем открытом мире The Crew 2.',                                        'Гонки',            '2018',     'AgADAgADV6oxG4idMUryGiAu0O3W4Cbitw4ABLdpnqR1PzIeOAoGAAEC',     2500,     ''),
                ('The Last Of Us',                     'Сюжет берет начало в Америке, спустя 20 лет после биологической катастрофы, превратившей большую часть людей в кровожадных мутантов. Герои отправляются в опасное приключение, чтобы добыть лекарство от страшного вируса.',       'Экшен',            '2014',     'AgADAgADeaoxG4idMUq4UC_ZyT_oHJ8-OQ8ABA1_Y1wnfs39MNMBAAEC',     900,      ''),
                ('The Witcher 3: Wild Hunt',           'Wild Hunt рассказывает историю Геральта из Ривии, ведьмака и охотника на монстров, отправившегося в опасное приключение, чтобы остановить кошмарные легионы, известные как Дикая Охота (Wild Hunt).',                              'РПГ',              '2015',     'AgADAgADfaoxG4idMUp7dAKpSTPfqlphXw8ABC4ObUaTBPremQUBAAEC',     1600,     ''),
                ("Tom Clancy's: Rainbow Six Siege\nAdvanced Edition", 'Rainbow Six Осада выводит жаркие перестрелки и тактическое планирование на новый уровень. Cоберите свою команду из лучших оперативников и вступите в бескомпромиссный бой.',                                        'Боевик',           '2018',     'AgADAgADy6kxG9UYKEpHSCqX3mgJhFVgXw8ABCaQy_dMLT2nwwwBAAEC',     1500,     ''),
                ('Tom Clancy\'s The Division 2',       'События происходят через 6 месяцев после своего предшественника в Вашингтоне, округ Колумбия, в котором разразилась гражданская война между выжившими и злодейскими группами мародеров',                                           'Боевик',           '2019',     'AgADAgADVKoxG5NfcEhn8reoEj4ujvVaOQ8ABOUzkEpvqANCLowDAAEC',     2500,     ''),
                ('UFC 3',                              'Все действия бойца с высочайшей точностью воссоздают реальность ощущений. Игрокам придётся поднимать шум вокруг боёв, привлекать фанатов, платить за тренировки и соперничать с другими бойцами.',                                 'Файтинг',          '2018',     'AgADAgADeqoxG4idMUpG-T-KULPO9z54Xw8ABOq1yccyng99hQgBAAEC',     2200,     ''),
                ('Uncharted 4: A Thief\'s End',        'Сюжет Uncharted 4: A Thief\'s End рассказывает об искателе приключений, Нейтане Дрейке, который должен отыскать легендарное пиратское сокровище.',                                                                                 'Приключения',      '2016',     'AgADAgADe6oxG4idMUrVtzaeEpvZCIbmtw4ABKzjp8A0_zDQiQYGAAEC',     800,      ''),
                ('Until Dawn',                         'Восемь друзей вернулись в уединенную горную хижину, где ровно год назад исчезли двое их товарищей. А все начиналось так хорошо...',                                                                                                'Экшен',            '2015',     'AgADAgADfKoxG4idMUrxgNab3l9BNUHltw4ABKrPwA9oRGrYzAMGAAEC',     800,      ''),
                ('WRC 7 FIA World Rally Championship', 'Пройдите 13 ралли и 52 спецучастка Чемпионата мира по ралли FIA. Выступите в роли гонщиков чемпионата за рулем их машин: Hyundai, Toyota, Citroën и Ford. Все автомобили повторяют свои аналоги. ',                                'Гонки',            '2017',     'AgADAgADfqoxG4idMUqRuIpurQNz55NUXw8ABCwi5KS0yxG6UQ4BAAEC',     2400,     ''),
                ('WWE 2K19',                           'Крупнейшая серия игр о профессиональном рестлинге возвращается вместе с игрой WWE 2K19, в которой вас ждет не только борец-суперзвезда с обложки AJ Styles, но и множество героев и легенд WWE и NXT!',                            'Файтинг',          '2018',     'AgADAgADf6oxG4idMUpysm2lUa9Yv_Tntw4ABCXxY0i0XLXmjQUGAAEC',     2600,     '')
                )
                # ('Name', 'Description', 'genre', 'date', 'photos/', 1000, ''),
        i = 1
        for game in games:
            add_new_game(conn, game)


def fill_top():
    conn = create_connection(database)
    with conn:
        try:
            delete_top(conn)
        except sqlite3.OperationalError:
            pass
        create_tables()
        tops = (1,
                2,
                3,
                6,
                9,
                14,
                15,
                22,
                24,
                26,
                27,
                28,
                32,
                33,
                34,
                37,
                38,
                39,
                41,
                58)
        for i in tops:
            add_to_top(conn, i)


def start():
    conn = create_connection(database)
    with conn:
        create_tables(conn)