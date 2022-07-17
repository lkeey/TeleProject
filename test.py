import json
from datetime import datetime, timedelta
from requests import request
import telebot
from deepface import DeepFace
import qrcode
import numpy as np 
from forex_python.converter import CurrencyRates
from icrawler.builtin import GoogleImageCrawler
import os
import shutil
from translate import Translator
import requests

def test():
    counter = 0
    with open("names.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()
        # print(lines)
        for line in lines:
            if "катя" in line.lower():
                print("зашел") 
                counter += 1

    print("катя встречается",counter,"раз")



from hashlib import new
from PIL import Image, ImageFilter, ImageEnhance
def test_2():
    file = Image.open("Huvstvitel.jpg")
    file = file.transpose(Image.FLIP_LEFT_RIGHT)
    file.show()


    new_file = Image.open("5422931ca6dcc.jpg")
    new_file = new_file.convert("L")
    new_file.show() 


def test_3():
    weather = {
        "London": "25 degree",
        "Moscow": "30 degree",
        "Saint-Petersburg": "15 degree",
    }

    with open('data_base.json', 'w', encoding='utf-8') as file:
            json.dump(weather, file, sort_keys = True)

    with open('data_base.json', 'r', encoding='utf-8') as file:
        weather = json.load(file)
        print(weather) 
def test_4():
    besties = {
    '6а' : ['Иванова', 'Петров', 'Петренко', 'Степанов'],
    '7а' : ['Васильев', 'Игнатова']
    }
    list_best = list()
    list_best.append("Пеньков")

    besties["6б"] = list_best

    list_I = list()

    for best in besties:
        for i in range(len(besties[best])):
            if besties[best][i][0].lower() == 'и':
                list_I.append(besties[best][i])

    for surname in list_I:
        print(surname)

def test_5():
    # Mops
    all_smiles = ["CAACAgIAAxkBAAIBg2J5e_A3Qyvvbx5mJq7zzyC4fsdXAAILAAOc_jIw9y0wzeHFaC0kBA"]


    with open('Data-Bases/Data-Smiles.json', 'w', encoding='utf-8') as file:
        data = {
            "all_smiles": all_smiles
        }
        json.dump(data, file, sort_keys = True)


# def test_6():
#     smile_1st = "cAAVK_mSpW_9hfOrH4cTWckQ"
#     smile_2nd = "p_csFbW_3MgAABA5JOLqR-Pg"
#     print(len(smile_1st))
#     smile_3rd = "CAACAgIAAxkBAAIBUmJ5eJCiqOh0O8UL-puFfhUxtxfLAAKWDAACC1sZSkTJo0Tt48bJJAQ"
#     count = 0
#     for i in range(len(smile_1st)):
#         if smile_1st[i] != smile_2nd[i]:
#             count += 1
#     print(count)
#     print(smile_1st == smile_2nd)



user = {'last_name': 'Кирюшин', 'language_code': 'en', 
        'is_bot': False, 'id': str(56), 
        'username': 'l_keey', 
        'first_name': 'Лёша'
        }

data_user = {
        
        'last_name': user["last_name"], 
        'language_code': user["language_code"], 
        'id': str(user["id"]), 
        'username': user["username"], 
        'first_name': user["first_name"],
        'password': "457n@4/2",
        'points': 0,
        'registered': str(datetime.now().strftime("%D %H:%M:%C")),

        # Для внутренних процессов
        "main": "online",
        "get_weather": False,
        "rate_weather": 0,
        "city": "DEFAULT",
        "was_online": str(datetime.now().strftime("%H:%M")),
        "get_url": False,
        "post": "User",
        "get_sentence": False,
        "get_qr": False,
        }



def test_6():
    # with open('Technology/Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
    #     data_all_users = json.load(file)
    #     data_all_users = data_all_users["users"]
    #     print("data_all_users", data_all_users)
    #     print("data_all_users 2",data_all_users["users"])
    #     print("data_all_users 3",data_all_users["users"][str(user["id"])])
    #     data_all_users["users"][str(user["id"])]["was_online"] = str(datetime.now())

    data_all_users = {}

    if data_user["id"] not in data_all_users:
        data_all_users[data_user["id"]] = data_user
    else:
        print("Уже есть")

    with open('Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
        data = {
                "users": data_all_users
                }
        json.dump(data, file, sort_keys = True)

        print(data)

    print(len(data))
    # {"users": {"1010205515": {"first_name": "\u041b\u0451\u0448\u0430", "id": "1010205515", "language_code": "en", "last_name": "\u041a\u0438\u0440\u044e\u0448\u0438\u043d", "username": "l_keey"}, "1580133018": {"first_name": "Daria", "id": "1580133018", "language_code": "ru", "last_name": null, "username": null}, "56": {"first_name": "\u041b\u0451\u0448\u0430", "id": "56", "language_code": "en", "last_name": "\u041a\u0438\u0440\u044e\u0448\u0438\u043d", "username": "l_keey"}, "952492649": {"first_name": "TT:", "id": "952492649", "language_code": "ru", "last_name": "hopelesdeath", "username": "LoveYouW0W"}}}


def test_7():
    data_all_users = {'1010205515': {'first_name': 'Лёша', 'id': '1010205515', 'language_code': 'en', 'last_name': 'Кирюшин', 'username': 'l_keey'}, '1580133018': {'first_name': 'Daria', 'id': '1580133018', 'language_code': 'ru', 'last_name': None, 'username': None}, '56': 
    {'first_name': 'Лёша', 'id': '56', 'language_code': 'en', 'last_name': 'Кирюшин', 'username': 'l_keey'}, '952492649': {'first_name': 'TT:', 'id': '952492649', 'language_code': 'ru', 'last_name': 'hopelesdeath', 'username': 'LoveYouW0W'}}
    # добавить время, когда залогинился
    for user in data_all_users:
        print(data_all_users[user]["first_name"])
      
def test_8():
    with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            data_all_users = json.load(file)
            user_data = data_all_users["users"]
            user_data = user_data[user["id"]]
            print(user_data)

import string
import secrets

def test_9():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    print(password)


def test_10():
    print(datetime.now().strftime("%D %H:%M:%C"))

def test_11():
    data = str(datetime.now())
    fifteen_minutes = timedelta(minutes=15)
    if int(data) - fifteen_minutes >= data:
        print(True)
    else:
        print(False)


def test_12():
    with open('Technology/Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            data_all_users = json.load(file)
            data_all_users = data_all_users["users"]
            print("data_all_users", len(data_all_users))

def test_13():
    string = str(datetime.now().strftime("%H:%M"))

    string_now = str(datetime.now().strftime("%H:%M"))

    date_object = datetime.strptime(string, '%H:%M')
    date_object_now = datetime.strptime(str(datetime.now().strftime("%H:%M")), '%H:%M')

    fifteen_minutes = timedelta(minutes=15)
    print("date_object", date_object+fifteen_minutes)
    print("date_object_now", date_object_now)

    if date_object + fifteen_minutes >= date_object_now:
        print(True)

    else:
        print(False)
        
def test_14():
    data = {"coord": {"lon": 37.6156, "lat": 55.7522}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds",
    "icon": "04d"}], "base": "stations", "main": {"temp": 9.57, "feels_like": 6.72, "temp_min": 5.75, "temp_max": 10.35, 
    "pressure": 1020, "humidity": 34, "sea_level": 1020, "grnd_level": 1002}, "visibility": 10000, "wind": {"speed": 5.94,
    "deg": 335, "gust": 6.75}, "clouds": {"all": 95}, "dt": 1652091338, "sys": {"type": 1, "id": 9027, "country": "RU", 
    "sunrise": 1652059798, "sunset": 1652116922}, "timezone": 10800, "id": 524901, "name": "Moscow", "cod": 200}

    humidity = data["main"]["humidity"]
    
    print("humidity", humidity)


# Айди фото

# [<telegram.files.photosize.PhotoSize object at 
# 0x000001E1BC64BCA0>, <telegram.files.photosize.PhotoSize 
# object at 0x000001E1BC64BD60>, <telegram.files.photosize.
# PhotoSize object at 0x000001E1BC64BDC0>, <telegram.files.
# photosize.PhotoSize object at 0x000001E1BC64BE20>]

bot = telebot.TeleBot("5366540233:AAEH04SZyyGE4uD7WvTHiRTXKxCvnQ-uqAM")

def face_analyze(img_1st):
    try:
        print("ТУТ")
        result_dict = DeepFace.analyze(img_1st, actions=["emotion"])
        print("ЗДЕСЬ")
        print("DICT:", result_dict)
        
    except Exception as _Except:
        return _Except

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.photo[0].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src='Data-Bases/'+file_info.file_path
        with open(src, 'w') as new_file:
            face_analyze(new_file)
        bot.reply_to(message,"Фото добавлено") 

    except Exception as e:
        bot.reply_to(message, e)

# bot.polling()

import os
def test_15():
    filename = "qrcode2.png"
    # создать экземпляр объекта QRCode
    qr = qrcode.QRCode(version=1, box_size=7, border=4)
    # добавить данные в QR-код
    qr.add_data("https://vk.com/l_keey")
    # компилируем данные в массив QR-кода
    qr.make()
    # распечатать форму изображения
    print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
    # переносим массив в реальное изображение
    img = qr.make_image(fill_color="#eca1a6", back_color="black")
    # сохраняем в файл
    img.save(filename) 
    img = Image.open(filename)
    img.show()

    os.remove(filename)
import wiki_search
import re
from random import *

# request = wikipedia.summary("cat", sentences=2)
# update.message.reply_text(request) 

# request=re.sub('\([^()]*\)', '', request) 
# request=re.sub('\([^()]*\)', '', request) 
# request=re.sub('\{[^\{\}]*\}', '', request) 

# list_requests = list(wikipedia.page.title[request])

# print(list_requests[0])
def test_16():
    try:
        p = wiki_search.page("cat")
    except wiki_search.DisambiguationError as e:
        s = choice(e.options)
        p = wiki_search.page(s)

    print(p)
    print(p.summary)
    # while True:
    #     try:
    #         request = wikipedia.summary("cat", sentences=2)
    #         break

    #     except wikipedia.exceptions.DisambiguationError as e: 
    #         s = choice(e.options)
    #         p = wikipedia.summary(s, sentences=2)

    # print(p)

    # Вычисляем длину
    # url = len(wikipedia.page(request).images)

    # print(url)
import wikipedia

def test_17(sentent):
    while True:
        try:
            page = wikipedia.page(sentent)
            break

        except wikipedia.DisambiguationError as e:
            chosen = choice(e.options)
            page = wikipedia.page(chosen)
            print("Слишком много страниц...\nРасскажу о "+str(page)) 
            break
    request = wiki_search.summary(page, sentences=2)         
    print(str(request))

    print(len(wiki_search.page(request).images))

import wget
import wiki_search
def test_18():
    responce = wiki_search.searching("car")
    print(responce)

def test_19():
    request = wiki_search.searching("car", "en")
    print(request)
    # url_list = list()

    if len(wikipedia.page(request).images) >= 0:
        for i in range(len(wikipedia.page(request).images)):
            url = wikipedia.page(request).images[i]
            if "jpg" in url:
                print(url)
                break


    url = wikipedia.page("money").images[0]
    print(url)

    filename = f"wiki.png"
    wget.download(url, filename)

    print()

from urllib.request import urlopen   
# test_19()
# url = urlopen("https://upload.wikimedia.org/wikipedia/commons/0/0c/Black_Cat_%287983739954%29.jpg")
# print(url)
# filename = f"wiki{144}.jpg"
# filename = wget.download("https://upload.wikimedia.org/wikipedia/commons/0/0c/Black_Cat_%287983739954%29.jpg")

import emoji
def test_20():
    a = 3

    if a == 1:
        emodzy = ':v:'
    else:
        emodzy = ':house_with_garden:'
    print (emoji.emojize(f"Python is {emodzy}",  language = 'alias' )) 
    print(emoji.emojize("Чтобы заработать Intent-ы переходи сюда:(url...) ®", language = 'alias'))

    print("\x1b]8;;http://example.com/\aCtrl+Click here\x1b]8;;\a")

def bio():
    str = '''
    · Возможность общения с чат-ботом 💬
    · Получение погоды в любом городе ⛅ 
    · Мобильная работа с базами данных 📝
    · Создание более приятного url-адреса пользователя 📎
    · Отправка данных пользователя о его соединении с интернетом 🌐
    · Парсинг данных Википедии с целью ответа на запрос пользователя 🔎
    · Создание Qr-code при любом введенном значении пользователя ✍

    · В случае обнаружения неполадок, существует возможность обратиться к модератору группы Vk ⚠

            '''
    print(len(str))

    print(len(". В случае обнаружения неполадок, существует возможность обратиться к модератору группы Vk ⚠"))

import array as arr
def test_21():
    with open("Data-Bases/Data-users.json", "r", encoding='utf-8') as file:
        # Весь
        data_all_users = json.load(file)
        users_data = data_all_users["users"]

    points_list = list()

    dict_users = {
        # user: points
    }

    for user in users_data: 
        dict_users[users_data[user]["username"]] = users_data[user]["points"]
        points_list.append(users_data[user]["points"])

    # 1-ое
    first_place = max(points_list)
    points_list.remove(first_place)

    # 2-ое
    second_place = max(points_list)
    points_list.remove(second_place)

    # 3-ье
    third_place = max(points_list)
    
    top_place = list()
    # 1st place
    for user in dict_users:
        if dict_users[user] == first_place:
            name_1st = user
            
            top_place.append(name_1st)

            del dict_users[user]
            break

    for user in dict_users:
        if dict_users[user] == second_place:
            name_2nd = user
            top_place.append(name_2nd)

            del dict_users[user]
            break

    for user in dict_users:
        if dict_users[user] == third_place:
            name_3rd = user
            top_place.append(name_3rd)

            del dict_users[user]
            break

    return top_place

def test_22(amount):
    with open("Data-Bases/Data-users.json", "r", encoding='utf-8') as file:
        # Весь
        data_all_users = json.load(file)
        users_data = data_all_users["users"]

    points_list = list()

    dict_users = {
        # user: points
    }

    for user in users_data: 
        dict_users[users_data[user]["username"]] = users_data[user]["points"]
        points_list.append(users_data[user]["points"])

    top_place = list()

    for i in range(amount):
        # Наивысшее место
        the_most_place = max(points_list)
        points_list.remove(the_most_place)

        for user in dict_users:
            if dict_users[user] == the_most_place:
                name_1st = user
                
                top_place.append(name_1st)

                del dict_users[user]
                break
    return top_place    


def amount_data():
    data = {}
    data["months"] = {}

    for i in range(4):
        # data["months"] = [i+9]
        data["months"][i+9] = {}
        data["months"][i+9]["users"] = 0
        data["months"][i+9]["messages"] = 0
        data["months"][i+9]["intents"] = 0

    print(data)

    with open('Data-Bases/Data-Amount.json', 'w', encoding='utf-8') as file:
        
        json.dump(data, file, sort_keys = True)



def data_day():
    with open('Data-Bases/Data-Amount.json', 'r', encoding='utf-8') as file:
        data_amount = json.load(file)["months"]
    
        for month in data_amount:
            print(f"{month} - {data_amount[month]['users']} users - {data_amount[month]['messages']} messages - {data_amount[month]['intents']} intents")


    with open('Data-Bases/Data-day.json', 'w', encoding='utf-8') as file:
            data = {
                f'{datetime.now().strftime("%m%d")}': {
                    "messages": 0,
                    "intents": 0,
                    "users": 0,
                }
            }
            json.dump(data, file, sort_keys = True)


def GoogleImgDownload():
    id = 5
    filters = dict(
        type='photo'
    )

    crawler = GoogleImageCrawler(storage={'root_dir': f'./img_by_{id}'})
    crawler.crawl(keyword='spongebob', max_num=5, filters=filters)
    
    for filename in os.listdir(f'./img_by_{id}'):

        with open(os.path.join(f'./img_by_{id}', filename), 'rb') as f:
            print("FILE", f)

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'./img_by_{id}')
    shutil.rmtree(path)

def CutWikiPage():
    string = "<WikipediaPage 'Moscow'>"

    print(string[16:(len(string)-2)])


def translate(text):
 
    translator = Translator(from_lang="ru", to_lang="en")
    text = translator.translate(text)
    print(text)


def test_send_post_request():
    secret_key = '=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD, =EF=BF=BD=EF=BF=BD =EF=BF==BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF==BD =EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD =EF=BF=BD=EF==BF=BD =EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF==BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD'

    url = f'http://127.0.0.1:5000/get/Data_Users/{secret_key}/'

    # requests.post(url, {"Name": "Sasha"})

    # print("OK")


    data = {
        "json": "Aleksey",
    }

    r = requests.post(url, data=data)
    print(r.text)


