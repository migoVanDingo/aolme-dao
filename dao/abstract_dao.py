from abc import ABC, abstractmethod


class AbstractDao(ABC):
    @abstractmethod
    def get_list(self, params):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def add(self, payload):
        pass

    @abstractmethod
    def update(self, payload):
        pass

    @abstractmethod
    def delete(self, id):
        pass