import customtkinter as ctk
from PIL import Image
from ..tela import Tela
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from ..aplicativo import Aplicativo

class TelaCadastro(Tela):
    def __init__(self, master: Type["Aplicativo"]):
        super().__init__(master)

        # Decorativos
        image_background = ctk.CTkImage(light_image=Image.open("data/images/background_login.png"), size=self._aplicativo.tamanho_desktop)
        tamanho_logo = 300
        image_logo = ctk.CTkImage(light_image=Image.open("data/images/logo.png"), size=(tamanho_logo, tamanho_logo))
        label_background = ctk.CTkLabel(self, image=image_background, text="")
        label_logo = ctk.CTkLabel(self, image=image_logo, text="")
        frame_login = ctk.CTkFrame(self, fg_color="#4B0082", corner_radius=6)
        label_usuario = ctk.CTkLabel(frame_login, text="E-mail", anchor="w", text_color="white")
        label_senha = ctk.CTkLabel(frame_login, text="Senha", anchor="w", text_color="white")
        label_cadastrar = ctk.CTkLabel(frame_login, text="Ainda não tem uma conta?", anchor="w", text_color="white")

        # Interativos
        altura = 38
        entry_usuario = ctk.CTkEntry(frame_login, placeholder_text="Digite seu e-mail", height=altura)
        entry_senha = ctk.CTkEntry(frame_login, placeholder_text="Digite sua senha", show="*", height=altura)
        image_mostrar_senha = ctk.CTkImage(light_image=Image.open("data/images/mostrar_senha.png"), size=(24, 24))
        button_mostrar_senha = ctk.CTkButton(frame_login, text="", image=image_mostrar_senha, command=lambda: entry_senha.configure(show="" if entry_senha.cget("show") else "*"), width=25, height=25, fg_color="white", hover=False, border_width=0, corner_radius=0)
        button_entrar = ctk.CTkButton(frame_login, text="Entrar", command=self.evento_entrar, height=altura)
        button_cadastrar = ctk.CTkButton(frame_login, text="Cadastrar", command=self.evento_tela_cadastro, fg_color="white", text_color="#9370DB", height=altura)

        # Guarda widgets necessários posteriormente
        self._widgets["entry_senha"] = entry_senha

        # Layout dos widgets de background
        label_background.grid(row=0, column=0, sticky="nsew")
        logo_rely = 0.17
        label_logo.place(relx=0.50, rely=logo_rely, anchor="center")

        # Layout do frame de login
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # O tamanho do frame depende do tamanho do desktop
        desktop = self._aplicativo.tamanho_desktop
        login_padx = int(desktop[0] * 0.38)
        login_pady = int(desktop[1] * 0.30)
        frame_login.grid(row=0, column=0, sticky="nsew", padx=login_padx, pady=login_pady)

        # Layout dos widgets de login
        frame_login.columnconfigure(0, weight=1)
        for linha in range(8):
            peso = 0 if linha != 5 else 1 # Linha 5 é vazia
            frame_login.rowconfigure(linha, weight=peso)
        margem = 35
        espacamento = margem // 4
        label_usuario.grid(row=0, column=0, sticky="w", padx=margem, pady=(margem, 0))
        entry_usuario.grid(row=1, column=0, sticky="ew", padx=margem, pady=(0, espacamento))
        label_senha.grid(row=2, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        entry_senha.grid(row=3, column=0, sticky="ew", padx=margem, pady=(0, espacamento * 2))
        button_mostrar_senha.grid(row=3, column=0, sticky="e", padx=(0, margem+5), pady=(0, espacamento * 2))
        button_entrar.grid(row=4, column=0, sticky="ew", padx=margem, pady=(espacamento * 2, margem))
        label_cadastrar.grid(row=6, column=0, sticky="w", padx=margem, pady=(margem, 0))
        button_cadastrar.grid(row=7, column=0, sticky="ew", padx=margem, pady=(0, margem))
    
    def evento_exibido(self) -> None:
        print("login.py — Registrar no log que a tela de login foi exibida.")
    
    def evento_entrar(self) -> None:
        print("login.py — Registrar no log que o usuário tentou entrar.")
    
    def evento_tela_cadastro(self) -> None:
        self._aplicativo.exibir_tela("TelaCadastro")
