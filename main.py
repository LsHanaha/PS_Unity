#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import requests
import telebot
import time
import re
import logging
from telebot import types
from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import json
import Base
from flask import Flask


bot = telebot.TeleBot("777566365:AAG3bkEb6MYGaJpIZmk-JaBwHYNwk-y15ek", threaded=False)

app = Flask(__name__)
sslify = SSLify(app) # Настраиваем шифрование

# https://api.telegram.org/bot777566365:AAG3bkEb6MYGaJpIZmk-JaBwHYNwk-y15ek/setWebhook?url=playps.pythonanywhere.com/
# 777566365:AAG3bkEb6MYGaJpIZmk-JaBwHYNwk-y15ek Включаем Веб-хук


@app.route('/', methods=["POST"])
def telegram_webhook():
    bot.remove_webhook()
    bot.set_webhook("https://playps.pythonanywhere.com/777566365:AAG3bkEb6MYGaJpIZmk-JaBwHYNwk-y15ek", max_connections=1)
    return "OK"


@app.route('/777566365:AAG3bkEb6MYGaJpIZmk-JaBwHYNwk-y15ek', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


"""#################################################################################################################"""

def show_start(message):
    chat_id = message.chat.id
    message_id = message.message_id
    text = message.text
    if Base.double_click_protection(chat_id, text, message_id):
        clear_screen(chat_id, Base.show_message_current(chat_id), message_id, text)
        bot.send_photo(chat_id, photo="AgADAgADtKkxG9UYKEoiplqHWQio_Qt1Xw8ABMNdi6kvvEL52QwBAAEC",
                       caption="<b>Привет!</b>\nЯ продам тебе игру на PS4 "
                       "\U0001F3AE дешевле, чем ты ожидаешь! \nУ меня всегда -40!\n", parse_mode="HTML")
        if Base.show_cart_for_chat_id(chat_id)[0] == 0:
            Base.new_customer(chat_id)
        show_menu(chat_id, 1)


def show_menu(chat_id, flag):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    if flag == 1:  # Находимся в основном меню
        back = types.InlineKeyboardButton('Жанры \U0001F4D6', callback_data="menu_жанр")
    else:
        back = types.InlineKeyboardButton('\U0001F448 Назад', callback_data=Base.show_callback(chat_id) + "%^")
    if flag == 3:  # Находимся в корзине
        top = types.InlineKeyboardButton('Жанры \U0001F4D6', callback_data="menu_жанр")
        cart = types.InlineKeyboardButton('\U0001F3C6 Топ 20 \U0001F3C6', callback_data="menu_топ")
    else:
        top = types.InlineKeyboardButton('\U0001F3C6 Топ 20 \U0001F3C6', callback_data="menu_топ")
        cart = types.InlineKeyboardButton('\U0001F6D2 Корзина', callback_data="menu_корзина")
    search = types.InlineKeyboardButton('\U0001F50D Поиск', callback_data="menu_поиск")
    if flag == 2:  # Работа с разработчиком
        connect = types.InlineKeyboardButton('Завершить связь с разработчиком \U0000274C',
                                             callback_data="/start")
    else:
        connect = types.InlineKeyboardButton('Связь с разработчиком \U0001F528', callback_data="menu_разработчик")
    if flag == 4:  # Находимся в топе
        top = types.InlineKeyboardButton('Жанры \U0001F4D6', callback_data="menu_жанр")
    keyboard.row(back, top, cart)
    keyboard.row(search)
    keyboard.row(connect)

    bot.send_message(chat_id, "Меню:                                             \U0000200C",
                     reply_markup=keyboard)


def generate_inline_buttons(chat_id, text, *args):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    inf = []
    for i in args:
        inf.append(types.InlineKeyboardButton(text=i[6:], callback_data=i))
    keyboard.add(*inf)
    bot.send_message(chat_id, text, reply_markup=keyboard, disable_notification=False, parse_mode="HTML")


def generate_inline_buttons_row(chat_id, text, *args):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    inf = []
    for i in args:
        inf.append(types.InlineKeyboardButton(text=i[13:], callback_data=i))
    keyboard.row(*inf)
    bot.send_message(chat_id, text, reply_markup=keyboard, disable_notification=True)


def generate_inline_buttons_row_double(chat_id, text, *args):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    inf = []
    length = int(len(args)/2)
    for i in range(length):
        inf.append(types.InlineKeyboardButton(text=args[i * 2][6:], callback_data=args[i * 2]))
        inf.append(types.InlineKeyboardButton(text=args[i * 2 + 1][6:], callback_data=args[i * 2 + 1]))
        keyboard.row(*inf)
        inf = []
    bot.send_message(chat_id, text, reply_markup=keyboard, disable_notification=True, parse_mode="HTML")


def generate_inline_buttons_remove(chat_id, text, id_games, *args):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for i in range(len(args)):
        game = types.InlineKeyboardButton(text=args[i][6:], callback_data="ggame" + str(i % 10) + args[i][6:])
        cross = types.InlineKeyboardButton(text="\U0000274C", callback_data="re#" + str(i % 10) + id_games[i] +
                                                                            args[i][6:])
        keyboard.row(game, cross)
    bot.send_message(chat_id, text, reply_markup=keyboard, disable_notification=False, parse_mode="HTML")


def generate_inline_buttons_cost(chat_id, text, cost=0):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="Оплата", callback_data="paid##"))
    bot.send_message(chat_id, text, reply_markup=keyboard, disable_notification=False)


