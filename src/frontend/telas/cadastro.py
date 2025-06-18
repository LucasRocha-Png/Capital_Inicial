import customtkinter as ctk
from backend.Log import Log
from backend.Usuarios import UsuarioPadrao
from backend.Usuarios import UsuarioDemo
from frontend.tela import Tela
import re
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.aplicativo import Aplicativo

class TelaCadastro(Tela):
    def __init__(self, master: Type["Aplicativo"]) -> None:
        super().__init__(master)

        # Decorativos
        label_background = ctk.CTkLabel(self, image=self._aplicativo.imagens["image_background"], text="")
        label_logo = ctk.CTkLabel(self, image=self._aplicativo.imagens["image_logo"], text="")
        frame_cadastro = ctk.CTkScrollableFrame(self, fg_color="#4B0082", corner_radius=6)
        label_tipo_conta = ctk.CTkLabel(frame_cadastro, text="Tipo de conta", anchor="w", text_color="white")
        label_nome = ctk.CTkLabel(frame_cadastro, text="Nome", anchor="w", text_color="white")
        label_cpf = ctk.CTkLabel(frame_cadastro, text="CPF", anchor="w", text_color="white")
        label_data = ctk.CTkLabel(frame_cadastro, text="Data de nascimento", anchor="w", text_color="white")
        label_email = ctk.CTkLabel(frame_cadastro, text="E-mail", anchor="w", text_color="white")
        label_senha = ctk.CTkLabel(frame_cadastro, text="Senha", anchor="w", text_color="white")
        label_entrar = ctk.CTkLabel(frame_cadastro, text="Já tem uma conta?", anchor="w", text_color="white")

        # Interativos
        altura = 38
        option_tipo_conta = ctk.CTkOptionMenu(frame_cadastro, values=["Padrão", "Demo"], height=altura)
        entry_nome = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite seu nome completo", height=altura)
        entry_cpf = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite seu CPF (AAA.BBB.CCC-DD)", height=altura)
        entry_data = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite a data (DD/MM/AAAA)", height=altura)
        entry_email = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite seu e-mail", height=altura)
        entry_senha = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite uma senha (mínimo 6 caracteres)", show="*", height=altura)
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
        self._widgets["option_tipo_conta"] = option_tipo_conta
        self._widgets["entry_nome"] = entry_nome
        self._widgets["entry_cpf"] = entry_cpf
        self._widgets["entry_data"] = entry_data
        self._widgets["entry_email"] = entry_email
        self._widgets["entry_senha"] = entry_senha
        self._widgets["button_cadastrar"] = button_cadastrar

        # Layout dos widgets de background
        label_background.grid(row=0, column=0, sticky="nsew")
        logo_rely = 0.17
        label_logo.place(relx=0.50, rely=logo_rely, anchor="center")

        # Layout do frame de cadastro
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # O tamanho do frame depende do tamanho do desktop
        desktop = self._aplicativo.tamanho_desktop
        cadastro_padx = int(desktop[0] * 0.38)
        cadastro_pady = (int(desktop[1] * 0.30), int(desktop[1] * 0.10))
        frame_cadastro.grid(row=0, column=0, sticky="nsew", padx=cadastro_padx, pady=cadastro_pady)

        # Layout dos widgets de cadastro
        frame_cadastro.columnconfigure(0, weight=1)
        for linha in range(16):
            peso = 0 if linha != 13 else 1 # Linha 13 é vazia
            frame_cadastro.rowconfigure(linha, weight=peso)
        margem = 35
        espacamento = margem // 4
        label_tipo_conta.grid(row=0, column=0, sticky="w", padx=margem, pady=(margem, 0))
        option_tipo_conta.grid(row=1, column=0, sticky="ew", padx=margem, pady=(0, espacamento))
        label_nome.grid(row=2, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        entry_nome.grid(row=3, column=0, sticky="ew", padx=margem, pady=(0, espacamento))
        label_cpf.grid(row=4, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        entry_cpf.grid(row=5, column=0, sticky="ew", padx=margem, pady=(0, espacamento))
        label_data.grid(row=6, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        entry_data.grid(row=7, column=0, sticky="ew", padx=margem, pady=(0, espacamento))
        label_email.grid(row=8, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        entry_email.grid(row=9, column=0, sticky="ew", padx=margem, pady=(0, espacamento))
        label_senha.grid(row=10, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        entry_senha.grid(row=11, column=0, sticky="ew", padx=margem, pady=(0, espacamento * 2))
        button_mostrar_senha.grid(row=11, column=0, sticky="e", padx=(0, margem+5), pady=(0, espacamento * 2))
        button_cadastrar.grid(row=12, column=0, sticky="ew", padx=margem, pady=(espacamento * 2, margem))
        label_entrar.grid(row=14, column=0, sticky="w", padx=margem, pady=(margem, 0))
        button_entrar.grid(row=15, column=0, sticky="ew", padx=margem, pady=(0, margem))

    def evento_exibido(self) -> None:
        Log.trace("Tela de cadastro exibida.")
        self._aplicativo.usuario_atual = None
    
    def evento_cadastrar(self) -> None:
        option_tipo_conta = self._widgets["option_tipo_conta"]
        entry_nome = self._widgets["entry_nome"]
        entry_cpf = self._widgets["entry_cpf"]
        entry_data = self._widgets["entry_data"]
        entry_email = self._widgets["entry_email"]
        entry_senha = self._widgets["entry_senha"]
        button_cadastrar = self._widgets["button_cadastrar"]
        Log.info(f"Tentativa de cadastro iniciada. Tipo de conta: {option_tipo_conta.get()}; E-mail: {entry_email.get()}; Nome: {entry_nome.get()}; CPF: {entry_cpf.get()}; Data de nascimento: {entry_data.get()}")
        
        # Primeiramente valida os dados fornecidos
        original_entry_border = entry_nome.cget("border_color")
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        data = entry_data.get()
        email = entry_email.get()
        senha = entry_senha.get()
        duracao_flash = 2000
        erro = False
        # Validação do nome
        if ' ' not in nome or any(char.isdigit() for char in nome):
            Log.error("Falha no cadastro. Nome inválido.")
            entry_nome.configure(border_color="red")
            erro = True
        # Validação do CPF
        if not re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
            Log.error("Falha no cadastro. CPF inválido.")
            entry_cpf.configure(border_color="red")
            erro = True
        # Validação da data de nascimento
        if not re.fullmatch(r"(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}", data):
            Log.error("Falha no cadastro. Data de nascimento inválida.")
            entry_data.configure(border_color="red")
            erro = True
        # Validação do e-mail
        if ("@" not in email) or ("." not in email.split("@")[-1]):
            Log.error("Falha no cadastro. E-mail inválido.")
            entry_email.configure(border_color="red")
            erro = True
        # Validação da senha
        if len(senha) < 6:
            Log.error("Falha no cadastro. Senha muito curta.")
            entry_senha.configure(border_color="red")
            erro = True
        
        if erro:
            original_button_color = button_cadastrar.cget("fg_color")
            button_cadastrar.configure(text="Dados inseridos inválidos", fg_color="red", border_color="red", hover=False, command=None)
            self.after(duracao_flash, lambda: (
                entry_nome.configure(border_color=original_entry_border),
                entry_cpf.configure(border_color=original_entry_border),
                entry_data.configure(border_color=original_entry_border),
                entry_email.configure(border_color=original_entry_border),
                entry_senha.configure(border_color=original_entry_border),
                button_cadastrar.configure(text="Cadastrar-se", fg_color=original_button_color, border_color=original_button_color, hover=True, command=self.evento_cadastrar)
            ))
            return
        
        # Criação e registro do usuário
        novo_usuario = None
        if option_tipo_conta.get() == "Demo":
            novo_usuario = UsuarioDemo(
                nome=nome,
                cpf=cpf,
                data_nascimento=data,
                email=email,
                senha=senha
            )
        else:
            novo_usuario = UsuarioPadrao(
                nome=nome,
                cpf=cpf,
                data_nascimento=data,
                email=email,
                senha=senha
            )
        self._aplicativo.manager_usuarios.adicionar(novo_usuario)
        self._aplicativo.manager_usuarios.salvar()
        self._aplicativo.usuario_atual = novo_usuario
        self._aplicativo.exibir_tela("TelaAcoesDisponiveis")
    
    def evento_tela_login(self) -> None:
        self._aplicativo.exibir_tela("TelaLogin")
