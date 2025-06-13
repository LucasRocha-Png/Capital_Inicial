# Python
from abc import ABC, abstractmethod

class Manager(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def carregar(self):
        pass

    @abstractmethod
    def salvar(self):
        pass

    @abstractmethod
    def atualizar(self):
        pass