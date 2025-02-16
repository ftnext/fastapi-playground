from abc import ABC, abstractmethod


class FetchBooksPort(ABC):
    @abstractmethod
    def fetch(self):
        raise NotImplementedError
