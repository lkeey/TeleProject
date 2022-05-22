#           Оложено:
# Фотографии

#           Разрабатывается
# Работа с текстом (озвучка)
# Работа с голосовыми сообщениями
# Админ и обычный 

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


# Variables
open_weather_token = '4da9f58fdb818e1b9979d5c95b2f2aaf'
tlgrm_tocken = "5366540233:AAEH04SZyyGE4uD7WvTHiRTXKxCvnQ-uqAM"

# открытие словаря
try:
    with open("Data-Bases/Data_Base.json", "r", encoding="utf-8") as file:
        BOT_CONFIG = json.load(file)
except:
    print("WARNING")

print("Successfully")

def saving_data_of_user(user, data):

    # Открытие словаря
    try:
        with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            # Весь
            data_all_users = json.load(file)
            user_data = data_all_users["users"]
            # Пользователя
            user_data = user_data[str(user["id"])]

    except:
        print("НЕВОЗМОЖНО ОТКРЫТЬ!")
    
    print("G-W",data["get_weather"])

    print("URL:", data["get_url"])

    print("WAS_ONLINE", data["was_online"])

    print("User-data-MAIN", data["main"])

    if data["main"] == "online":
        data_all_users["users"][str(user["id"])]["was_online"] = str(datetime.now().strftime("%H:%M"))
    
    data_all_users["users"][str(user["id"])]["main"] = data["main"]
    
    print("Main", user["id"], data["main"])

    print("MAIN:", data_all_users["users"][str(user["id"])]["main"])
    data_all_users["users"][str(user["id"])]["rate_weather"] = data["rate_weather"]
    data_all_users["users"][str(user["id"])]["get_weather"] = data["get_weather"]
    data_all_users["users"][str(user["id"])]["get_url"] = data["get_url"]

    try:
        with open('Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
            data = {
                    "users": data_all_users["users"]
                    }
            json.dump(data, file, sort_keys = True)
    except:
        print("НЕ ОТКРЫВАЕТСЯ")

def add_online(user):
    # Открытие словаря
    try:
        with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            data_all_users = json.load(file)
            user_data = data_all_users["users"]
            user_data = user_data[str(user["id"])]

    except:
        print("НЕ ОТКРЫВАЕТСЯ")

    user_data["main"] = "online"

    saving_data_of_user(user, user_data)

def get_password():
    # 8 символов
    all_passwords = list()
    
    with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        data_all_users = json.load(file)
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
        # Future-Forest, [5/10/2022 3:59 PM]
        # Hi Лёша Кирюшин!

        # Future-Forest, [5/10/2022 3:59 PM]
        # [Лёша Кирюшин](tg://user?id=1010205515)\!  
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    update.message.reply_text(fr'{user.mention_markdown_v2()}\!') 

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
        "post": "User"
        }

    try:
        with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            data_all_users = json.load(file)
            data_all_users = data_all_users["users"]
    except:
        update.message.reply_text("Warning in open BASE-DATA")

    # если не зареган
    if not (data_user["id"] in data_all_users):
        data_all_users[data_user["id"]] = data_user
        try:
            with open('Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
                data = {
                        "users": data_all_users
                        }
                json.dump(data, file, sort_keys = True)
        except:
            update.message.reply_text("Warning in open data-user")

        update.message.reply_text("Вы были успешно зарегистрированы!")
    else:
        
        update.message.reply_text("С возвращением)\nВижу, вы уже были здесь зарегистрированы!")
    # update.message.reply_text(str(len(data_all_users)))
        # Остальные сообщения
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

    # подписка к векторайзеру
def get_intent_by_model(text):
    return clf.predict(vectorizer.transform([text]))[0]

def bot(text):
    intent = get_intent_by_model(text)
    if intent != 'intent not found:(':
        return choice(BOT_CONFIG['intents'][intent]['responses'])
    else:
        return 'Некорректная форма вопроса!'

def echo(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    # Открытие словаря
    try:
        with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            data_all_users = json.load(file)
            user_data = data_all_users["users"]
            user_data = user_data[str(user["id"])]

    except:
        update.message.reply_text("Warninng in GET-DATA")

    get_weather = user_data["get_weather"] 
    print("GET_WEATHER:",get_weather)

    get_url = user_data["get_url"] 
    print("GET_URL:", get_url)

    print(1, not get_weather and not get_url)
    print(2, get_weather and not get_url)
    print(3, get_url and not get_weather)

    """Echo the user message."""
    if not get_weather and not get_url:
        
        input_text = update.message.text
        reply = bot(input_text)
        update.message.reply_text(reply)

    elif get_weather and not get_url:
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
                update.message.reply_text('***'+str(datetime.now().strftime('%Y-%m-%d %H:%M'))+'***')
                update.message.reply_text('Погода в городе: '+str(city)+', '+str(country)+'\nТемпература: '+str(cur_weather)+'°C\nСкорость ветра: '+str(wind)+'м\с')
                update.message.reply_text("Описание: "+str(description)+'\nВидимость: '+str(visibility)+'\nВлажность: '+str(humidity))
                update.message.reply_text('Восход солнца: '+str(sunrise_timestamp)+'\nЗакат солнца: '+str(sunset_timestamp)+'\nПродолжительность дня: '+str(length_of_day))
                update.message.reply_text('Одевайся по погоде!)')              

            except Exception as ex:
                update.message.reply_text("Warning in GET_WEATHER")
                update.message.reply_text(data)   
                update.message.reply_text(str(ex))

        get_weather = user_data["get_weather"] 
        print("GET_WEATHER:",get_weather)

        get_url = user_data["get_url"] 
        print("GET_URL:", get_url)

    elif get_url and not get_weather:
        url = update.message.text
        try:

            short = pyshorteners.Shortener()

            update.message.reply_text("Получившийся url-адрес:")
            update.message.reply_text(short.tinyurl.short((str(url))))

            user_data["main"] = "online"
            user_data["get_url"] = False
            saving_data_of_user(user, user_data)

        except Exception as ex:        
            update.message.reply_text(str(ex))

        get_weather = user_data["get_weather"] 
        print("GET_WEATHER:",get_weather)

        get_url = user_data["get_url"] 
        print("GET_URL:", get_url)
            
def weather(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    # Открытие словаря
    try:
        with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            data_all_users = json.load(file)
            user_data = data_all_users["users"]
            user_data = user_data[str(user["id"])]

    except:
        update.message.reply_text("Warninng in GET-DATA")

    user_data["rate_weather"] = 1
    user_data["get_weather"] = True
    user_data["main"] = "online"

    saving_data_of_user(user, user_data)
    
    update.message.reply_text("Write City:")

def smile(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    add_online(user)
    
    with open('Data-Bases/Data-Smiles.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        all_smiles = data["all_smiles"]

    random_smile = choice(all_smiles)
    update.message.reply_sticker(random_smile)
    update.message.reply_text("у меня очень мало стикеров(( Пришли мне пару своих..)\nУ меня лишь "+str(len(all_smiles))+" стикера(-ов)")

def new_smile(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    add_online(user)

    with open('Data-Bases/Data-Smiles.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        all_smiles = data["all_smiles"]

    sticker_id = update.message.sticker.file_id
    

    all_smiles.append(sticker_id)

    with open('Data-Bases/Data-Smiles.json', 'w', encoding='utf-8') as file:
        data = {
            "all_smiles": all_smiles
        }
        json.dump(data, file, sort_keys = True)

    update.message.reply_text("Твой стик был успешно добавлен...)")

def print_bio(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    add_online(user)
    
    try:
        with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            data_all_users = json.load(file)
            user_data = data_all_users["users"]
            user_data = user_data[str(user["id"])]

    except:
        update.message.reply_text("Warninng in BIO")

    update.message.reply_text("*** BIO ***")
    update.message.reply_text("Имя: "+str(user_data["first_name"]))
    update.message.reply_text("Фамилия: "+str(user_data["last_name"]))
    update.message.reply_text("Предпочтительный язык: "+str(user_data["language_code"]))
    update.message.reply_text("ID: "+str(user_data["id"]))
    update.message.reply_text("Логин: "+str(user_data["username"]))
    update.message.reply_text("Пароль: "+str(user_data["password"]))
    update.message.reply_text("Статус: "+str(user_data["main"]))
    update.message.reply_text("Пост "+str(user_data["post"]))
    update.message.reply_text("Был зарегистрирован: "+str(user_data["registered"]))
    update.message.reply_text("Intent-ы: "+str(user_data["points"]))

    update.message.reply_text("Чтобы заработать Intent-ы переходи сюда:(url...)")
    
def print_statistics(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    try:
        with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            data_all_users = json.load(file)
            users_data = data_all_users["users"]
            user_data = users_data[str(user["id"])]

    except Exception as ex:
        update.message.reply_text(str(ex)) 
        update.message.reply_text("Warninng in Statistics") 

    counter_online = 0
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
                print("User_time:", user_time+fifteen_minutes)
                print("Now:", now_time)
                print(users_data[user_for]["main"] == "online")
                counter_online += 1

            # OFFLINE
            else:
                user_data["main"] = "off-line"
               
                print(users_data[user_for])

                saving_data_of_user(users_data[user_for], user_data)
 
        print(1, user_time + fifteen_minutes <= now_time)
        print(2, user_time + fifteen_minutes >= now_time)
        
        print("User_time:", user_time+fifteen_minutes)
        print("Now:", now_time)

    update.message.reply_text("Online: "+str(counter_online))

    # Добавить спрятанный текст
    update.message.reply_text("Общее количество пользователей, зарегистрированных в Future Forest: "+str(len(users_data)))

# Обработка фотографий
def analyze_photo(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    add_online(user)
    
    update.message.reply_text("Photo was saved")
    
    # # текст айди
    # update.message.reply_text(str(photo_id))
    # # сама фотография
    # update.message.reply_photo(str(photo_id))

    with open('Data-Bases/Data-Photos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        all_photos = data["all_photos"]

    #  Уникальный айди фото
    photo_id = update.message.photo[0].file_id

    all_photos.append(photo_id)

    # добавление в json-файл
    with open('Data-Bases/Data-Photos.json', 'w', encoding='utf-8') as file:
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
    user = update.effective_user
    add_online(user)
    
    try:
        st = speedtest.Speedtest() 

        update.message.reply_text("Немного подождите...\nВыполняется проверка интернета")

        #  Скачка
        update.message.reply_text("Скорость скачивания:\n"+str(st.download())+" Mbit/s")
        #  Загрузка
        update.message.reply_text("Скорость загрузки:\n"+str(st.upload())+" Mbit/s")
        #  Пинг
        servernames =[]   
        st.get_servers(servernames)       
        update.message.reply_text("Пинг:\n"+str(st.results.ping)+" ms")
    except Exception as _Ex:
        update.message.reply_text(str(_Ex))

def cute_url(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    # Открытие словаря
    try:
        with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            data_all_users = json.load(file)
            user_data = data_all_users["users"]
            user_data = user_data[str(user["id"])]

    except:
        update.message.reply_text("Warninng in GET-DATA")

    user_data["get_url"] = True
    user_data["main"] = "online"

    saving_data_of_user(user, user_data)

    update.message.reply_text("Write Url:")

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
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("weather", weather))
    dispatcher.add_handler(CommandHandler("smile", smile))
    dispatcher.add_handler(CommandHandler("bio", print_bio))
    dispatcher.add_handler(CommandHandler("statistics", print_statistics))    
    dispatcher.add_handler(CommandHandler("url", cute_url))
    dispatcher.add_handler(CommandHandler("ethernet", ethernet_check))    
        
    


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
