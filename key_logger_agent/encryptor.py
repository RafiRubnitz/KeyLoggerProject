class Encryptor:

    def __init__(self,key:str):
        self.key = key

    def encrypt(self,data:dict) -> dict:

        def _xor(string):
            new_str = ''
            #לא השתמשנו בlist comparison כי המתודה join לא מקבלת ערכים כאלה
            for i in string:
                new_str += chr((ord(i) ^ ord(self.key)))
            return new_str

        encrypt_data = {}
        for key, val in data.items():
            new_key = _xor(key)
            if isinstance(val,dict):
                encrypt_data[new_key] = self.encrypt(val)
            else:
                new_val = _xor(val)
                encrypt_data[new_key] = new_val

        return encrypt_data


    def decrypt(self,data:dict) -> dict:
        return self.encrypt(data)