def delete_last_messages(chat_id, message_id):
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass


def clear_screen(chat_id, message_id_base, message_id, call, flag=0, no_add=0):
    Base.update_message_id_last_and_current(chat_id, message_id)
    if call[-2:] == "%^":
        Base.remove_callback(chat_id)
        call = call[:-2]
    elif call == "Меню:":
        Base.update_callback(chat_id, "/start")
    else:
        if no_add != 1:
            Base.update_callback(chat_id, call)
    if message_id_base != 0 and Base.show_message_last(chat_id):
        for i in range(int(Base.show_message_last(chat_id)), int(Base.show_message_current(chat_id)) + 2):
            delete_last_messages(chat_id, str(i))
    Base.update_message_id_in_chat_id(chat_id, message_id)
    Base.update_flag_in_messages(chat_id, flag)
    return call


"""#################################################################################################################"""


@bot.callback_query_handler(func=lambda call: re.search(r'genres', call.data) is not None)
def send_games_with_genre(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.data
    if Base.double_click_protection(chat_id, text):
        text = clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data)
        delete_last_messages(chat_id, message_id)

        games_list = Base.show_games_by_genre(text[6:])
        generate_inline_buttons(chat_id, "<b>Игры в жанре {}</b>     \U0000200C".format(text[6:]), *games_list)

        show_menu(chat_id, 0)


@bot.callback_query_handler(func=lambda call: re.search(r'ggame', call.data) is not None)
def send_game_info(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.data
    if Base.double_click_protection(chat_id, text):
        text = clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data)
        delete_last_messages(chat_id, message_id + 1)
        delete_last_messages(chat_id, message_id + 2)
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        if text[6:10] == 'cart':
            games_list = Base.show_game_by_name(text[12:])
        else:
            games_list = Base.show_game_by_name(text[6:])
        bot.send_message(chat_id=chat_id,  text="<b>" + games_list[0][1]+"</b>\n\n" + "Жанр: " + games_list[0][3] +
                         "      " + "  Год релиза на PS4: " + games_list[0][4] + "\n", parse_mode="HTML")
        if games_list[0][0] < 10:
            temp = "0" + str(games_list[0][0])
        else:
            temp = str(games_list[0][0])
        keyboard.row(types.InlineKeyboardButton(text="Играть за " + str(games_list[0][6]) + " \U000020BD",
                     callback_data="add_to_cart" + temp))
        bot.send_photo(chat_id, photo=games_list[0][5], caption="<i>"+games_list[0][2]+"</i>\n",
                       parse_mode="HTML", reply_markup=keyboard, disable_notification=True)

        show_menu(chat_id, 0)


@bot.callback_query_handler(func=lambda call: re.search(r'add_to_cart', call.data) is not None)
def add_to_cart(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.data
    if Base.double_click_protection(chat_id, text):
        text = clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data, no_add=1)
        delete_last_messages(chat_id, message_id)
        delete_last_messages(chat_id, message_id + 1)

        Base.update_customers_cart(chat_id, text[11:13])
        Base.show_cart_for_chat_id(chat_id)
        bot.send_message(chat_id, "Игра добалена в корзину!       \U0000200C")

        show_menu(chat_id, 1)


