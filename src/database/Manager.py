# Python
from abc import ABC, abstractmethod

class Manager(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def listar(self) -> list:
        pass

    @abstractmethod
    def salvar(self) -> None:
        pass

    @abstractmethod
    def carregar(self) -> None:
        pass