#           Оложено:
# Фотографии
# Скачка данных с сайта

#           Разрабатывается
# Начислять опыт более правильно( проверять есть ли интент
# : проверить работает ли бд)
# Работа с текстом (озвучка)
# Работа с голосовыми сообщениями
# Админ и обычный 

# Разделить базы данных на типы: будут хранится у сайта, 
#                           будут хранится у бота

# Модуль
import wiki_search

from random import *
from time import *
from datetime import datetime, timedelta
import string
import secrets
import nltk
import json
import sklearn
import requests
from telegram import Update, ForceReply, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from unittest import result
from deepface import DeepFace
import speedtest  
import pyshorteners
import wikipedia
import re
import qrcode
import numpy as np 
import os
import emoji
from icrawler.builtin import GoogleImageCrawler
import shutil
from translate import Translator

# Variables
open_weather_token = '4da9f58fdb818e1b9979d5c95b2f2aaf'
tlgrm_tocken = "5366540233:AAEH04SZyyGE4uD7WvTHiRTXKxCvnQ-uqAM"
google_search = "AIzaSyBzdzDll3gyr7867TsfI2FbIcuEzl_8crA"
secret_key = '=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD, =EF=BF=BD=EF=BF=BD =EF=BF==BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF==BD =EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD =EF=BF=BD=EF==BF=BD =EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF==BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD'
host = 'l14key.pythonanywhere.com'

def request_to_server(name_data):
    url = f'http://{host}/get/{name_data}/{secret_key}/'
    
    response = requests.get(url).json()

    print("RESPONSE",response)

    return response

def post_to_server(name_data, data_base):
    try:
        print("DATA", data_base)

        data = {
            "json": data_base,
        }

        # headers = {'Content-type': 'application/json',
        #             'Accept': 'text/plain'
        # }
        
        url = f'http://{host}/get/{name_data}/{secret_key}/'

        response = requests.post(url, json=json.dumps(data))

        print("JSON", (json.dumps(data)))

        print("STATUS", response.status_code)

    except Exception as _ex:
        print("Don't open",_ex)


def saving_data_of_user(user, data):

    # Открытие словаря
    try:
        # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            # Весь
        data_all_users = request_to_server("Data_Users")
            # user_data = data_all_users["users"]
        user_data = data_all_users["users"]
        # Пользователя
        user_data = user_data[str(user["id"])]

    except:
        print("НЕВОЗМОЖНО ОТКРЫТЬ!")
    
    print("G-W",data["get_weather"])

    print("URL:", data["get_url"])

    print("WAS_ONLINE", data["was_online"])

    print("User-data-MAIN", data["main"])

    print("GET_SENTENCE:", data["get_sentence"])

    print("GET_QR:", data["get_qr"])

    if data["main"] == "online":
        data_all_users["users"][str(user["id"])]["was_online"] = str(datetime.now().strftime("%H:%M"))
    
    data_all_users["users"][str(user["id"])]["main"] = data["main"]
    
    print("Main", user["id"], data["main"])

    print("MAIN:", data_all_users["users"][str(user["id"])]["main"])
    data_all_users["users"][str(user["id"])]["rate_weather"] = data["rate_weather"]
    data_all_users["users"][str(user["id"])]["get_weather"] = data["get_weather"]
    data_all_users["users"][str(user["id"])]["get_url"] = data["get_url"]
    data_all_users["users"][str(user["id"])]["get_sentence"] = data["get_sentence"]
    data_all_users["users"][str(user["id"])]["get_qr"] = data["get_qr"]
    data_all_users["users"][str(user["id"])]["city"] = data["city"]

    try:
        # with open('Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
        
        data = {
                "users": data_all_users["users"]
                }

        print("ALL OKEY")

        #     json.dump(data, file, sort_keys = True)
        post_to_server("Data_Users", data)

        print("ALL OKEY 2")

    except Exception as _EX:
        print("НЕ ОТКРЫВАЕТСЯ HERE\n"+str(_EX))

