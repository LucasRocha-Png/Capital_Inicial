import customtkinter as ctk
from backend.Log import Log
from frontend.tela import Tela
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.aplicativo import Aplicativo

class TelaLogin(Tela):
    def __init__(self, master: Type["Aplicativo"]) -> None:
        super().__init__(master)

        # Decorativos
        label_background = ctk.CTkLabel(self, image=self._aplicativo.imagens["image_background"], text="")
        label_logo = ctk.CTkLabel(self, image=self._aplicativo.imagens["image_logo"], text="")
        frame_login = ctk.CTkFrame(self, fg_color="#4B0082", corner_radius=6)
        label_usuario = ctk.CTkLabel(frame_login, text="E-mail", anchor="w", text_color="white")
        label_senha = ctk.CTkLabel(frame_login, text="Senha", anchor="w", text_color="white")
        label_cadastrar = ctk.CTkLabel(frame_login, text="Ainda não tem uma conta?", anchor="w", text_color="white")

        # Interativos
        altura = 38
        entry_usuario = ctk.CTkEntry(frame_login, placeholder_text="Digite seu e-mail", height=altura)
        entry_senha = ctk.CTkEntry(frame_login, placeholder_text="Digite sua senha", show="*", height=altura)
        button_mostrar_senha = ctk.CTkButton(
            frame_login,
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
        button_entrar = ctk.CTkButton(frame_login, text="Entrar", command=self.evento_entrar, height=altura)
        button_cadastrar = ctk.CTkButton(frame_login, text="Cadastrar-se", command=self.evento_tela_cadastro, fg_color="white", text_color="#9370DB", height=altura)

        # Guarda widgets necessários posteriormente
        self._widgets["entry_usuario"] = entry_usuario
        self._widgets["entry_senha"] = entry_senha
        self._widgets["button_entrar"] = button_entrar

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
        Log.trace("Tela de login exibida.")
        self._aplicativo.usuario_atual = None
    
    def evento_entrar(self) -> None:
        entry_usuario = self._widgets["entry_usuario"]
        entry_senha = self._widgets["entry_senha"]
        button_entrar = self._widgets["button_entrar"]
        Log.info(f"Tentativa de login iniciada. E-mail do usuário: {entry_usuario.get()}")

        # Tenta carregar o usuário da database usando ManagerUsuarios de Aplicativo
        self._aplicativo.usuario_atual = self._aplicativo.manager_usuarios.carregar(entry_usuario.get(), entry_senha.get())
        if self._aplicativo.usuario_atual:
            Log.info(f"Usuário {self._aplicativo.usuario_atual.nome} logado com sucesso.")
            self._aplicativo.exibir_tela("TelaAcoesDisponiveis")
        else:
            Log.error("Falha no login. E-mail ou senha incorretos.")
            # Dica visual de erro
            original_entry_border = entry_usuario.cget("border_color")
            original_button_color = button_entrar.cget("fg_color")
            entry_usuario.configure(border_color="red")
            entry_senha.configure(border_color="red")
            button_entrar.configure(text="E-mail ou senha incorretos", fg_color="red", border_color="red", hover=False, command=None)
            duracao_flash = 2000
            self.after(duracao_flash, lambda: (
                entry_usuario.configure(border_color=original_entry_border),
                entry_senha.configure(border_color=original_entry_border),
                button_entrar.configure(text="Entrar", fg_color=original_button_color, border_color=original_button_color, hover=True, command=self.evento_entrar)
            ))
    
    def evento_tela_cadastro(self) -> None:
        self._aplicativo.exibir_tela("TelaCadastro")
