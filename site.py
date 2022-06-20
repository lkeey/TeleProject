from flask import Flask, render_template, redirect, url_for, request
import json
app = Flask(__name__)

# VARIABLES
amount_place = 3
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
    # Добавление опыта пользователю

    with open('Data-Bases/Data-users.json', 'r', encoding='utf-8') as file:
        # Весь
        data_all_users = json.load(file)
        user_data = data_all_users["users"]
    
    user_data[id]["points"] += (len(example.split("/")) + len(responce.split("/")))*2

    with open('Data-Bases/Data-users.json', 'w', encoding='utf-8') as file:
        data = {
                "users": user_data
                }
        json.dump(data, file, sort_keys = True)

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

                # Функции для браузера
# main

@app.route("/<int:id>", methods=["GET"])
@app.route("/", methods=["GET"])
def main_page(id=0):
    print("ID", id)
    with open("Data-Bases/Data-users.json", "r", encoding='utf-8') as file:
        # Весь
        data_all_users = json.load(file)
        users_data = data_all_users["users"]

    top_user = top(users_data)

    return render_template("main.html", top_users=top_user, id=id)

# Logging
@app.route("/logging", methods=["GET", "POST"])
def logging_page():
    global top_user
    if request.method == "POST":

        # get data

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

                    return redirect(f'/{id}/create')    

            return "Password is incorrect"

        except Exception as _Ex:
            print("Warning in logging:\n", _Ex)

    return render_template("logging.html")


# Global Page
@app.route("/<int:id>/create", methods=["GET","POST"])
def form(id):
    if id == 0:
        return redirect('/logging') 

    # открытие словаря со вsсеми данными пользователей
    
    try:
        with open("Data-Bases/Data-users.json", "r", encoding='utf-8') as file:
            # Весь
            data_all_users = json.load(file)
            users_data = data_all_users["users"]
            data = users_data[str(id)]
       

        if request.method == "POST":
            topic = request.form["topic"]
            example = request.form["example"]
            responce = request.form["responce"]

            print("TOPIC", topic,"\nEXAMPLE", example,"\nRESPONCE", responce)
            if topic != '' and example != '' and responce != '':
                save_intent(example, responce)

                return redirect(f'/{id}')  

        return render_template("index.html",id=id, data_user=data, top_users=top_user)

    except:
        return redirect('/logging') 

                # Back-end
# @app.route("/check_user", methods=["POST"])
# def check_user():
#     global data, top_user, id
#     id = request.form["id"]
#     password = request.form["password"]
#     print("ID",id,"\nPASSWORD",password)

#     try:
#         # открытие словаря со всеми данными пользователей
#         with open("Data-Bases/Data-users.json", "r", encoding='utf-8') as file:
#             # Весь
#             data_all_users = json.load(file)
#             users_data = data_all_users["users"]

#         if id in users_data:
#             if users_data[id]["password"] == password:

#                 data = users_data[id]

#                 # Вычисление топа
#                 top_user = top(users_data)

#                 return redirect(url_for("form"))
                
#         return "Password is incorrect"

#     except Exception as _Ex:
#         return str(_Ex)

# @app.route("/send_intent", methods=["POST"])
# def send_intent():
#     topic = request.form["topic"]
#     example = request.form["example"]
#     responce = request.form["responce"]

#     print("TOPIC", topic,"\nEXAMPLE", example,"\nRESPONCE", responce)
#     if topic != '' and example != '' and responce != '':
#         save_intent(example, responce)

#     return redirect(url_for("form"))

# <!-- python script {%   %} -->

if __name__ == '__main__':
      app.run(debug=True)