def add_message(amount):
    print("ADD MESSAGE")

    # В словарь DAY
    try:
        # with open("Data-Bases/Data-day.json", "r", encoding='utf-8') as file:
            # data_day = json.load(file)

        data_day = request_to_server("Data_Day")

        if f'{datetime.now().strftime("%m%d")}' not in data_day:
            data_day[f'{datetime.now().strftime("%m%d")}'] = {}
            data_day[f'{datetime.now().strftime("%m%d")}']["intents"] = 0
            data_day[f'{datetime.now().strftime("%m%d")}']["users"] = 0
            data_day[f'{datetime.now().strftime("%m%d")}']["messages"] = 0

        data_day[f'{datetime.now().strftime("%m%d")}']["messages"] += amount
            
        # with open('Data-Bases/Data-day.json', 'w', encoding='utf-8') as file:
        #     json.dump(data_day, file, sort_keys = True)

        post_to_server("Data_Day", data_day)

        # В словарь AMOUNT
        # with open("Data-Bases/Data-Amount.json", "r", encoding='utf-8') as file:
            # data_day = json.load(file)["months"]

        request_to_server("Data_Amount")["months"]
        print("Month", datetime.now().strftime("%m"))
        print("Data", data_day[f'{datetime.now().strftime("%m")}'])
        
        data_day[f'{datetime.now().strftime("%m")}']["messages"] += 3

        # with open("Data-Bases/Data_Amount.json", "w", encoding='utf-8') as file:
        data = {"months": data_day}
            
            # json.dump(data, file, sort_keys = True)

        post_to_server("Data_Amount", data)

        print("MESSAGE WAS ADDED")


    except Exception as _Ex:
        print("Warning in Add_Message\n", _Ex)

def add_online(user):
    # Открытие словаря
    try:
        # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            # data_all_users = json.load(file)

        data_all_users = request_to_server("Data_Users")
        user_data = data_all_users["users"]
        user_data = user_data[str(user["id"])]

    except Exception as _EX:
        print("НЕ ОТКРЫВАЕТСЯ "+str(_EX))

    user_data["main"] = "online"

    saving_data_of_user(user, user_data)

def get_password():
    # 8 символов
    all_passwords = list()
    
    # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        # data_all_users = json.load(file)
    data_all_users = request_to_server("Data_Users")    
    data_all_users = data_all_users["users"]
        
    for user in data_all_users:
        print(data_all_users[user]['password'])
        all_passwords.append(data_all_users[user]['password'])
        

    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))

    while password in all_passwords:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))
    
    print("PASSWORD", password)

    return password

        # Приветствие ( /start )
