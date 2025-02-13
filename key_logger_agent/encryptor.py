

class Encryptor:

    def __init__(self):
        self.key = "A"

    def xor(self,data):
        def _xor(string):
            new_str = ''
            for i in string:
                new_str += chr((ord(i) ^ ord(self.key)) + 65)
            return new_str

        encrypt_data = {}
        for window_name, val in data.items():
            new_window_name = _xor(window_name)
            encrypt_data[new_window_name] = {}

            for time_line, str_val in val.items():
                new_time_line = _xor(time_line)
                new_str_val = _xor(str_val)
                encrypt_data[new_window_name][new_time_line] = new_str_val

        return encrypt_data


    def decrypt_xor(self,data):
        pass

