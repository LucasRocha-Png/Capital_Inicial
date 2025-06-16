import customtkinter as ctk
from backend.Log import Log
from frontend.tela import Tela
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.aplicativo import Aplicativo

class TelaDashboard(Tela):
    def __init__(self, master: Type["Aplicativo"]) -> None:
        super().__init__(master)

    def evento_exibido(self) -> None:
        Log.trace("Dashboard exibido.")
    