@bot.callback_query_handler(func=lambda call: re.search(r're#', call.data) is not None)
def send_cart_info(call):
    """
    Функция отвечает за удаление игры из корзины. Приходит сообщение вида re#Nnngame_name. N - порядковый номер на
    случай дублирования игры, nn - номер игры в БД.
    delete_last_messages нужны, т.к. удаление в double_click_protection происходит относительно нажатой нопки. А после
    кнопки удаления в данном случае есть еще сообщения.
    :param call:
    :return:
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.data
    if Base.double_click_protection(chat_id, text):
        text = clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data, no_add=1)
        delete_last_messages(chat_id, message_id + 1)
        delete_last_messages(chat_id, message_id + 2)
        print("text: {}, delete text {}".format(text, text[4:6]))
        try:
            Base.delete_game_from_cart(chat_id, text[4:6])
            games = Base.show_cart_for_chat_id(chat_id)
            print("games in cart = {}".format(games))
            temp = games[1]
            while len(temp) > 1 and temp[0] == ',':
                temp = temp[1:]
            if temp == ',' or temp == '':
                bot.send_message(chat_id, "В корзине нет товаров             \U0000200C")
            else:
                temp = (games[1].split(','))
                while temp[0] == '':
                    temp.pop(0)
                generate_inline_buttons_remove(chat_id, "<b>Игры в корзине:</b>                                       "
                                               "\U0000200C", temp, *Base.show_games_by_id(temp))
                generate_inline_buttons_cost(chat_id, "Для покупки необходимо внести {}  \U000020BD".
                                             format(Base.show_games_cost_by_id(temp)))
        except Exception:
            bot.send_message(chad_id_with_dev, "Произошла ошибка в отображении корзины, нужно проверить работает ли бот")
            Base.clear_cart_for_chat_id(chat_id)
        show_menu(chat_id, 3)


"""###############################################Оплата#############################################################"""


@bot.callback_query_handler(func=lambda call: re.search(r'paid##', call.data) is not None)
def ways_to_paid(call):
    """
    Пользователь получает список кнопок для выбора наиболее удобного типа оплаты.
    :param call:
    :return:
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.data
    if Base.double_click_protection(chat_id, text):
        text = clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data)
        delete_last_messages(chat_id, message_id)
        delete_last_messages(chat_id, message_id + 1)
        bot.send_message(chat_id, "Оплата осуществляется переводом на любой из предложенных счетов.")
        generate_inline_buttons(chat_id, "<b>Варианты оплаты:</b>", *["CRDDksКарта Сбербанка", "CRDDkrКарта "
                                "Рокет Банка","CRDDktКарта Тинькова", "CRDDkoКарта Открытия", "CRDDkqQIWI",
                                "CRDDkwWebmoney", "CRDDkcBitcoin"])
        show_menu(chat_id, 3)


@bot.callback_query_handler(func=lambda call: re.search(r'CRDD', call.data) is not None)
def various_of_paid(call):
    """
    Коллбэком принимаем сообщение вида "CRDDxx", где xx - один из варантов среди if-ов. Пользователю передается
    информация о выбранном способе оплаты.
    :param call:
    :return:
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.data
    if Base.double_click_protection(chat_id, text):
        text = clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data)
        games = Base.show_cart_for_chat_id(chat_id)
        temp = games[1]
        while len(temp) > 1 and temp[0] == ',':
            temp = temp[1:]
        temp = (games[1].split(','))
        while temp[0] == '':
            temp.pop(0)
        if text[4:6] == "ks":
            card = "на карту "
        elif text[4:6] == "kr":
            card = "на карту "
        elif text[4:6] == "kt":
            card = "на карту "
        elif text[4:6] == "ko":
            card = "на карту "
        elif text[4:6] == "kq":
            card = "на счет +"
        elif text[4:6] == "kw":
            card = "на счет "
        elif text[4:6] == "kc":
            card = "по текущему курсу на счет "
        generate_inline_buttons(chat_id, "Для оплаты товаров из корзины необходимо перевести %s \U000020BD "
            % Base.show_games_cost_by_id(temp) + card + ".\n\nПосле перевода нажмите на кнопку 'Оплата внесена'",
            "PAIDSBОплата внесена")
        show_menu(chat_id, 3)


