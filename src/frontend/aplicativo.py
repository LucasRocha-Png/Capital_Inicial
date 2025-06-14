import customtkinter as ctk
import tkinter.font as tkfont

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
        self.__frames = {}
        self.__usuario_atual = None
        self.__ultimo_frame = None
        self.__tamanho_desktop = (self.winfo_screenwidth(), self.winfo_screenheight())

        # Configurações de tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("data/themes/capital_inicial.json")

        # Configurações da janela principal
        self.title("Capital Inicial")
        self.redimensionar(*self.__tamanho_desktop)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.encerrar) # Chama 'encerrar' ao fechar a janela

        # Inicializa todos os frames
        for frame_subclasse in (TelaLogin,):
            nome = frame_subclasse.__name__
            frame = frame_subclasse(self) # Passa este objeto Aplicativo como "master" do frame
            self.__frames[nome] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.exibir_frame("TelaLogin")
    
    def redimensionar(self, largura: int, altura: int) -> None:
        if largura <= 0 or altura <= 0:
            raise ValueError("Largura e altura não positivas.")
        elif largura > self.__tamanho_desktop[0] or altura > self.__tamanho_desktop[1]:
            raise ValueError(f"Largura ou altura excedem o tamanho do desktop. ({self.__tamanho_desktop[0]}x{self.__tamanho_desktop[1]})")
        self.geometry(f"{largura}x{altura}")

    # Coloca o frame especificado em primeiro plano
    def exibir_frame(self, nome: str) -> None:
        if nome in self.__frames:
            frame = self.__frames[nome]
            self.__ultimo_frame = frame
            frame.tkraise()
            frame.evento_exibido()
        else:
            raise ValueError(f"Frame '{nome}' não existe.")
    
    # Chamado sempre ao fechar o aplicativo
    def encerrar(self) -> None:
        if self.__usuario_atual:
            print("aplicativo.py — Salvar usuário atual antes de encerrar.")
        self.destroy()
