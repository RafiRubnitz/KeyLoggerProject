import keyboard
import time

class SpecialKeys:
    """
    This class accepts a string and swaps between special key names and what they actually do
    example:
    Instead - 'Hello~space~world'
    will be - 'Hello world'
    """

    def __init__(self):
        self.selector = {
            "altshift" : self.change_language(),
            "shiftalt" : self.change_language(),
            "shiftalt gr": self.change_language(),
            "spaceleft windows" : self.change_language(),
            "shifttab" : self.change_window(),
            "tabshift" : self.change_window(),
        }

    def process_list_of_data(self,data):
        for i in range(len(data)):
            for key,value in data[i].items():
                for key2,value2 in value.items():
                    data[i][key][key2] = self.process_of_arranging_string(value2)

        return data

    def process_of_arranging_string(self,string) -> str:
        string = self.replace_special_keys(string)
        string = self.rest_of_the_special_keys(string)
        return string

    @staticmethod
    def replace_special_keys(string):
        string = string.replace('~space~', ' ')
        string = string.replace('~tab~', '\t')
        string = string.replace('~enter~', '\n')
        return string

    def rest_of_the_special_keys(self,string) -> str:
        string = string.split("~")
        new_string = ""
        for word in string:
            if word == "":
                continue
            if word == "backspace":
                if new_string:
                    new_string = new_string[:-1]
                    continue
            if word in self.selector:
                new_string += self.selector[word]
            else:
                new_string += word
        return new_string

    def change_language(self):
        return "(change language)"

    def change_window(self):
        return "(change window)"

    def movement_keys(self):
        pass

    def double_keys(self):
        pass