@bot.callback_query_handler(func=lambda call: re.search(r'PAID', call.data) is not None)
def paid_complete(call):
    """
    Коллбэком принимаем сообщение вида "PAIDxx", где xx - один из варантов среди if-ов. Пользователь видет сообщение о
    модерации. Админу приходит соощение о необходимости проверки оплаты.
    :param call:
    :return:
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.data
    if Base.double_click_protection(chat_id, text):
        text = clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data)
        bot.send_message(chat_id, "Проверяем внесение оплаты. Ожидайте сообщения от модератора (не более 10 минут)")
        show_menu(chat_id, 3)
        if text[4:6] == "SB":
            card = "сбер"
        elif text[4:6] == "RC":
            card = "рокет"
        elif text[4:6] == "TK":
            card = "тиньков"
        elif text[4:6] == "OT":
            card = "открытие"
        elif text[4:6] == "QI":
            card = "киви"
        elif text[4:6] == "WM":
            card = "вебмани"
        elif text[4:6] == "CC":
            card = "биткойны"
        games = Base.show_cart_for_chat_id(chat_id)
        j = 0
        temp = games[1]
        for i in temp:
            if i == ',':
                j += 1
            else:
                break
        temp = temp[j:]
        temp = (temp.split(','))
        while temp and temp[0] == '':
            temp.pop(0)
        games_list = Base.show_games_by_id(temp)
        res = ""
        for i in games_list:
            res = res + ", " + i[6:]
        temp2 = str(Base.show_games_cost_by_id(temp))
        bot.send_message(chad_id_with_dev, "Проверить внесение денег на " + card + ", user: @" + str(call.from_user.username) +
                         ".\n" + "Заказал игры: " + res + ".\nНа сумму в " + temp2)
        Base.clear_cart_for_chat_id(chat_id)


"""##################################################################################################################"""


@bot.callback_query_handler(func=lambda call: re.search(r'menu_ж', call.data) is not None)
def show_genres(call):
    """
    If user push the button "Genres" in menu, bot uses this commands and send all genres, which he found in Base.
    :param call:
    :return: Inline buttons, each shows unique genre from Base
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.message.text
    if Base.double_click_protection(chat_id, text):
        clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data)

        games = Base.show_all_genres()

        generate_inline_buttons_row_double(chat_id, "<b>Список жанров:</b>                                        "
                                                    "\U0000200C", *games)
        show_menu(chat_id, 0)


@bot.callback_query_handler(func=lambda call: re.search(r'menu_т', call.data) is not None)
def show_top(call):
    """
    If user push the button "Top" in menu, bot uses this commands and send all games from top20 table in Base
    :param call:
    :return: Inline buttons, each shows the game from top20 table Base
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.message.text
    if Base.double_click_protection(chat_id, text):
        clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data)

        games_list = Base.show_games_by_id(Base.show_all_top())
        generate_inline_buttons_row_double(chat_id, "<b>Топ 20 популярных игр:</b>                              "
                                                    "\U0000200C", *games_list)
        show_menu(chat_id, 4)


@bot.callback_query_handler(func=lambda call: re.search(r'menu_к', call.data) is not None)
def show_cart(call):
    """
    If user push the button "Cart" in menu, bot uses this commands and send all games from users Cart in Base. If no
    games was add yet, bot send message that cart is free
    :param call:
    :return:
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.message.text
    if Base.double_click_protection(chat_id, text):
        clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data)
        games = Base.show_cart_for_chat_id(chat_id)
        time_add = int(time.time() * 100)
        try:
            j = 0
            for i in games[1]:
                if i == ',':
                    j += 1
                else:
                    break
            if time_add - games[2] > 172800:
                Base.update_customers_cart(chat_id, ",")
            if games[1] == '' or games[1] == ',' or j == len(games[1]):
                bot.send_message(chat_id, "В корзине нет товаров             \U0000200C")
            else:
                temp = (games[1].split(','))
                while temp and temp[0] == '':
                    temp.pop(0)
                print("show_cart games list = ", temp, "available games = ",  Base.show_games_by_id(temp))
                generate_inline_buttons_remove(chat_id, "<b>Игры в корзине:</b>                                        "
                                               "    \U0000200C", temp, *Base.show_games_by_id(temp))
                generate_inline_buttons_cost(chat_id, "Для покупки всех игр в корзине необходимо внести {} \U000020BD".
                                             format(Base.show_games_cost_by_id(temp)))
        except Exception:
            bot.send_message(chad_id_with_dev, "Произошла ошибка в отображении корзины, нужно проверить работает ли бот")
            Base.clear_cart_for_chat_id(chat_id)
        show_menu(chat_id, 3)


@bot.callback_query_handler(func=lambda call: re.search(r'menu_п', call.data) is not None)
def use_search(call):
    """
    After user pushed this button, he can type the Name of the gam and bot going to  found it in Base and show it, or
    send message that no game was founded, please try again.
    :param call:
    :return:
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.message.text
    if Base.double_click_protection(chat_id, text):
        clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data, 2)
        show_menu(chat_id, 0)
        bot.send_message(chat_id, "Введите название игры:")


