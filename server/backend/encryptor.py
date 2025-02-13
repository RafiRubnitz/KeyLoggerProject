

class Encryptor:

    def __init__(self):
        self.key = "A"

    def xor(self,data):
        def _xor(string):
            new_str = ''
            for i in string:
                new_str += chr((ord(i) ^ ord(self.key)))
            return new_str

        encrypt_data = {}
        for key, val in data.items():
            new_key = _xor(key)
            if isinstance(val, dict):
                encrypt_data[new_key] = self.xor(val)
            else:
                new_val = _xor(val)
                encrypt_data[new_key] = new_val

        return encrypt_data

    def decrypt_xor(self,data):
        return self.xor(data)



