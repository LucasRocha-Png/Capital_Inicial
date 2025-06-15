import customtkinter as ctk
from ..tela import Tela
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from ..aplicativo import Aplicativo

class TelaCadastro(Tela):
    def __init__(self, master: Type["Aplicativo"]):
        super().__init__(master)

        # Decorativos
        tamanho_logo = 300
        label_background = ctk.CTkLabel(self, image=self._aplicativo.imagens["image_background"], text="")
        label_logo = ctk.CTkLabel(self, image=self._aplicativo.imagens["image_logo"], text="")
        frame_cadastro = ctk.CTkFrame(self, fg_color="#4B0082", corner_radius=6)
        label_nome = ctk.CTkLabel(frame_cadastro, text="Nome", anchor="w", text_color="white")
        label_cpf = ctk.CTkLabel(frame_cadastro, text="CPF", anchor="w", text_color="white")
        label_data = ctk.CTkLabel(frame_cadastro, text="Data de nascimento", anchor="w", text_color="white")
        label_email = ctk.CTkLabel(frame_cadastro, text="E-mail", anchor="w", text_color="white")
        label_senha = ctk.CTkLabel(frame_cadastro, text="Senha", anchor="w", text_color="white")
        label_entrar = ctk.CTkLabel(frame_cadastro, text="Já tem uma conta?", anchor="w", text_color="white")

        # Interativos
        altura = 38
        entry_nome = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite seu nome", height=altura)
        entry_cpf = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite seu CPF", height=altura)
        entry_data = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite sua data de nascimento (DD/MM/AAAA)", height=altura)
        entry_email = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite seu e-mail", height=altura)
        entry_senha = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite uma senha", show="*", height=altura)
        button_mostrar_senha = ctk.CTkButton(
            frame_cadastro,
            text="",
            image=self._aplicativo.imagens["image_senha_oculta"],
            command=lambda: (
                entry_senha.configure(show="" if entry_senha.cget("show") else "*"),
                button_mostrar_senha.configure(image=self._aplicativo.imagens["image_senha_oculta"] if entry_senha.cget("show") else self._aplicativo.imagens["image_senha_revelada"])
            ),
            width=25,
            height=25,
            fg_color="white",
            hover=False,
            border_width=0,
            corner_radius=0
        )
        button_cadastrar = ctk.CTkButton(frame_cadastro, text="Cadastrar-se", command=self.evento_cadastrar, height=altura)
        button_entrar = ctk.CTkButton(frame_cadastro, text="Entrar", command=self.evento_tela_login, fg_color="white", text_color="#9370DB", height=altura)

        # Guarda widgets necessários posteriormente
        self._widgets["entry_nome"] = entry_nome
        self._widgets["entry_cpf"] = entry_cpf
        self._widgets["entry_data"] = entry_data
        self._widgets["entry_email"] = entry_email
        self._widgets["entry_senha"] = entry_senha

        # Layout dos widgets de background
        label_background.grid(row=0, column=0, sticky="nsew")
        logo_rely = 0.17
        label_logo.place(relx=0.50, rely=logo_rely, anchor="center")

        # Layout do frame de cadastro
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # O tamanho do frame depende do tamanho do desktop
        desktop = self._aplicativo.tamanho_desktop
        login_padx = int(desktop[0] * 0.38)
        login_pady = (int(desktop[1] * 0.30), int(desktop[1] * 0.08))
        frame_cadastro.grid(row=0, column=0, sticky="nsew", padx=login_padx, pady=login_pady)

        # Layout dos widgets de cadastro
        frame_cadastro.columnconfigure(0, weight=1)
        for linha in range(14):
            peso = 0 if linha != 11 else 1 # Linha 11 é vazia
            frame_cadastro.rowconfigure(linha, weight=peso)
        margem = 35
        espacamento = margem // 4
        label_nome.grid(row=0, column=0, sticky="w", padx=margem, pady=(margem, 0))
        entry_nome.grid(row=1, column=0, sticky="ew", padx=margem, pady=(0, espacamento))
        label_cpf.grid(row=2, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        entry_cpf.grid(row=3, column=0, sticky="ew", padx=margem, pady=(0, espacamento))
        label_data.grid(row=4, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        entry_data.grid(row=5, column=0, sticky="ew", padx=margem, pady=(0, espacamento))
        label_email.grid(row=6, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        entry_email.grid(row=7, column=0, sticky="ew", padx=margem, pady=(0, espacamento))
        label_senha.grid(row=8, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        entry_senha.grid(row=9, column=0, sticky="ew", padx=margem, pady=(0, espacamento * 2))
        button_mostrar_senha.grid(row=9, column=0, sticky="e", padx=(0, margem+5), pady=(0, espacamento * 2))
        button_cadastrar.grid(row=10, column=0, sticky="ew", padx=margem, pady=(espacamento * 2, margem))
        label_entrar.grid(row=12, column=0, sticky="w", padx=margem, pady=(margem, 0))
        button_entrar.grid(row=13, column=0, sticky="ew", padx=margem, pady=(0, margem))
    
    def evento_exibido(self) -> None:
        print("cadastro.py — Registrar no log que a tela de cadastro foi exibida.")
    
    def evento_cadastrar(self) -> None:
        print("cadastro.py — Registrar no log que o usuário tentou cadastrar.")
    
    def evento_tela_login(self) -> None:
        self._aplicativo.exibir_tela("TelaLogin")
