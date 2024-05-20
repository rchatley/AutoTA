from abc import ABC, abstractmethod


class Catalogue(ABC):
    @abstractmethod
    def search_for(self, query):
        pass
