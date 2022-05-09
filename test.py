import json

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
