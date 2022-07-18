from os import urandom
from flask import Flask, render_template, redirect, url_for, request, session
import json
import os 
from datetime import datetime
from base64 import b64encode

import simplejson as json

app = Flask(__name__)

# VARIABLES
amount_place = 2
id = 0
key = ''
secret_key = '=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD, =EF=BF=BD=EF=BF=BD =EF=BF==BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF==BD =EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD =EF=BF=BD=EF==BF=BD =EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD=EF==BF=BD=EF=BF=BD=EF=BF=BD=EF=BF=BD'


app.config['SECRET_KEY'] = os.urandom(32)

            # Функции для back-end
def top(users_data):

    points_list = list()

    dict_users = {
        # user: points
    }

    for user in users_data: 
        dict_users[users_data[user]["username"]] = users_data[user]["points"]
        points_list.append(users_data[user]["points"])

    top_place = list()

    # количество мест
    for i in range(len(users_data)):
        # Наивысшее место
        the_most_place = max(points_list)
        points_list.remove(the_most_place)

        for user in dict_users:
            if dict_users[user] == the_most_place:
                name_1st = user
                
                top_place.append(name_1st)

                del dict_users[user]
                break

    print("top_places", top_place)

    return top_place    

def save_intent(example, responce):
    try:
        # Добавление опыта пользователю
        print("Experience")

        with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
            # Весь
            data_all_users = json.load(file)
            user_data = data_all_users["users"]
        
        user_data[id]["points"] += 3

        with open('Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
            data = {
                    "users": user_data
                    }
            json.dump(data, file, sort_keys = True)

        print("INTENT")
        # Добавление предложенных пользователем intent и responce

        with open("Data-Bases/Data_Base.json", "r", encoding='utf-8') as file:
            data = json.load(file)
            data_intents = data["intents"]

        name_topic = f"{id}_{str(user_data[id]['points'])}"

        data_intents[name_topic] = {}
        data_intents[name_topic]["examples"] = example.split("/")
        data_intents[name_topic]["responses"] = responce.split("/")

        print(data_intents[name_topic])

        with open('Data-Bases/Data_Base.json', 'w', encoding='utf-8') as file:
            
            data = {
                    "intents": data_intents
                    }
            json.dump(data, file, sort_keys = True)

        print("END INTENT")

    except Exception as _Ex:
        print("Warning in saving", _Ex)
        return False

    return True

                # Функции для браузера
# main

@app.route("/<int:id>", methods=["GET"])
@app.route("/", methods=["GET"])
def main_page(id=0):

    if not session.modified:
        session["verificat_key"] = b64encode(os.urandom(1)).decode('utf-8')
        session.modified = True

    print("ID", id)
    
    with open('Data-Bases/Data-Amount.json', 'r', encoding='utf-8') as file:
        data_amount = json.load(file)["months"]
    

        for month in data_amount:
            print(f"{month} - {data_amount[month]['users']} users - {data_amount[month]['messages']} messages - {data_amount[month]['intents']} intents")

    return render_template("main.html",data_month=data_amount, id=id, verificat_key=session["verificat_key"])

# Logging
@app.route("/logging/<key>", methods=["GET", "POST"])
def logging_page(key=''):
    global top_user
    print(f"{key} - {session['verificat_key']}")
    if session["verificat_key"] == key: 
        if not session.modified:
            session.modified = True
        session["verificat_key"] = b64encode(os.urandom(1)).decode('utf-8')
        print(f"Logging: Incorrect verificate key\nKey is {key} - {session['verificat_key']}")
    
        if request.method == "POST":

            # login-пользователя
            login = request.form["login"]
            # password-пользователя
            password = request.form["password"]
            print("Login",login,"\nPASSWORD",password)

            try:
            # открытие словаря со всеми данными пользователей
                with open("Data-Bases/Data-users.json", "r", encoding='utf-8') as file:
                    # Весь
                    data_all_users = json.load(file)
                    users_data = data_all_users["users"]

                for id in users_data:
                    if login == users_data[id]["username"]:
                        if users_data[id]["password"] == password:

                            # data = users_data[id]

                            # Вычисление топа
                            top_user = top(users_data)
                            print("ID", id)

                            return redirect(f'/{id}')    

                return render_template("logging.html", success=False, verificat_key=session["verificat_key"])

            except Exception as _Ex:
                print("Warning in logging:\n", _Ex)

        return render_template("logging.html", success=True, verificat_key=session["verificat_key"])
    
    print(f"Logging: Incorrect verificate key\nKey is {key} - {session['verificat_key']}")
    try:
        return redirect(f'/{id}') 
    except:
        return redirect(f'/{0}')

# Global Page
@app.route("//create/<key>", methods=["GET","POST"])
@app.route("/<int:id>/create/<key>", methods=["GET","POST"])
def form(id=0, key=''):
    print("ID", id)
    if session["verificat_key"] == key:
        if not session.modified:
            session.modified = True
        session["verificat_key"] = b64encode(os.urandom(1)).decode('utf-8')
            
        if id == 0:
            return redirect(f'/logging/{session["verificat_key"]}') 

        # открытие словаря со вsсеми данными пользователей
        
        try:
            
            if request.method == "POST":
                topic = request.form["topic"]
                example = request.form["example"]
                responce = request.form["responce"]

                print("TOPIC", topic,"\nEXAMPLE", example,"\nRESPONCE", responce)
                
                if topic != '' and example != '' and responce != '':
                    # 
                    try:
                        # Добавление опыта пользователю
                        print("Experience")

                        with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
                            # Весь
                            data_all_users = json.load(file)
                            user_data = data_all_users["users"]
                        
                        user_data[str(id)]["points"] += 3

                        with open('Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
                            data = {
                                    "users": user_data
                                    }
                            json.dump(data, file, sort_keys = True)

                        print("INTENT")
                        # Добавление предложенных пользователем intent и responce

                        with open("Data-Bases/Data_Base.json", "r", encoding='utf-8') as file:
                            data = json.load(file)
                            data_intents = data["intents"]

                        name_topic = f"{str(id)}_{str(user_data[str(id)]['points'])}"

                        data_intents[name_topic] = {}
                        data_intents[name_topic]["examples"] = example
                        data_intents[name_topic]["responses"] = responce

                        print(data_intents[name_topic])

                        with open('Data-Bases/Data_Base.json', 'w', encoding='utf-8') as file:
                            
                            data = {
                                    "intents": data_intents
                                    }
                            json.dump(data, file, sort_keys = True)


                        # Добавление интентов за день
                        
                        print("Add Intent Count")
                        with open("Data-Bases/Data-day.json", "r", encoding='utf-8') as file:
                            data_day = json.load(file)
                            if f'{datetime.now().strftime("%m%d")}' not in data_day:
                                data_day[f'{datetime.now().strftime("%m%d")}'] = {}
                                data_day[f'{datetime.now().strftime("%m%d")}']["intents"] = 0
                                data_day[f'{datetime.now().strftime("%m%d")}']["users"] = 0
                                data_day[f'{datetime.now().strftime("%m%d")}']["messages"] = 0

                            data_day[f'{datetime.now().strftime("%m%d")}']["intents"] += 3
                            
                        with open('Data-Bases/Data-day.json', 'w', encoding='utf-8') as file:
                            json.dump(data_day, file, sort_keys = True)

                        # Добавление интента в data-amount
                        with open("Data-Bases/Data-Amount.json", "r", encoding='utf-8') as file:
                            data_day = json.load(file)["months"]
                            print("Month", datetime.now().strftime("%m"))
                            print("Data", data_day[f'{datetime.now().strftime("%m")}'])
                            
                            data_day[f'{datetime.now().strftime("%m")}']["intents"] += 3

                        with open("Data-Bases/Data-Amount.json", "w", encoding='utf-8') as file:
                            data = {"months": data_day}
                            
                            json.dump(data, file, sort_keys = True)

                        print("END INTENT")

                    except Exception as _Ex:
                        print("Warning in saving", _Ex)
                        return render_template("index.html",id=id, verificat_key=session["verificat_key"])

                    return redirect(f'/{id}')  

                return render_template("index.html",id=id, verificat_key=session["verificat_key"])
            
            return render_template("index.html",id=id, verificat_key=session["verificat_key"])

        except Exception as _Ex:
            print("Warning in Save Intent", _Ex)
            return render_template("index.html",id=id, data_user=data,verificat_key=session["verificat_key"])
    
    print(f"Create: Incorrect verificate key\nKey is{key} - {session['verificat_key']}")
    
    return redirect(f'/{id}') 

@app.route("//profile/<key>", methods=["GET","POST"])
@app.route("/<int:id>/profile/<key>", methods=["GET"])
def show_profile(id=0, key=''):
    print("ID", id)
    
    if session["verificat_key"] == key:
        if not session.modified:
            session.modified = True
        session["verificat_key"] = b64encode(os.urandom(1)).decode('utf-8')
      

        if id == 0:
            return redirect(f'/logging/{session["verificat_key"]}') 

        with open("Data-Bases/Data-users.json", "r", encoding='utf-8') as file:
            # Весь
            data_all_users = json.load(file)
            users_data = data_all_users["users"]
            data = users_data[str(id)]

        with open("Data-Bases/Data-users.json", "r", encoding='utf-8') as file:
            # Весь
            data_all_users = json.load(file)
            users_data = data_all_users["users"]

        top_user = top(users_data)

        counter = 0

        for user in top_user:
            counter += 1
            if user == users_data[str(id)]["username"]:
                break


        return render_template("profile.html",id=id, data_user=data, top_user=top_user[:amount_place], place_num=counter, verificat_key=session["verificat_key"])

    print(f"Profile: Incorrect verificate key\nKey is{key} - {session['verificat_key']}")

    return redirect(f'/{id}') 

@app.route("//about", methods=["GET","POST"])
@app.route("/<int:id>/about", methods=["GET"])
def show_about(id=0):
    if not session.modified:
        session.modified = True
    session["verificat_key"] = b64encode(os.urandom(1)).decode('utf-8')

    with open("Data-Bases/Data-day.json", "r", encoding='utf-8') as file:
        # Весь
        data_day = json.load(file)

        # Даты нет в словаре
        if f'{datetime.now().strftime("%m%d")}' not in data_day:
            data_day[f'{datetime.now().strftime("%m%d")}'] = {}
            data_day[f'{datetime.now().strftime("%m%d")}']["intents"] = 0
            data_day[f'{datetime.now().strftime("%m%d")}']["users"] = 0
            data_day[f'{datetime.now().strftime("%m%d")}']["messages"] = 0
       
        if f'{datetime.now().strftime("%m")+str(int(datetime.now().strftime("%d"))-1)}' not in data_day:
            data_day[f'{datetime.now().strftime("%m")+str(int(datetime.now().strftime("%d"))-1)}'] = {}
            data_day[f'{datetime.now().strftime("%m")+str(int(datetime.now().strftime("%d"))-1)}']["intents"] = 0
            data_day[f'{datetime.now().strftime("%m")+str(int(datetime.now().strftime("%d"))-1)}']["users"] = 0
            data_day[f'{datetime.now().strftime("%m")+str(int(datetime.now().strftime("%d"))-1)}']["messages"] = 0

        
            with open('Data-Bases/Data-day.json', 'w', encoding='utf-8') as file:
                json.dump(data_day, file, sort_keys = True)

        current_data = data_day[f'{datetime.now().strftime("%m%d")}']

        yesterday_data = data_day[f'{datetime.now().strftime("%m")+str(int(datetime.now().strftime("%d"))-1)}']
        print("data_day", current_data)
        print("yestaerday_data", yesterday_data)

    # Выбираем значки
    sign_list = list()

    if current_data["messages"] > yesterday_data["messages"]:
        sign_list.append("img/uparrow_78484.png")

    elif current_data["messages"] < yesterday_data["messages"]:
        sign_list.append("img/arrowdown_flech_1539.png")
    
    else:
        sign_list.append("img/calculate_equals_icon_194844.png")    


    if current_data["users"] > yesterday_data["users"]:
        sign_list.append("img/uparrow_78484.png")

    elif current_data["users"] < yesterday_data["users"]:
        sign_list.append("img/arrowdown_flech_1539.png")
    
    else:
        sign_list.append("img/calculate_equals_icon_194844.png")


    if current_data["intents"] > yesterday_data["intents"]:
        sign_list.append("img/uparrow_78484.png")

    elif current_data["intents"] < yesterday_data["intents"]:
        sign_list.append("img/arrowdown_flech_1539.png")
    
    else:
        sign_list.append("img/calculate_equals_icon_194844.png")


    with open("Data-Bases/Data-Amount.json", "r", encoding='utf-8') as file:
        amount_users = 0
        amount_messages = 0
        amount_intents = 0

        data_months = json.load(file)["months"]

        for month in data_months:
            amount_users += data_months[month]["users"]
            amount_messages += data_months[month]["messages"]
            amount_intents += data_months[month]["intents"]

    return render_template("about.html",sign_list=sign_list, id=id, amount_intents=amount_intents, amount_users=amount_users, amount_messages=amount_messages, current_data=current_data, yesterday_data=yesterday_data, verificat_key=session["verificat_key"] )

@app.route("//support", methods=["GET","POST"])
@app.route("/<int:id>/support", methods=["GET"])
def show_support(id=0):
    if not session.modified:
        session.modified = True
    session["verificat_key"] = b64encode(os.urandom(1)).decode('utf-8')

    return render_template("support.html", id=id, verificat_key=session["verificat_key"])

    # Возвращают словари 

# Словарь ИНТЕНТОВ
@app.route("/get/Data_Base/<string:key>/", methods=["GET"])
def Get_Data_Base(key):
    print("KEY", key)
    if key == secret_key:
    
        if request.method == "GET":

            try:
                with open("Data-Bases/Data_Base.json", "r", encoding="utf-8") as file:
                    BOT_CONFIG = json.load(file)

                    return BOT_CONFIG

            except Exception as _EX:
                return("WARNING ⚠\n"+str(_EX) )

# Словарь Данных Пользователей
@app.route("/get/Data_Users/<string:key>/", methods=["GET", "POST"])
def Get_Data_Users(key):
    global data_all_users

    print("KEY", key)
    if key == secret_key:
        if request.method == "POST":
            try:

                json_file = json.loads(request.get_json())['json']

                print("Success get json")

                print("REQUEST", json_file)

                with open('Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:

                    json.dump(json_file, file, sort_keys = True)
                    
                print("Success save json")

                return render_template("json_get.html", data=data_all_users,)
                
            except Exception as _EX: 
                return "FAIL \n" + str(_EX)

        elif request.method == "GET":
            
            try:
                with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
                    # Весь
                    data_all_users = json.load(file)

                    return data_all_users

            except Exception as _EX:
                return("WARNING ⚠\n"+str(_EX) )

# Словарь Данных за День
@app.route("/get/Data_Day/<string:key>/", methods=["GET", "POST"])
def Get_Data_Day(key):
    global data_day

    print("KEY", key)
    if key == secret_key:
        if request.method == "POST":
            try:
                
                json_file = json.loads(request.get_json())['json']

                print("REQUEST", json_file)

                with open("Data-Bases/Data-day.json", "w", encoding='utf-8') as file:
                    json.dump(json_file, file, sort_keys = True)

                return render_template("json_get.html",data=data_day,)
                
            except Exception as _EX: 
                return "FAIL \n" + str(_EX)

        elif request.method == "GET":

            try:
                with open("Data-Bases/Data-day.json", "r", encoding='utf-8') as file:
                    data_day = json.load(file)

                    return data_day

            except Exception as _EX:
                return("WARNING ⚠\n"+str(_EX) )


# Словарь Данных за Весь период
@app.route("/get/Data_Amount/<string:key>/", methods=["GET", "POST"])
def Get_Data_Amount(key):
    global data_amount

    print("KEY", key)
    if key == secret_key:
        if request.method == "POST":
            try:
                # получаем json-file
                # print("1st", type(request.form['json']))
                # print("2nd", type(json.loads(request.form['json'])))

                json_file = json.loads(request.get_json())['json']

                print("REQUEST", json_file)

                with open("Data-Bases/Data-Amount.json", "w", encoding='utf-8') as file:

                    json.dump(json_file, file, sort_keys = True)

                return render_template("json_get.html",data=data_amount,)
                
            except Exception as _EX: 
                return "FAIL \n" + str(_EX)

        elif request.method == "GET":

            try:
                with open("Data-Bases/Data-Amount.json", "r", encoding='utf-8') as file:
                    data_amount = json.load(file)["months"]
                    
                    return data_amount

            except Exception as _EX:
                return("WARNING ⚠\n"+str(_EX) )


if __name__ == '__main__':
      app.run(debug=True)
