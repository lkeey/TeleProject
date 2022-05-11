# показывать дату регистрации

from random import *
from time import *
from datetime import datetime
import string
import secrets
import nltk
import json
import sklearn
import requests
from telegram import Update, ForceReply, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

with open('Technology/Data-Bases/Data-Smiles.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    all_smiles = data["all_smiles"]

# Variables
get_weather = False
rate_weather = 0
open_weather_token = '4da9f58fdb818e1b9979d5c95b2f2aaf'
user = None


# открытие словаря
try:
    with open("Technology/Data-Bases/Data_Base.json", "r", encoding="utf-8") as file:
        BOT_CONFIG = json.load(file)
except:
    print("WARNING")

print("Successfully")

def get_password():
    # 8 символов
    all_passwords = list()
    

    with open('Technology/Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        data_all_users = json.load(file)
        data_all_users = data_all_users["users"]
    for user in data_all_users:
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
        'registered': str(datetime.now().strftime("%D %H:%M:%C"))
        }

    try:
        with open('Technology/Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            data_all_users = json.load(file)
            data_all_users = data_all_users["users"]
    except:
        update.message.reply_text("Warning in open BASE-DATA")

    # если не зареган
    if not (data_user["id"] in data_all_users):
        data_all_users[data_user["id"]] = data_user
        try:
            with open('Technology/Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
                data = {
                        "users": data_all_users
                        }
                json.dump(data, file, sort_keys = True)
        except:
            update.message.reply_text("Warning in open data-user")

        update.message.reply_text("Вы были успешно зарегистрированы!")
    else:
        update.message.reply_text("С возвращением)\nВижу, вы уже были здесь зарегистрированы!")

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
    global city, rate_weather, get_weather
    """Echo the user message."""
    if not get_weather:
        input_text = update.message.text
        reply = bot(input_text)
        update.message.reply_text(reply)
    else:
        if rate_weather == 1:
            city = update.message.text
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
                cur_weather = data['main']['temp']
                wind = data['wind']['speed']
                sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
                sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
                # length_of_day = datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])
                length_of_day = sunset_timestamp - sunrise_timestamp
                update.message.reply_text('***'+str(datetime.now().strftime('%Y-%m-%d %H:%M'))+'***')
                update.message.reply_text('Погода в городе: '+str(city)+'\nТемпература: '+str(cur_weather)+'°C\nСкорость ветра: '+str(wind)+'м\с')
                update.message.reply_text('Восход солнца: '+str(sunrise_timestamp)+'\nЗакат солнца: '+str(sunset_timestamp)+'\nПродолжительность дня: '+str(length_of_day))
                update.message.reply_text('Одевайся по погоде!)')              

            except Exception as ex:
                update.message.reply_text("Warning in GET_WEATHER")
                update.message.reply_text(data)   
                update.message.reply_text(str(ex))

            rate_weather = 0
            get_weather = False
            
def weather(update: Update, context: CallbackContext) -> None:
    global get_weather, rate_weather
    rate_weather = 1
    get_weather = True

    if rate_weather == 1:
        update.message.reply_text("Write City:")

def smile(update: Update, context: CallbackContext) -> None:
    random_smile = choice(all_smiles)
    update.message.reply_sticker(random_smile)
    update.message.reply_text("у меня очень мало стикеров(( Пришли мне пару своих..)\nУ меня лишь "+str(len(all_smiles))+" стикера(-ов)")

def new_smile(update: Update, context: CallbackContext) -> None:

    sticker_id = update.message.sticker.file_id
    
    all_smiles.append(sticker_id)

    with open('Technology/Data-Bases/Data-Smiles.json', 'w', encoding='utf-8') as file:
        data = {
            "all_smiles": all_smiles
        }
        json.dump(data, file, sort_keys = True)

    update.message.reply_text("Твой стик был успешно добавлен...)")

def print_bio(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    try:
        with open('Technology/Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
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
    update.message.reply_text("Login: "+str(user_data["username"]))
    update.message.reply_text("Password: "+str(user_data["password"]))
    update.message.reply_text("Was registered: "+str(user_data["registered"]))
    update.message.reply_text("Intents: "+str(user_data["points"]))

    update.message.reply_text("Чтобы заработать Intent-ы переходи сюда:(url...)")
    

# Главная функция
def main() -> None:
    print("MAIN")

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Телеграмм токен
    updater = Updater("5366540233:AAEH04SZyyGE4uD7WvTHiRTXKxCvnQ-uqAM")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
# СЛЕШОВЫЕ команды
  
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("weather", weather))
    dispatcher.add_handler(CommandHandler("smile", smile))
    dispatcher.add_handler(CommandHandler("bio", print_bio))
    
    dispatcher.add_handler(MessageHandler(Filters.sticker, new_smile))

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