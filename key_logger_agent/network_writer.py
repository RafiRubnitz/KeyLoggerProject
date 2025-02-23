from writer import IWriter
import requests

class NetworkWriter(IWriter):

    def __init__(self,host:str):
        # self.urls = ["http://127.0.0.1:5000/api/upload"]
        self.host = host

    def send_data(self,data) -> bool:
        response = requests.post(self.host + "/api/upload",json=data)
        try:
            response = response.json()
            if response["message"] == "stop":
                return True
            return False
        except:
            return False