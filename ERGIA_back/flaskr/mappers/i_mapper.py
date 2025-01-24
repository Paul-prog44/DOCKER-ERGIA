from abc import abstractmethod


class Mapper:
    @abstractmethod
    def map(self, data):
        pass