import customtkinter as ctk
from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from .aplicativo import Aplicativo

class Frame(ctk.CTkFrame, ABC):
    def __init__(self, master: Type["Aplicativo"]):
        super().__init__(master)
        self._aplicativo = master
        self._widgets = {}
    
    # Chamado sempre que o frame é exibido
    @abstractmethod
    def evento_exibido(self) -> None:
        pass
