from writer import IWriter
import json

class FileWriter(IWriter):

    def send_data(self,data):
        try:
            with open('DB.json', 'r') as f:
                exists_data = json.load(f)
        except:
            exists_data = {}

        exists_data.update(data)
        with open('DB.json','w') as f:
            json.dump(exists_data,f,indent=4)