def start(update: Update, context: CallbackContext) -> None:
    print("Successfully")

        
        # Future-Forest, [5/10/2022 3:59 PM]
        # Hi Лёша Кирюшин!

        # Future-Forest, [5/10/2022 3:59 PM]
        # [Лёша Кирюшин](tg://user?id=1010205515)\!  
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        emoji.emojize(fr'Hi, {user.mention_markdown_v2()}\!:v:', language = 'alias'),
        reply_markup=ForceReply(selective=True),
        
    )
    # update.message.reply_text(fr'{user.mention_markdown_v2()}\!') 

    # update.message.reply_text(str(user))
    # {'last_name': 'Кирюшин', 'language_code': 'en', 
    # 'is_bot': False, 'id': 1010205515, 
    # 'username': 'l_keey', 
    # 'first_name': 'Лёша'}

    password = get_password() 
    print("password", password)

    # Данного пользователя
    data_user = {
        'last_name': user["last_name"], 
        'language_code': user["language_code"], 
        'id': str(user["id"]), 
        'username': user["username"], 
        'first_name': user["first_name"],
        'password': password,
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

    try:
        # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        #     data_all_users = json.load(file)
        data_all_users = request_to_server("Data_Users")
        data_all_users = data_all_users["users"]
    except:
        update.message.reply_text(emoji.emojize("Warning in open BASE-DATA :warning:\nPlease, write /error", language = 'alias' ))

    # если не зареган
    if not (data_user["id"] in data_all_users):
        data_all_users[data_user["id"]] = data_user
        try:
            # with open('Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
            data = {
                    "users": data_all_users
                    }
                # json.dump(data, file, sort_keys = True)
            post_to_server("Data_Users", data)
            # Добавление в словарь DAY

            # with open("Data-Bases/Data-day.json", "r", encoding='utf-8') as file:
            #     data_day = json.load(file)

            data_day = request_to_server("Data_Day")

            if f'{datetime.now().strftime("%m%d")}' not in data_day:
                data_day[f'{datetime.now().strftime("%m%d")}'] = {}
                data_day[f'{datetime.now().strftime("%m%d")}']["intents"] = 0
                data_day[f'{datetime.now().strftime("%m%d")}']["users"] = 0
                data_day[f'{datetime.now().strftime("%m%d")}']["messages"] = 0

            data_day[f'{datetime.now().strftime("%m%d")}']["users"] += 1
                        
            # with open('Data-Bases/Data-day.json', 'w', encoding='utf-8') as file:
            #     json.dump(data_day, file, sort_keys = True)
            
            post_to_server("Data_Day", data_day) 

            # В словарь AMOUNT
            # with open("Data-Bases/Data-Amount.json", "r", encoding='utf-8') as file:
            #     data_day = json.load(file)["months"]
            request_to_server("Data_Amount")["months"]
            print("Month", datetime.now().strftime("%m"))
            print("Data", data_day[f'{datetime.now().strftime("%m")}'])
            
            data_day[f'{datetime.now().strftime("%m")}']["users"] += 1

            # with open("Data-Bases/Data_Amount.json", "w", encoding='utf-8') as file:
            data = {"months": data_day}
                
                # json.dump(data, file, sort_keys = True)
            
            post_to_server("Data_Amount", data)

        except Exception as _Ex:
            update.message.reply_text(emoji.emojize("Warning in open data-user :warning:\nPlease, write /error", language = 'alias' ))
            print("Warning", _Ex)

        update.message.reply_text(emoji.emojize("Вы были успешно зарегистрированы! :globe_with_meridians:", language = 'alias' ))
    else:
        
        update.message.reply_text(emoji.emojize("С возвращением)\nВижу:eyes:, вы уже были здесь зарегистрированы!", language = 'alias'))
    # update.message.reply_text(str(len(data_all_users)))
        # Остальные сообщения
    
    


    # подписка к векторайзеру
def get_intent_by_model(text, BOT_CONFIG):

    

    corpus = []
    y = []
    for intent in BOT_CONFIG['intents'].keys():
        for example in BOT_CONFIG['intents'][intent]['examples']:
            corpus.append(example)
            y.append(intent)

    corpus_train, corpus_test, y_train, y_test = sklearn.model_selection.train_test_split(corpus, y, test_size=0.2)
    # векторайзер
    # vectorizer = sklearn.feature_extraction.text.CountVectorizer(ngram_range=(2,4), analyzer='char_wb')
    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(ngram_range=(2, 4), analyzer='char_wb', use_idf=True)
    X_train = vectorizer.fit_transform(corpus_train)
    X_test = vectorizer.transform(corpus_test)
    clf = sklearn.linear_model.RidgeClassifier(copy_X=True, max_iter=200)
    # clf = sklearn.ensemble.RandomForestClassifier()
    clf.fit(X_train, y_train)
    clf.score(X_test, y_test)

    return clf.predict(vectorizer.transform([text]))[0]

def bot(text):
    # открытие словаря
    try:
        # with open("Data-Bases/Data_Base.json", "r", encoding="utf-8") as file: 
        
        BOT_CONFIG = request_to_server("Data_Base")
        print(BOT_CONFIG)

    except:
        print("WARNING ⚠")

    intent = get_intent_by_model(text, BOT_CONFIG)
        
    return BOT_CONFIG['intents'][intent]['responses']
    

def echo(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    # Открытие словаря
    try:
        # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        #     data_all_users = json.load(file)
        data_all_users = request_to_server("Data_Users")

        print("1 step")

        user_data = data_all_users["users"]

        print("2 step")

        user_data = user_data[str(user["id"])]

        print("I've data")

    except:
        update.message.reply_text(emoji.emojize("Warninng in GET-DATA 1 :warning:\nPlease, write /error", language = 'alias' ))

    lang = user_data["language_code"] 
    print("LANG:", lang)

    id = user_data["id"]
    print("ID:", id)

    get_weather = user_data["get_weather"] 
    print("GET_WEATHER:",get_weather)

    get_url = user_data["get_url"] 
    print("GET_URL:", get_url)

    get_sentence = user_data["get_sentence"] 
    print("GET_SENTENCE:", get_sentence)

    get_qr = user_data["get_qr"] 
    print("GET_QR:", get_qr)

    print(1, not get_weather and not get_url and not get_sentence and not get_qr)
    print(2, get_weather and not get_url and not get_sentence and not get_qr)
    print(3, get_url and not get_weather and not get_sentence and not get_qr)
    print(4, get_sentence and not get_url and not get_weather and not get_qr)
    print(5, get_qr and not get_weather and not get_url and not get_sentence)

    """Echo the user message."""
    if not get_weather and not get_url and not get_sentence and not get_qr:
        add_message(1)

        input_text = update.message.text
        reply = bot(input_text)
        update.message.reply_text(reply)

        user_data["main"] = "online"
        saving_data_of_user(user, user_data)

    elif get_weather and not get_url and not get_sentence and not get_qr:
        add_message(1)

        rate_weather = user_data["rate_weather"] 
        print("rate_weather", rate_weather)

        if rate_weather == 1:
            city = update.message.text
            
            # Данного пользователя
            # data_user = {
            #     'last_name': user_data["first_name"], 
            #     'language_code': user_data["language_code"], 
            #     'id': str(user_data["id"]), 
            #     'username': user_data["username"], 
            #     'first_name': user_data["first_name"],
            #     'password': str(user_data["password"]),
            #     'points': str(user_data["points"]),
            #     'registered': str(user_data["registered"]),

            #     # Для внутренних процессов
            #     "main": "online",
            #     "get_weather": False,
            #     "rate_weather": 0,
            #     "city": city,
            #     }
            user_data["city"] = city
            user_data["main"] = "online"
            user_data["rate_weather"] = 0
            user_data["get_weather"] = False

            saving_data_of_user(user, user_data)
            
            try:
                data = requests.get((
                    f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
                )).json()

                # {"coord": {"lon": 37.6156, "lat": 55.7522}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds",
                #  "icon": "04d"}], "base": "stations", "main": {"temp": 9.57, "feels_like": 6.72, "temp_min": 5.75, "temp_max": 10.35, 
                #  "pressure": 1020, "humidity": 34, "sea_level": 1020, "grnd_level": 1002}, "visibility": 10000, "wind": {"speed": 5.94,
                #   "deg": 335, "gust": 6.75}, "clouds": {"all": 95}, "dt": 1652091338, "sys": {"type": 1, "id": 9027, "country": "RU", 
                #   "sunrise": 1652059798, "sunset": 1652116922}, "timezone": 10800, "id": 524901, "name": "Moscow", "cod": 200}

                city = data['name']

                country = data["sys"]["country"]
                description = data["weather"][0]["main"]
                visibility = data["visibility"]
                humidity = data["main"]["humidity"]

                cur_weather = data['main']['temp']
                wind = data['wind']['speed']
                sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
                sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
                # length_of_day = datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])
                length_of_day = sunset_timestamp - sunrise_timestamp
                
                
                # EMOJIZE
                    # Temperature
                if int(cur_weather) >= 15:
                    emoji_weather = ':sunny:'
                elif int(cur_weather) >= 0 and int(cur_weather) < 15:
                    emoji_weather = ':neutral_face:'
                else:
                    emoji_weather = ":snowflake:"

                    # Description
                if description == "Clouds":
                    emoji_description = ":cloud:"
                elif description == "Rain":
                    emoji_description = ":umbrella:"
                else:
                    emoji_description = ":partly_sunny:"

                    # Visibility
                emoji_visibility = ":foggy:"
                
                update.message.reply_text(emoji.emojize('***'+str(datetime.now().strftime('%Y-%m-%d :watch: %H:%M'))+'***', language = 'alias'))
                update.message.reply_text(emoji.emojize(f'Погода в городе: '+str(city)+', '+str(country)+' :house_with_garden:\nТемпература: '+str(cur_weather)+f"°C {emoji_weather}\nСкорость ветра: "+str(wind)+'м\с :dash:', language = 'alias'))
                update.message.reply_text(emoji.emojize(f"Описание: "+str(description)+f' {emoji_description}\nВидимость: '+str(visibility)+f' {emoji_visibility}\nВлажность: '+str(humidity)+' :droplet:', language = 'alias'))
                update.message.reply_text(emoji.emojize('Восход солнца: '+str(sunrise_timestamp)+' :sunrise:\nЗакат солнца: '+str(sunset_timestamp)+' :city_sunset:\nПродолжительность дня: '+str(length_of_day)+' :hourglass:', language = 'alias'))
                update.message.reply_text(emoji.emojize('Одевайся по погоде!) :necktie:',language = 'alias'))              

            except Exception as ex:
                update.message.reply_text("Warning in GET_WEATHER ⚠\nPlease, write /error")
                update.message.reply_text(data)   
                update.message.reply_text(str(ex))

    elif get_url and not get_weather and not get_sentence and not get_qr:
        add_message(1)

        url = update.message.text
        try:

            short = pyshorteners.Shortener()

            update.message.reply_text(emoji.emojize("Получившийся url-адрес: :sparkles:", language = 'alias'))
            update.message.reply_text(short.tinyurl.short((str(url))))

            user_data["main"] = "online"
            user_data["get_url"] = False
            saving_data_of_user(user, user_data)

        except Exception as ex:    
                
            update.message.reply_text("Warning in PRETTY URL ⚠\nPlease, write /error")
            update.message.reply_text(str(ex))

        # get_weather = user_data["get_weather"] 
        # print("GET_WEATHER:",get_weather)

        # get_url = user_data["get_url"] 
        # print("GET_URL:", get_url)
    
    elif get_sentence and not get_url and not get_weather and not get_qr:
        add_message(1)

        user_data["main"] = "online"
        user_data["get_sentence"] = False
        saving_data_of_user(user, user_data)

        # перевод на English
        translator = Translator(from_lang="ru", to_lang="en")
        sentence = translator.translate(update.message.text)
        
        print('Result on EN:', sentence)
 
        update.message.reply_text("Выполняю поиск по Wikipedia 🔎\nПожалуйста, подождите...") 
 
        # try:
        #     page = wikipedia.page(sentence)
           
        # except wikipedia.DisambiguationError as e:
        #     chosen = choice(e.options)
        #     page = wikipedia.page(chosen)
        #     update.message.reply_text("Слишком много страниц...\nРасскажу о "+str(page)) 

          
        print(lang)
        page = wiki_search.searching(sentence, lang)
        print(page)
        while True:
            try:
                request = wikipedia.summary(page, sentences=1)
                break
            except Exception as e:
                chosen = choice(e.options)
                page = wikipedia.page(chosen)

        request=re.sub('\([^()]*\)', '', request) 
        request=re.sub('\([^()]*\)', '', request) 
        request=re.sub('\{[^\{\}]*\}', '', request)

        
        update.message.reply_text(request) 
        try:
            # выбор файла
            # if len(wikipedia.page(request).images) >= 0:
            #     for i in range(len(wikipedia.page(request).images)):
            #         url = wikipedia.page(request).images[i]
                    
            #         if "png" in url:
            #             filename = f"wiki{id}.png"
            #             wget.download(url, filename)

            #             with open(filename, "rb") as file_send:
            #                 update.message.reply_photo(file_send)

            #             os.remove(filename)
            #             print(url)
            #             break

            # url = f"https://api.telegram.org/bot<{tlgrm_tocken}>/sendPhoto"
            # files = {'photo': open("templates/global_page/img/1st_pict.jpg", 'rb')}
            # data = {'chat_id' : "1010205515"}
            # r= requests.post(url, files=files, data=data)
            # print(r.json())

            # НАходим файлы через ГУГЛ
            filters = dict(
                type='photo'
            )

            # Записываем в папку
            crawler = GoogleImageCrawler(storage={'root_dir': f'./img_by_{id}'})
            
            # из запроса page вырезаем "wikipedia"
            print("REQUEST IS", str(page)[16:(len((str(page)))-2)])
            crawler.crawl(keyword=str(page)[16:(len((str(page)))-2)], max_num=5, filters=filters)
            
            # Отправляем кадый файл папки
            for filename in os.listdir(f'./img_by_{id}'):

                with open(os.path.join(f'./img_by_{id}', filename), 'rb') as file_send:
                    update.message.reply_photo(file_send)

            # Удаляем папку вместе со всеми ее файлами
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'./img_by_{id}')
            shutil.rmtree(path)


        except Exception as _Ex:
            update.message.reply_text("Warning in Wiki ⚠\nPlease, write /error") 
            print(_Ex)

    elif get_qr and not get_weather and not get_url and not get_sentence:
        add_message(1)

        smth = sentence = update.message.text
        try:
            filename = f"qrcode{id}.png"
            # создать экземпляр объекта QRCode
            qr = qrcode.QRCode(version=1, box_size=7, border=4)
            # добавить данные в QR-код
            qr.add_data(smth)
            # компилируем данные в массив QR-кода
            qr.make()
            # распечатать форму изображения
            print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
            # переносим массив в реальное изображение
            img = qr.make_image(fill_color="#eca1a6", back_color="black")
            # сохраняем в файл
            img.save(filename) 

            with open(filename, "rb") as file:
                update.message.reply_photo(file)
            os.remove(filename)

            user_data["main"] = "online"
            user_data["get_qr"] = False
            saving_data_of_user(user, user_data)

            # update.message.reply_text("Warning in QR ⚠\nPlease, write /error")


        except Exception as _Ex:
            update.message.reply_text("Warning in QR ⚠\nPlease, write /error")
            update.message.reply_text(str(_Ex))
       
def weather(update: Update, context: CallbackContext) -> None:
    add_message(3)

    user = update.effective_user

    # Открытие словаря
    try:
        # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        #     data_all_users = json.load(file)
        data_all_users = request_to_server("Data_Users")
        user_data = data_all_users["users"]
        user_data = user_data[str(user["id"])]

        print("I've data")

    except Exception as _Ex:
        update.message.reply_text("Warninng in GET-DATA 2 ⚠\nPlease, write /error")
        print(_Ex)

    user_data["rate_weather"] = 1
    user_data["get_weather"] = True
    user_data["main"] = "online"

    saving_data_of_user(user, user_data)
    
    update.message.reply_text(emoji.emojize("Введите город: :house:",language = 'alias'))

def smile(update: Update, context: CallbackContext) -> None:
    add_message(2)

    user = update.effective_user
    add_online(user)
    
    with open('Data-Bases-Tele/Data-Smiles.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        all_smiles = data["all_smiles"]

    random_smile = choice(all_smiles)
    update.message.reply_sticker(random_smile)
    update.message.reply_text(emoji.emojize("У меня очень мало стикеров(( Пришли мне пару своих..) :relaxed:\nЛишь "+str(len(all_smiles))+" стикера(-ов)", language = 'alias'))

def new_smile(update: Update, context: CallbackContext) -> None:
    add_message(2)

    user = update.effective_user
    add_online(user)

    with open('Data-Bases-Tele/Data-Smiles.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        all_smiles = data["all_smiles"]

    sticker_id = update.message.sticker.file_id
    

    all_smiles.append(sticker_id)

    with open('Data-Bases-Tele/Data-Smiles.json', 'w', encoding='utf-8') as file:
        data = {
            "all_smiles": all_smiles
        }
        json.dump(data, file, sort_keys = True)

    update.message.reply_text("Твой стик был успешно добавлен...) 😊")

def print_bio(update: Update, context: CallbackContext) -> None:
    add_message(3)

    user = update.effective_user
    add_online(user)
    
    try:
        # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        #     data_all_users = json.load(file)
        data_all_users = request_to_server("Data_Users")
        user_data = data_all_users["users"]
        user_data = user_data[str(user["id"])]

    except:
        update.message.reply_text("Warninng in BIO ⚠\nPlease, write /error")

    # update.message.reply_text("*** BIO ***")
    update.message.reply_text(emoji.emojize("*Имя:* "+str(user_data["first_name"])+" :bust_in_silhouette:", language = 'alias'), parse_mode='MarkdownV2' )
    update.message.reply_text(emoji.emojize("*Фамилия:* "+str(user_data["last_name"])+" :credit_card:", language = 'alias'), parse_mode='MarkdownV2')
    update.message.reply_text(emoji.emojize("*Предпочтительный язык:* "+str(user_data["language_code"])+" :tongue:", language = 'alias'), parse_mode='MarkdownV2')
    update.message.reply_text(emoji.emojize("*ID:* ||"+str(user_data["id"])+"|| :id:", language = 'alias'), parse_mode='MarkdownV2')
    update.message.reply_text(emoji.emojize("Логин: "+str(user_data["username"])+" :lock:", language = 'alias'))
    update.message.reply_text(emoji.emojize("*Пароль:* ||"+str(user_data["password"])+"|| :key:", language = 'alias'), parse_mode='MarkdownV2')
    update.message.reply_text(emoji.emojize("*Статус:* "+str(user_data["main"])+" :free:", language = 'alias'), parse_mode='MarkdownV2')
    update.message.reply_text(emoji.emojize("*Пост:* "+str(user_data["post"])+" :chart_with_upwards_trend:", language = 'alias'), parse_mode='MarkdownV2')
    update.message.reply_text(emoji.emojize("*Был зарегистрирован:* "+str(user_data["registered"])+" ⓡ", language = 'alias'), parse_mode='MarkdownV2')
    update.message.reply_text(emoji.emojize("*Roots:* "+str(user_data["points"])+" :deciduous_tree:", language = 'alias'), parse_mode='MarkdownV2')

    update.message.reply_text(emoji.emojize("Чтобы заработать Intent-ы переходи сюда:(url...) :link:", language = 'alias'))
    
def print_statistics(update: Update, context: CallbackContext) -> None:
    add_message(3)

    user = update.effective_user
    add_online(user)
    
    try:
        # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        #     data_all_users = json.load(file)
        data_all_users = request_to_server("Data_Users")
        users_data = data_all_users["users"]
        user_data = users_data[str(user["id"])]

    except Exception as ex:
        update.message.reply_text(str(ex)) 
        update.message.reply_text("Warninng in Statistics ⚠\nPlease, write /error") 

    counter_online = 0
    admin_counter = 0

    for user_for in users_data:

        fifteen_minutes = timedelta(minutes=15)

                        # перевод из str в date-time-format

        user_time = datetime.strptime(users_data[user_for]["was_online"], '%H:%M')

        now_time = datetime.strptime(str(datetime.now().strftime("%H:%M")), '%H:%M') 

        if users_data[user_for]["main"] == "online":
            
            # Если не совершал никаих действий более 15 минут
            # not user_time + fifteen_minutes <= now_time and not user_time + fifteen_minutes >= now_time:
                
            # Онлайн
            if user_time + fifteen_minutes >= now_time:
                if user_time - fifteen_minutes <= now_time:
                    print("User_time:", user_time+fifteen_minutes)
                    print("Now:", now_time)
                    print(users_data[user_for]["main"] == "online")
                    counter_online += 1

            # OFFLINE
            else:
                user_data["main"] = "off-line"
               
                print(users_data[user_for])

                saving_data_of_user(users_data[user_for], user_data)
 
        if users_data[user_for]["post"] == "Admin":
            admin_counter += 1

        print(1, user_time + fifteen_minutes <= now_time)
        print(2, user_time + fifteen_minutes >= now_time)
        
        print("User_time:", user_time+fifteen_minutes)
        print("Now:", now_time)

    update.message.reply_text(emoji.emojize("*Online:* "+str(counter_online)+" :iphone:", language = 'alias'), parse_mode='MarkdownV2')
    update.message.reply_text(emoji.emojize("*Admins:* "+str(admin_counter)+ "👨‍💻", language = 'alias'), parse_mode='MarkdownV2')

    # Добавить спрятанный текст
    update.message.reply_text(emoji.emojize("Общее количество пользователей, зарегистрированных в Future Forest: "+str(len(users_data))+" :busts_in_silhouette:", language = 'alias'))

# Обработка фотографий
def analyze_photo(update: Update, context: CallbackContext) -> None:
    add_message(1)

    user = update.effective_user
    add_online(user)
    
    update.message.reply_text("Photo was saved")
    
    # # текст айди
    # update.message.reply_text(str(photo_id))
    # # сама фотография
    # update.message.reply_photo(str(photo_id))

    with open('Data-Bases-Tele/Data-Photos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        all_photos = data["all_photos"]

    #  Уникальный айди фото
    photo_id = update.message.photo[0].file_id

    all_photos.append(photo_id)

    # добавление в json-файл
    with open('Data-Bases-Tele/Data-Photos.json', 'w', encoding='utf-8') as file:
        data = {
            "all_photos": all_photos
        }
        json.dump(data, file, sort_keys = True)
   
    # try:
    #     file_info = dispatcher.get_file(photo_id)
    #     downloaded_file = dispatcher.download_file(file_info.file_path)
    #     src='Data-Bases/'+file_info.file_path
    #     with open(src, 'wb') as new_file:
    #         new_file.write(downloaded_file)
    #         result_dict = DeepFace.analyze(new_file, actions=["emotion"])
    #     update.message.reply_text("Photo was added")


    #     result_dict = DeepFace.analyze(photo_id, actions=["age", "gender", "race", "emotion"])
    #     print(result_dict)
        

    # except Exception as _Ex:
    #     update.message.reply_text(str(_Ex))

# Проверка интернета
def ethernet_check(update: Update, context: CallbackContext) -> None:
    add_message(4)

    user = update.effective_user
    add_online(user)
    
    try:
        st = speedtest.Speedtest() 

        update.message.reply_text(emoji.emojize("Немного подождите...\nВыполняется проверка интернета :hourglass_flowing_sand:", language = 'alias'))

        #  Скачка
        update.message.reply_text("Скорость скачивания: ⤵\n"+str(st.download())+" Mbit/s")
        #  Загрузка
        update.message.reply_text("Скорость загрузки: ⤴\n"+str(st.upload())+" Mbit/s")
        #  Пинг
        servernames =[]   
        st.get_servers(servernames)       
        update.message.reply_text("Пинг: 🌐\n"+str(st.results.ping)+" ms")
    
    except Exception as _Ex:

        update.message.reply_text("Warning in ETHERNET-CHECK ⚠\nPlease, write /error")
        update.message.reply_text(str(_Ex))

def cute_url(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    add_message(2)

    # Открытие словаря
    try:
        # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        #     data_all_users = json.load(file)
        data_all_users = request_to_server("Data_Users")
        user_data = data_all_users["users"]
        user_data = user_data[str(user["id"])]

    except:
        update.message.reply_text("Warninng in GET-DATA 3 ⚠\nPlease, write /error")

    user_data["get_url"] = True
    user_data["main"] = "online"

    saving_data_of_user(user, user_data)

    update.message.reply_text(emoji.emojize("Введите ссылку: :link:", language = 'alias'))

def search_wiki(update: Update, context: CallbackContext) -> None:
    add_message(3)

    user = update.effective_user

    # Открытие словаря
    try:
        # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        #     data_all_users = json.load(file)
        data_all_users = request_to_server("Data_Users")
        user_data = data_all_users["users"]
        user_data = user_data[str(user["id"])]

    except:
        update.message.reply_text("Warninng in GET-DATA 4 ⚠\nPlease, write /error")

    user_data["get_sentence"] = True
    user_data["main"] = "online"

    saving_data_of_user(user, user_data)

    update.message.reply_text("Введите запрос: ℹ")

def qr_code(update: Update, context: CallbackContext) -> None:
    add_message(1)
    user = update.effective_user

    # Открытие словаря
    try:
        # with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        #     data_all_users = json.load(file)
        data_all_users = request_to_server("Data_Users")
        user_data = data_all_users["users"]
        user_data = user_data[str(user["id"])]

    except:
        update.message.reply_text("Warninng in GET-DATA 5 ⚠\nPlease, write /error")

    user_data["get_qr"] = True
    user_data["main"] = "online"

    saving_data_of_user(user, user_data)

    update.message.reply_text("Введите что-либо: ссылку, предложение, контакт... 📝")

def print_error(update: Update, context: CallbackContext) -> None:
    add_message(2)
    user = update.effective_user
    add_online(user)

    update.message.reply_text("В случае нахождения ошибок или неполадок в работе бота, просим писать модераторам группы Vk: ✍\nhttps://vk.com/only_number_one01")
    # update.message.reply_text("\x1b]8;;https://vk.com/only_number_one01\aВ случае нахождения ошибок или неполадок в работе бота, просим писать модераторам группы\x1b]8;;\a")

def print_info(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    add_online(user)
    add_message(3)
    
    # What can this bot do?


    string = '''· Возможность общения с чат-ботом 💬\n
· Получение погоды в любом городе ⛅\n 
· Отправка рандомного стикера, а также его сохранение в базу данных 📝\n
· Добавление пользователя в базу данных и показ его статистики и данных 🔐\n
· Статистика всех зарегистрированных пользователей 👥\n
· Создание более приятного url-адреса пользователя 📎\n
· Отправка данных пользователя о его соединении с интернетом 🌐\n
· Парсинг данных Википедии с целью ответа на запрос пользователя 🔎\n
· Создание Qr-code при любом значении ✍\n

· В случае обнаружения неполадок, существует возможность обратиться к модератору группы Vk ⚠
            '''

    update.message.reply_text("Функции Future Forest: 🌳")
    update.message.reply_text(string)



# Главная функция
def main() -> None:
    print("MAIN")

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Телеграмм токен
    updater = Updater(tlgrm_tocken)  

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
# СЛЕШОВЫЕ команды
  
    # on different commands - answer in Telegram

                #со смайлами (+)
    dispatcher.add_handler(CommandHandler("start", start)) # + 
    dispatcher.add_handler(CommandHandler("weather", weather)) # + 
    dispatcher.add_handler(CommandHandler("smile", smile)) # +
    dispatcher.add_handler(CommandHandler("bio", print_bio)) # +
    dispatcher.add_handler(CommandHandler("statistics", print_statistics)) # +    
    dispatcher.add_handler(CommandHandler("url", cute_url)) # + 
    dispatcher.add_handler(CommandHandler("ethernet", ethernet_check)) # +    
    dispatcher.add_handler(CommandHandler("wiki", search_wiki))    
    dispatcher.add_handler(CommandHandler("qr", qr_code))    
    dispatcher.add_handler(CommandHandler("error", print_error))    
    dispatcher.add_handler(CommandHandler("info", print_info))    
  
    dispatcher.add_handler(MessageHandler(Filters.sticker, new_smile))
    dispatcher.add_handler(MessageHandler(Filters.photo, analyze_photo))


    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
  # Цикл,который никогда не закончится,пока его не отстановишь
    updater.idle()

if __name__ == '__main__':
    main()

