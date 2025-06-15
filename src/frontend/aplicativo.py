import customtkinter as ctk

from .telas.login import TelaLogin
"""
from .telas.cadastro import TelaCadastro
from .telas.dashboard import TelaDashboard
from .telas.acoes_disponiveis import TelaAcoesDisponiveis
from .telas.acoes_possuidas import TelaAcoesPossuidas
from .telas.historico import TelaHistorico
"""

class Aplicativo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.__telas = {}
        self.__usuario_atual = None
        self.__ultima_tela = None
        self.__tamanho_desktop = (self.winfo_screenwidth(), self.winfo_screenheight())

        # Configurações de tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("data/themes/capital_inicial.json")

        # Configurações da janela principal
        self.title("Capital Inicial")
        self.redimensionar(*self.__tamanho_desktop)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.encerrar) # Chama 'encerrar' ao fechar a janela

        # Inicializa todas as telas
        for tela_subclasse in (TelaLogin,):
            nome = tela_subclasse.__name__
            tela = tela_subclasse(self) # Passa este objeto Aplicativo como "master" da tela
            self.__telas[nome] = tela
            tela.grid(row=0, column=0, sticky="nsew")
        
        self.exibir_tela("TelaLogin")
    
    @property
    def tamanho_desktop(self) -> tuple[int, int]:
        return self.__tamanho_desktop
    
    def redimensionar(self, largura: int, altura: int) -> None:
        if largura <= 0 or altura <= 0:
            raise ValueError("Largura e altura não positivas.")
        elif largura > self.__tamanho_desktop[0] or altura > self.__tamanho_desktop[1]:
            raise ValueError(f"Largura ou altura excedem o tamanho do desktop. ({self.__tamanho_desktop[0]}x{self.__tamanho_desktop[1]})")
        self.geometry(f"{largura}x{altura}")

    # Coloca a tela especificada em primeiro plano
    def exibir_tela(self, nome: str) -> None:
        if nome in self.__telas:
            tela = self.__telas[nome]
            self.__ultima_tela = tela
            tela.lift()
            tela.evento_exibido()
        else:
            raise ValueError(f"Tela '{nome}' não existe.")
    
    # Chamado sempre ao fechar o aplicativo
    def encerrar(self) -> None:
        if self.__usuario_atual:
            print("aplicativo.py — Salvar usuário atual antes de encerrar.")
        self.destroy()
