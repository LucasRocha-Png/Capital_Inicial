import customtkinter as ctk
from backend.Log import Log
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.tela import Tela

class Dashboard(ctk.CTkFrame):
    def __init__(self, master: Type["Tela"]) -> None:
        super().__init__(master)
        self._aplicativo = master._aplicativo
        self._widgets = {}
        self.configure(fg_color="#4B0082", corner_radius=12)

        # Decorativos
        fonte_titulo = ctk.CTkFont(family="Roboto", size=26, weight="bold")
        frame_bem_vindo = ctk.CTkFrame(self, fg_color="transparent")
        label_bem_vindo = ctk.CTkLabel(frame_bem_vindo, text="Bem vindo,", font=fonte_titulo, anchor="w", text_color="white")
        label_nome = ctk.CTkLabel(frame_bem_vindo, text="Usuário", font=fonte_titulo, anchor="w", text_color="#9370DB")
        frame_saldo = ctk.CTkFrame(self, fg_color="transparent")
        label_saldo = ctk.CTkLabel(frame_saldo, text="R$0.00", font=fonte_titulo, anchor="w", text_color="white")
        label_icone_saldo = ctk.CTkLabel(frame_saldo, image=self._aplicativo.imagens["image_saldo"], text="")
        frame_espacamento = ctk.CTkLabel(self, fg_color="transparent")
        frame_saida = ctk.CTkFrame(self, fg_color="transparent")
        label_sair = ctk.CTkLabel(frame_saida, text="Já está de saída?", anchor="w", text_color="white")

        # Interativos
        altura = 38
        button_sair = ctk.CTkButton(frame_saida, text="Trocar usuário", command=self.evento_sair, height=altura)

        # Guarda widgets necessários posteriormente
        self._widgets["label_nome"] = label_nome
        self._widgets["label_saldo"] = label_saldo

        # Layout dos widgets de saldo
        frame_saldo.rowconfigure(0, weight=1)
        frame_saldo.columnconfigure(0, weight=0)
        frame_saldo.columnconfigure(1, weight=0)
        margem_saldo_horizontal = 10
        margem_saldo_vertical = 5
        espacamento_saldo = 3
        label_icone_saldo.grid(row=0, column=0, sticky="nsew", padx=(margem_saldo_horizontal, espacamento_saldo), pady=margem_saldo_vertical)
        label_saldo.grid(row=0, column=1, sticky="nsew", padx=(espacamento_saldo, margem_saldo_horizontal), pady=margem_saldo_vertical)

        # Layout dos widgets de boas-vindas
        frame_bem_vindo.rowconfigure(0, weight=0)
        frame_bem_vindo.rowconfigure(1, weight=0)
        frame_bem_vindo.columnconfigure(0, weight=1)
        margem = 35
        espacamento = margem // 3
        label_bem_vindo.grid(row=0, column=0, sticky="ew", padx=margem, pady=(margem, 0))
        label_nome.grid(row=1, column=0, sticky="ew", padx=margem, pady=(0, margem))

        # Layout dos widgets de saída
        frame_saida.rowconfigure(0, weight=0)
        frame_saida.rowconfigure(1, weight=0)
        frame_saida.columnconfigure(0, weight=1)
        label_sair.grid(row=0, column=0, sticky="w", padx=margem, pady=(margem, 0))
        button_sair.grid(row=1, column=0, sticky="ew", padx=margem, pady=(0, margem))

        # Layout dos widgets do dashboard
        self.rowconfigure(0, weight=1)
        for coluna in range(4):
            peso = 0 if coluna != 2 else 1 # Coluna 2 é vazia
            self.columnconfigure(coluna, weight=peso)
        frame_bem_vindo.grid(row=0, column=0, sticky="nsew")
        frame_saldo.grid(row=0, column=1, sticky="nsew")
        frame_espacamento.grid(row=0, column=2, sticky="nsew")
        frame_saida.grid(row=0, column=3, sticky="nsew")
    
    def atualizar(self) -> None:
        usuario_atual = self._aplicativo.usuario_atual
        label_nome = self._widgets["label_nome"]
        label_saldo = self._widgets["label_saldo"]
        label_nome.configure(text=usuario_atual.nome)
        label_saldo.configure(text=f"R${usuario_atual.carteira.saldo:.2f}")
    
    def evento_sair(self) -> None:
        Log.trace("Saindo da conta...")
        self._aplicativo.exibir_tela("TelaLogin")
