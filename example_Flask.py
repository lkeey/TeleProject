# кортежи
from collections import namedtuple

# связанное в Flask-ом
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__) 


Message = namedtuple("Message", "text tag")
messages = list()

@app.route("/", methods=["GET"])
def hello_world():
    # передача html
    return render_template("template_example.html")

@app.route("/main", methods=["GET"])
def main():
    return render_template("template_main_example.html", messages=messages)


@app.route("/add_message", methods=["POST"])
def add_message():
# при получении нового сообщения, оно перенаправляется на страницу main
    
    # text и tag из html
    text = request.form["text"]
    tag = request.form["tag"]
    messages.append(Message(text, tag))

    return redirect(url_for("main"))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
