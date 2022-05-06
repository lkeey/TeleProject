
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

import json
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
test_4()



