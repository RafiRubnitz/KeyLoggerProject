from writer import Iwriter
import requests

class NetworkWriter(Iwriter):

    def __init__(self):
        self.urls = ["http://127.0.0.1:5000/api/upload"]

    def send_data(self,data) -> bool:
        response = requests.post(self.urls[0],json=data)
        try:
            response = response.json()
            if response["message"] == "stop":
                return True
            return False
        except:
            return False