import customtkinter as ctk
from ..frame import Frame
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from ..aplicativo import Aplicativo

class TelaLogin(Frame):
    def __init__(self, master: Type["Aplicativo"]):
        super().__init__(master)
        label_usuario = ctk.CTkLabel(self, text="E-mail")
        entry_usuario = ctk.CTkEntry(self, placeholder_text="Digite seu e-mail")
        label_senha = ctk.CTkLabel(self, text="Senha")
        entry_senha = ctk.CTkEntry(self, placeholder_text="Digite sua senha", show="*")
        button_entrar = ctk.CTkButton(self, text="Entrar", command=self.evento_entrar)
        label_cadastrar = ctk.CTkLabel(self, text="Ainda não tem uma conta?")
        button_cadastrar = ctk.CTkButton(self, text="Cadastrar", command=self.evento_tela_cadastro)

        label_usuario.pack(pady=(10, 0))
        entry_usuario.pack(pady=(0, 10))
        label_senha.pack(pady=(10, 0))
        entry_senha.pack(pady=(0, 10))
        button_entrar.pack(pady=(10, 5))
        label_cadastrar.pack(pady=(20, 0))
        button_cadastrar.pack(pady=(0, 10))
    
    def evento_exibido(self) -> None:
        print("login.py — Registrar no log que a tela de login foi exibida.")
    
    def evento_entrar(self) -> None:
        print("login.py — Registrar no log que o usuário tentou entrar.")
    
    def evento_tela_cadastro(self) -> None:
        self._aplicativo.exibir_frame("TelaCadastro")
