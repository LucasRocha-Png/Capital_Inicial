import customtkinter as ctk
from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.aplicativo import Aplicativo

class Tela(ctk.CTkFrame, ABC):
    def __init__(self, master: Type["Aplicativo"]) -> None:
        super().__init__(master)
        self._aplicativo = master
        self._widgets = {}
    
    # Chamado sempre que a tela é exibida
    @abstractmethod
    def evento_exibido(self) -> None:
        pass