@bot.callback_query_handler(func=lambda call: re.search(r'menu_раз', call.data) is not None)
def send_message_to_developer(call):
    """
    After user pushed this button all his messages will transfer to developer. Достигается это сохранением флага 1 в
    Base.show_messages_flag(chat_id)
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.data
    if Base.double_click_protection(chat_id, text):
        clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data, 1)
        show_menu(chat_id, 2)
        bot.send_message(chat_id, "Введите сообщение: ")


"""##################################################################################################################"""


# Если Коллбэк /start, то показываем приветсвенную страницу. Необходимо если на стартовую страницу попадаем через кнопку
# назад
@bot.callback_query_handler(func=lambda call: re.search(r'/start', call.data) is not None)
def show_start_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    text = call.data
    if Base.double_click_protection(chat_id, text):
        clear_screen(chat_id, Base.show_message_current(chat_id), message_id, call.data)
        show_start(call.message)


# Если сообщение /start, то показываем приветсвенную страницу
@bot.message_handler(commands=['start'])
def send_greetings(message):
    show_start(message)


# Если нужна информация о боте либо навигация по странице, то
@bot.message_handler(commands=['help'])
def send_humanitarian(message):
    chat_id = message.chat.id
    message_id = message.message_id
    clear_screen(chat_id, Base.show_message_current(chat_id), message_id, "/help")

    bot.send_message(message.chat.id, "Привет!\nЯ продаю цифровые копии игр для Playstation 4.\n"
                                      "Игры можно выбрать по жанрам, по популярности или поискать в моей базе.\n"
                                      "Цены, в среднем, на 40% ниже, чем в оффициальном магазине.\n"
                                      "Если возникнут вопросы - пишите разработчику, он все расскажет "
                                      "и объяснит \U0001F609.\nПриятного использования! "
                                      "Надеюсь на продолжительное сотрудничество!")


@bot.message_handler(func=lambda message: re.search(r'получить_коды_фото', message.text) is not None)
def get_file_ids(message):
    """При вводе сообщения 'получить_коды_фото' все фото из папки photos/ будут направлены в базу телеграма
    в качестве ответа вернутся хэши для каждой из переданных фото """
    i = 0
    for file in os.listdir('photos/'):
        if file.split('.')[-1] == 'jpg' or 'JPG':
            f = open('photos/' + file, 'rb')
            msg = bot.send_photo(message.chat.id, f)
            bot.send_message(message.chat.id, msg.photo[0].file_id, reply_to_message_id=msg.message_id)
            f.close()
            i += 1
            time.sleep(5)


@bot.message_handler(func=lambda message: re.search(r'ракамакафо', message.text) is not None)
def debug_message(message):
    """Тех-сообщение"""
    bot.send_message(chad_id_with_dev, str(message))


# Во всех прочих случаях отправляется сообщение со строкой "text"
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """
    Если флаг, сохраненный в Base.show_messages_flag(chat_id), равен 1, то сообщения автоматически перенаправляются
    в чат-айди chad_id_with_dev.
    Если флаг равен 2, то происходит поиск в БД. Помимо этого, запрос сохраняется в логах"
    :param message:
    :return:
    """
    chat_id = message.chat.id
    text = message.text
    flag = Base.show_messages_flag(chat_id)
    if flag == 1:
        bot.send_message(chad_id_with_dev , "chat with " + str(chat_id) + ", user: @" + str(message.from_user.username) +
                         ".\n" + text)
    elif flag == 2:
        clear_screen(chat_id, Base.show_message_current(chat_id), message.message_id, text, 2)

        if len(text) < 2:
            bot.send_message(chat_id, "Слишком короткий запрос, не могу ничего найти")
        else:
            with open("log.txt", 'a') as log:
                log.write(str(message))
            search = Base.show_search_games(Base.search_in_games(text))
            if len(search) == 0:
                show_menu(chat_id, 1)
                bot.send_message(chat_id, "По запросу \"{}\" ничего не найдено. Попробуйте еще раз".format(text))
            else:
                generate_inline_buttons(chat_id, "Результат поиска:", *search)
                show_menu(chat_id, 1)
    else:
        bot.send_message(chat_id, "Не понял запрос. Возможно, кто-то из нас делает что-то не так. Посмотрите /help")


if __name__ == "__main__":
    # Base.delete_messages_table()
    # Base.delete_cart_table()
    # Base.delete_games_table()
    # Base.delete_top_table()
    Base.create_tables()
    Base.fill_games()
    Base.fill_top()
    # bot.polling()
    app.run()
