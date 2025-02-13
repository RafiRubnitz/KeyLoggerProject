import keyboard

class SpecialKeys:
    """
    This class accepts a string and swaps between special key names and what they actually do
    example:
    Instead - 'Hello~space~world'
    will be - 'Hello world'
    """

    def __init__(self):
        pass

    def process_of_arranging_string(self,string) -> str:
        string = self.replace_special_keys(string)
        string = self.rest_of_the_special_keys(string)
        return string

    def replace_special_keys(self,string):
        string = string.replace('~space~', ' ')
        string = string.replace('~tab~', '\t')
        string = string.replace('~enter~', '\n')
        return string

    def rest_of_the_special_keys(self,string):
        pass

    def delete_key(self,string):
        pass

    def movement_keys(self):
        pass

    def double_keys(self):
        pass






