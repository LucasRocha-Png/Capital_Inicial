import customtkinter as ctk
from PIL import Image

from database.ManagerUsuarios import ManagerUsuarios
from database.ManagerAcao import ManagerAcao
from backend.Log import Log
from backend.Usuarios import Usuario
from backend.Corretora import Corretora
from frontend.telas.login import TelaLogin
from frontend.telas.cadastro import TelaCadastro
from frontend.telas.acoes_disponiveis import TelaAcoesDisponiveis
from frontend.telas.acoes_possuidas import TelaAcoesPossuidas

from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from backend.Usuarios import Usuario

class Aplicativo(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.__telas = {}
        self.__usuario_atual = None
        self.__tamanho_desktop = (self.winfo_screenwidth(), self.winfo_screenheight())
        self.__imagens = {
            "image_background": ctk.CTkImage(light_image=Image.open("data/images/background_login.png"), size=self.__tamanho_desktop),
            "image_logo": ctk.CTkImage(light_image=Image.open("data/images/logo.png"), size=(300, 300)),
            "image_senha_oculta": ctk.CTkImage(light_image=Image.open("data/images/senha_oculta.png"), size=(24, 24)),
            "image_senha_revelada": ctk.CTkImage(light_image=Image.open("data/images/senha_revelada.png"), size=(24, 24)),
            "image_saldo": ctk.CTkImage(light_image=Image.open("data/images/saldo.png"), size=(60, 60)),
            "image_acoes": ctk.CTkImage(light_image=Image.open("data/images/acoes.png"), size=(60, 60)),
            "image_detalhes": ctk.CTkImage(light_image=Image.open("data/images/detalhes.png"), size=(60, 60)),
            "image_historico": ctk.CTkImage(light_image=Image.open("data/images/historico.png"), size=(60, 60)),
            "image_background_dashboard": ctk.CTkImage(light_image=Image.open("data/images/background_dashboard.png"), size=self.__tamanho_desktop)
        }
        self.__manager_usuarios = ManagerUsuarios()
        self.__manager_acao = ManagerAcao()
        self.__corretora = Corretora()
        
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
        Log.trace("Inicializando o aplicativo...")
        for tela_subclasse in (TelaLogin, TelaCadastro, TelaAcoesDisponiveis, TelaAcoesPossuidas):
            nome = tela_subclasse.__name__
            tela = tela_subclasse(self) # Passa este objeto Aplicativo como "master" da tela
            self.__telas[nome] = tela
            tela.grid(row=0, column=0, sticky="nsew")
            Log.trace(f"Desenhando tela '{nome}'...")
        
        self.exibir_tela("TelaLogin")
    
    @property
    def tamanho_desktop(self) -> tuple[int, int]:
        return self.__tamanho_desktop
    
    @property
    def imagens(self) -> dict[str, ctk.CTkImage]:
        return self.__imagens
    
    @property
    def manager_usuarios(self) -> Type[ManagerUsuarios]:
        return self.__manager_usuarios
    
    @property
    def manager_acao(self) -> Type[ManagerAcao]:
        return self.__manager_acao
    
    @property
    def corretora(self) -> Type[Corretora]:
        return self.__corretora
    
    @property
    def usuario_atual(self) -> Type[Usuario]:
        return self.__usuario_atual
    
    @usuario_atual.setter
    def usuario_atual(self, usuario: Type[Usuario] | None) -> None:
        if usuario is None or isinstance(usuario, Usuario):
            self.__usuario_atual = usuario
        else:
            erro = "Usuário inválido. Deve ser uma instância de Usuario ou None."
            Log.error(erro)
            raise ValueError(erro)

    def redimensionar(self, largura: int, altura: int) -> None:
        if largura <= 0 or altura <= 0:
            erro = "Largura e altura devem ser positivas."
            Log.error(erro)
            raise ValueError(erro)
        elif largura > self.__tamanho_desktop[0] or altura > self.__tamanho_desktop[1]:
            erro = f"Largura ou altura excedem o tamanho do desktop. ({self.__tamanho_desktop[0]}x{self.__tamanho_desktop[1]})"
            Log.error(erro)
            raise ValueError(erro)
        self.geometry(f"{largura}x{altura}")

    # Coloca a tela especificada em primeiro plano
    def exibir_tela(self, nome: str) -> None:
        if nome in self.__telas:
            tela = self.__telas[nome]
            tela.lift()
            tela.evento_exibido()
        else:
            erro = f"Tela '{nome}' não existe."
            Log.error(erro)
            raise ValueError(erro)
    
    # Chamado sempre ao fechar o aplicativo
    def encerrar(self) -> None:
        Log.trace("Encerrando o aplicativo...")
        if self.__usuario_atual:
            self.__manager_usuarios.salvar(self.__usuario_atual)
        self.destroy()
