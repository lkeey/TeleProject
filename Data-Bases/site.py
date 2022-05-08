from flask import Flask, request, render_template
# для определения времени
from datetime import datetime
import json

app = Flask(__name__, template_folder='templates')  # still relative to module

                # для json файла

db_file = "Data-Bases\Data_Base.json"  
# Путь к файлу 
json_db = open(db_file, "rb")  # Открываем файл 
data_base = json.load(json_db)  # Загружаем данные из файла
intents_list = data_base["intents"]  # Берем сообщения из структуры и кладем в переменную


# Функция сохранения сообщений в файл
def save_intents():
    # Создаем структуру
    data = {
        "intents": intents_list,
    }
    # Открываем файл на запись
    json_db = open(db_file, "w")
    json.dump(data, json_db)  # Записываем данные в файл


# Функция, выводящая одно сообщение
def print_message(message):
    print(f"[{message['sender']}]: {message['text']} / {message['date']}")
    print("-" * 50)


# Функция добавления нового сообщения
def add_message(example, response, topic):
    intents = {
        topic:{
            "examples": example,
            "responses": response,
        }   
    }
    intents_list.append(intents) 
 # Добавляем новое сообщение в список
    print("intents_list",intents_list)

                                     # Функции для браузера
# Главная страница
@app.route("/")
def index_page():
    return "Hello, welcome to TeleWeb"


# Раздел со списком сообщений
@app.route("/get_intents")
def get_messages():
    return {"intents": intents_list} 


# Раздел для отправки сообщения
@app.route("/send_intents")
def send_intents():
    example = request.args["examples"]
    responce = request.args["responses"]

    if len(example) > 100 or len(example) < 2:
        return "ERROR"

    if len(responce) > 1000 or len(responce) == 0:
        return "ERROR"

    add_message(example, responce)
    save_intents()  # Сохраняем все сообщение в файл
    return "Your message was sent"


# Раздел с визуальным интерфейсом
@app.route("/form")
def form():
    return render_template("index.html")

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)


