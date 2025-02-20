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
        pass

    def process_list_of_data(self,data):
        for i in range(len(data)):
            for key,value in data[i].items():
                for key2,value2 in value.items():
                    data[i][key][key2] = self.process_of_arranging_string(value2)

        return data

    def process_of_arranging_string(self,string) -> str:
        string = self.replace_special_keys(string)
        # string = self.rest_of_the_special_keys(string)
        return string

    @staticmethod
    def replace_special_keys(string):
        string = string.replace('~space~', ' ')
        string = string.replace('~tab~', '\t')
        string = string.replace('~enter~', '\n')
        return string

    def rest_of_the_special_keys(self,string) -> str:
        string = string.split("~")

    def delete_key(self,string):
        pass

    def movement_keys(self):
        pass

    def double_keys(self):
        pass





