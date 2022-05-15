import json
from datetime import datetime, timedelta

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


def test_6():
    smile_1st = "cAAVK_mSpW_9hfOrH4cTWckQ"
    smile_2nd = "p_csFbW_3MgAABA5JOLqR-Pg"
    print(len(smile_1st))
    smile_3rd = "CAACAgIAAxkBAAIBUmJ5eJCiqOh0O8UL-puFfhUxtxfLAAKWDAACC1sZSkTJo0Tt48bJJAQ"
    count = 0
    for i in range(len(smile_1st)):
        if smile_1st[i] != smile_2nd[i]:
            count += 1
    print(count)
    print(smile_1st == smile_2nd)



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
        'password': "ygh$!78",
        'points': 0,
        'registered': str(datetime.now().strftime("%D %H:%M:%C")),

        # Для внутренних процессов
        "main": "online",
        "get_weather": False,
        "rate_weather": 0,
        "city": "DEFAULT",
        "was_online": str(datetime.now().strftime("%H:%M"))
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

    with open('Technology/Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
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
        
test_6()
