from writer import IWriter
import requests

class NetworkWriter(IWriter):

    def __init__(self,host:str):
        self.host = host

    def send_data(self,data:dict) -> str:
        try:
            #שליחת המידע לשרת
            response = requests.post(self.host + "/api/upload",json=data,timeout=5)
            #קבלת תשובה
            response_json = response.json()

            #בדיקה האם להפסיק
            if response_json["message"] == "stop":
                return "stop"
            #בדיקה האם להמשיך
            elif response_json["message"] == "success":
                return "continue"
            #בדיקה האם הייתה שגיאה
            else:
                return "error"
        #אם קרתה שגיאה
        except Exception as e:
            print(e)
            return "error"