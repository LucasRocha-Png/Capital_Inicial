import customtkinter as ctk
from backend.Log import Log
from frontend.tela import Tela
from frontend.dashboard import Dashboard
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.aplicativo import Aplicativo

class TelaAcoesDisponiveis(Tela):
    def __init__(self, master: Type["Aplicativo"]) -> None:
        super().__init__(master)
        self.__dashboard = Dashboard(self)
        
        # Layout dos frames principais
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # O tamanho do dashboard depende do tamanho do desktop
        desktop = self._aplicativo.tamanho_desktop
        dashboard_pady = (0, int(desktop[1] * 0.88))
        self.__dashboard.grid(row=0, column=0, sticky="nsew", pady=dashboard_pady)

    def evento_exibido(self) -> None:
        Log.trace("Tela de ações disponíveis exibida.")
        self.__dashboard.atualizar()

