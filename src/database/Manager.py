# Python
from abc import ABC, abstractmethod

class Manager(ABC):
    def __init__(self) -> None:
        pass

    # SETTERS AND GETTERS -----------------------
    @abstractmethod
    def listar(self) -> None:
        pass

    @abstractmethod
    def salvar(self) -> None:
        pass

    @abstractmethod
    def carregar(self) -> None:
        pass
    # -------------------------------------------