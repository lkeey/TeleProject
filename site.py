from flask import Flask, render_template, redirect, url_for, request
import json
from datetime import datetime

app = Flask(__name__)

# VARIABLES
amount_place = 2
id = 0

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
    for i in range(amount_place):
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
    print("ID", id)
    

    with open('Data-Bases/Data-Amount.json', 'r', encoding='utf-8') as file:
        data_amount = json.load(file)["months"]
    

        for month in data_amount:
            print(f"{month} - {data_amount[month]['users']} users - {data_amount[month]['messages']} messages - {data_amount[month]['intents']} intents")

    return render_template("main.html",data_month=data_amount, id=id)

# Logging
@app.route("/logging", methods=["GET", "POST"])
def logging_page():
    global top_user
    if request.method == "POST":


        # id-пользователя
        id = request.form["id"]

        password = request.form["password"]
        print("ID",id,"\nPASSWORD",password)

        try:
        # открытие словаря со всеми данными пользователей
            with open("Data-Bases/Data-users.json", "r", encoding='utf-8') as file:
                # Весь
                data_all_users = json.load(file)
                users_data = data_all_users["users"]

            if id in users_data:
                if users_data[id]["password"] == password:

                    # data = users_data[id]

                    # Вычисление топа
                    top_user = top(users_data)
                    print("ID", id)

                    return redirect(f'/{id}')    

            return "Password is incorrect"

        except Exception as _Ex:
            print("Warning in logging:\n", _Ex)

    return render_template("logging.html")


# Global Page
@app.route("//create", methods=["GET","POST"])
@app.route("/<int:id>/create", methods=["GET","POST"])
def form(id=0):
    print("ID", id)
    if id == 0:
        return redirect('/logging') 

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
                    return render_template("index.html",id=id, )

                return redirect(f'/{id}')  

            return render_template("index.html",id=id, )
        
        return render_template("index.html",id=id, )

    except Exception as _Ex:
        print("Warning in Save Intent", _Ex)
        return render_template("index.html",id=id, data_user=data)

@app.route("//profile", methods=["GET","POST"])
@app.route("/<int:id>/profile", methods=["GET"])
def show_profile(id=0):
    print("ID", id)
    if id == 0:
        return redirect('/logging') 

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
    place = None

    for user in top_user:
        counter += 1
        if user == users_data[str(id)]["username"]:
            place = counter

    with open("Data-Bases/Data-day.json", "r", encoding='utf-8') as file:
        # Весь
        data_day = json.load(file)
        current_data = data_day[f'{datetime.now().strftime("%d")}']
        yesterday_data = data_day[f'{int(datetime.now().strftime("%d"))-1}']
        print("data_day", current_data)
        print("yestaerday_data", yesterday_data)

    return render_template("profile.html",current_data=current_data, yesterday_data=yesterday_data ,id=id, data_user=data, top_user=top_user, place_num=place)

if __name__ == '__main__':
      app.run(debug=True)
