from abc import ABC,abstractmethod

class Iwriter(ABC):

    @abstractmethod
    def send_data(self,data):
        pass



