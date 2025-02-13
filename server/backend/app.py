import json
import os
from flask import Flask,jsonify,request
import time

app = Flask(__name__)

@app.route('/')
def home():
    pass

@app.route("/api/upload",methods=['POST'])
def upload():

    data = request.get_json()

    #ניהול שגיאות
    if error_manager(data):
        return jsonify({"error" : "error","message" : data})

    #קבלת הנתונים המתאימים
    folder_name = data["mac_name"].replace(":","_")
    new_data = data["data"]

    #להחזיר את ההצפנה לנתונים המקוריים


    #לעשות על הנתונים פרוסס


    #יצירת תיקיה למחשב הנתון
    open_new_folder(folder_name)

    #יצירת נתיב ליצירת קובץ
    file_path = folder_name + '\\' + generate_json_file()

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
    with open(file_path,'w') as file:
        json.dump(data,file,indent=4)

def get_data_from_DB():
    pass

@app.route("/api/data",methods=['GET'])
def get_data():
    pass

if __name__ == '__main__':
    app.run(debug=True,port=5000)

