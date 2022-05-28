from flask import Flask, render_template, redirect, url_for, request

import json

app = Flask(__name__)

# VARIABLES
amount_place = 3

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
    return top_place    

def save_intent(example, responce):
    # Добавление предложенных пользователем intent и responce

    with open("Data-Bases/Data_Base.json", "r", encoding='utf-8') as file:
        data = json.load(file)
        data_intents = data["intents"]

    data_intents[id] = {}
    data_intents[id]["examples"] = example
    data_intents[id]["responses"] = responce

    print(data_intents[id])

    with open('Data-Bases/Data_Base.json', 'w', encoding='utf-8') as file:
        data = {
                "intents": data_intents
                }
        json.dump(data, file, sort_keys = True)

    # Добавление опыта пользователю

    with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        # Весь
        data_all_users = json.load(file)
        user_data = data_all_users["users"]

    user_data[id]["points"] += 10

    with open('Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
        data = {
                "users": user_data
                }
        json.dump(data, file, sort_keys = True)

                # Функции для браузера
# Logging
@app.route("/log_in", methods=["GET"])
def index_page():
    return render_template("log_in/index.html")


# Global Page
@app.route("/form", methods=["GET"])
def form():
    # открытие словаря со всеми данными пользователей
    with open("Data-Bases/Data-users.json", "r", encoding='utf-8') as file:
        # Весь
        data_all_users = json.load(file)
        users_data = data_all_users["users"]
        data = users_data[id]
    return render_template("global_page/index.html", data_user=data, top_users=top_user, amount_place=amount_place)

                # Back-end
@app.route("/check_user", methods=["POST"])
def check_user():
    global data, top_user, id
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

                data = users_data[id]

                # Вычисление топа
                top_user = top(users_data)

                return redirect(url_for("form"))
                
        return "Password is incorrect"

    except Exception as _Ex:
        return str(_Ex)

@app.route("/send_intent", methods=["POST"])
def send_intent():
    topic = request.form["topic"]
    example = request.form["example"]
    responce = request.form["responce"]

    print("TOPIC", topic,"\nEXAMPLE", example,"\nRESPONCE", responce)
    if topic != '' and example != '' and responce != '':
        save_intent(example, responce)

    return redirect(url_for("form"))

# <!-- python script {%   %} -->

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)
