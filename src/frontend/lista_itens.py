import customtkinter as ctk
from backend.Log import Log
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.tela import Tela

class ListaItens(ctk.CTkScrollableFrame):
    def __init__(self, master: Type["Tela"]) -> None:
        super().__init__(master)
        self._aplicativo = master._aplicativo
        self._widgets = {}
        self.configure(fg_color="#4B0082", corner_radius=6)

        # Decorativos


        # Interativos
        