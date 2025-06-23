import customtkinter as ctk
from tkinter import StringVar
from backend.Log import Log
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.tela import Tela

class Dashboard(ctk.CTkFrame):
    def __init__(self, master: Type["Tela"]) -> None:
        super().__init__(master)
        Log.trace("Desenhando dashboard...")
        self.__aplicativo = master._aplicativo
        self.__widgets = {}
        self.__transacao_em_andamento = False
        self.configure(fg_color="#4B0082", corner_radius=12)

        # Decorativos
        fonte_titulo = ctk.CTkFont(family="Roboto", size=26, weight="bold")
        frame_bem_vindo = ctk.CTkFrame(self, fg_color="transparent")
        label_bem_vindo = ctk.CTkLabel(frame_bem_vindo, text="Bem vindo,", font=fonte_titulo, anchor="w", text_color="white")
        label_nome = ctk.CTkLabel(frame_bem_vindo, text="Usuário", font=fonte_titulo, anchor="w", text_color="#9370DB")
        frame_saldo = ctk.CTkFrame(self, fg_color="transparent")
        label_saldo = ctk.CTkLabel(frame_saldo, text="R$0.00", font=fonte_titulo, anchor="w", text_color="white")
        label_icone_saldo = ctk.CTkLabel(frame_saldo, image=self.__aplicativo.imagens["image_saldo"], text="")
        frame_adicionar_saldo = ctk.CTkFrame(self, fg_color="transparent")
        label_adicionar_saldo = ctk.CTkLabel(frame_adicionar_saldo, text="Quer comprar mais ações?", anchor="w", text_color="white")
        frame_espacamento = ctk.CTkLabel(self, fg_color="transparent")
        frame_saida = ctk.CTkFrame(self, fg_color="transparent")
        label_sair = ctk.CTkLabel(frame_saida, text="Já está de saída?", anchor="w", text_color="white")
        frame_transacao = ctk.CTkFrame(self, fg_color="#4B0082", corner_radius=0, border_width=2)
        label_quantia = ctk.CTkLabel(frame_transacao, text="Quantia", anchor="w", text_color="white")

        # Interativos
        altura = 38
        button_adicionar_saldo = ctk.CTkButton(frame_adicionar_saldo, text="Adicionar saldo", command=self.__evento_prompt_transacao, fg_color="white", text_color="#9370DB", height=altura)
        button_sair = ctk.CTkButton(frame_saida, text="Trocar usuário", command=self.__evento_sair, height=altura)
        variable_quantia = StringVar()
        variable_quantia.trace_add("write", self.__validar_transacao) # Rastreia o valor de quantia digitado para validá-lo
        altura_transacao = 28
        entry_quantia = ctk.CTkEntry(frame_transacao, placeholder_text="Digite a quantia", height=altura_transacao, textvariable=variable_quantia)
        button_confirmar_transacao = ctk.CTkButton(frame_transacao, text="Confirmar transação", command=self.__evento_transacao, height=altura_transacao)

        # Guarda widgets necessários posteriormente
        self.__widgets["label_nome"] = label_nome
        self.__widgets["label_saldo"] = label_saldo
        self.__widgets["frame_transacao"] = frame_transacao
        self.__widgets["entry_quantia"] = entry_quantia
        self.__widgets["button_confirmar_transacao"] = button_confirmar_transacao

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
        label_bem_vindo.grid(row=0, column=0, sticky="ew", padx=margem, pady=(margem, 0))
        label_nome.grid(row=1, column=0, sticky="ew", padx=margem, pady=(0, margem))

        # Layout dos widgets de adição de saldo
        frame_adicionar_saldo.rowconfigure(0, weight=0)
        frame_adicionar_saldo.rowconfigure(1, weight=0)
        frame_adicionar_saldo.columnconfigure(0, weight=1)
        label_adicionar_saldo.grid(row=0, column=0, sticky="w", padx=margem, pady=(margem, 0))
        button_adicionar_saldo.grid(row=1, column=0, sticky="ew", padx=margem, pady=(0, margem))

        # Layout do frame de transação
        frame_transacao.columnconfigure(0, weight=1)
        for linha in range(3):
            frame_transacao.rowconfigure(linha, weight=0)
        margem_transacao = 10
        espacamento_transacao = margem_transacao // 3
        label_quantia.grid(row=0, column=0, sticky="w", padx=margem_transacao, pady=(margem_transacao, 0))
        entry_quantia.grid(row=1, column=0, sticky="ew", padx=margem_transacao, pady=(0, espacamento_transacao))
        button_confirmar_transacao.grid(row=2, column=0, sticky="ew", padx=margem_transacao, pady=(espacamento_transacao, margem_transacao))

        # Layout dos widgets de saída
        frame_saida.rowconfigure(0, weight=0)
        frame_saida.rowconfigure(1, weight=0)
        frame_saida.columnconfigure(0, weight=1)
        label_sair.grid(row=0, column=0, sticky="w", padx=margem, pady=(margem, 0))
        button_sair.grid(row=1, column=0, sticky="ew", padx=margem, pady=(0, margem))

        # Layout dos widgets do dashboard
        self.rowconfigure(0, weight=1)
        for coluna in range(6):
            peso = 0 if coluna != 4 else 1 # Coluna 2 é vazia
            self.columnconfigure(coluna, weight=peso)
        frame_bem_vindo.grid(row=0, column=0, sticky="nsew")
        frame_saldo.grid(row=0, column=1, sticky="nsew")
        frame_adicionar_saldo.grid(row=0, column=2, sticky="nsew")
        transacao_pady = (5, 25)
        transacao_padx = 3
        frame_transacao.grid(row=0, column=3, sticky="nsew", padx=transacao_padx, pady=transacao_pady)
        frame_espacamento.grid(row=0, column=4, sticky="nsew")
        frame_saida.grid(row=0, column=5, sticky="nsew")
        frame_transacao.grid_remove()
    
    def atualizar(self) -> None:
        usuario_atual = self.__aplicativo.usuario_atual
        label_nome = self.__widgets["label_nome"]
        label_saldo = self.__widgets["label_saldo"]
        label_nome.configure(text=usuario_atual.nome)
        label_saldo.configure(text=f"R${usuario_atual.carteira.saldo:.2f}")
        if self.__transacao_em_andamento:
            self.__evento_prompt_transacao()

    def __validar_transacao(self, *args) -> None:
        entry_quantia = self.__widgets["entry_quantia"]
        valor_digitado = entry_quantia.get()
        # Valida se o valor digitado é um float
        valor_float = True
        try:
            float(valor_digitado)
        except ValueError:
            valor_float = False
        if valor_float and float(valor_digitado) > 0.00:
            entry_quantia.configure(border_color="#9370DB")
        elif valor_digitado != "":
            Log.warning("Aceitam-se apenas valores float positivos para a quantia de saldo a ser adicionada.")
            entry_quantia.configure(border_color="red")

    def __evento_prompt_transacao(self) -> None:
        frame_transacao = self.__widgets["frame_transacao"]
        self.__widgets["entry_quantia"].cget("textvariable").set("1.00")
        if self.__transacao_em_andamento:
            Log.trace("Fechando janela de adição de saldo...")
            frame_transacao.grid_remove()
        else:
            Log.trace("Abrindo janela de adição de saldo...")
            frame_transacao.grid()
            self.atualizar()
        self.__transacao_em_andamento = not self.__transacao_em_andamento
    
    def __evento_transacao(self) -> None:
        Log.trace("Processando adição de saldo...")
        valor_digitado = self.__widgets["entry_quantia"].get()
        valor_float = True
        try:
            float(valor_digitado)
        except ValueError:
            valor_float = False
        if valor_float and float(valor_digitado) > 0.00:
            self.__aplicativo.corretora.fazer_transacao(self.__aplicativo.usuario_atual, float(valor_digitado))
        else:
            Log.error("Falha em adicionar saldo. A quantia especificada não é um valor float positivo.")
            # Dica visual de erro
            button_confirmar_transacao = self.__widgets["button_confirmar_transacao"]
            original_button_color = button_confirmar_transacao.cget("fg_color")
            button_confirmar_transacao.configure(text="Quantia inválida", fg_color="red", border_color="red", hover=False, command=None)
            duracao_flash = 2000
            self.after(duracao_flash, lambda: (
                button_confirmar_transacao.configure(text="Confirmar transação", fg_color=original_button_color, border_color=original_button_color, hover=True, command=self.__evento_transacao)
            ))
            return
        self.atualizar()
    
    def evento_mudar_aba(self, aba: str) -> None:
        nova_tela = ""
        match aba:
            case "Ações possuídas":
                nova_tela = "TelaAcoesPossuidas"
            case "Histórico de negociações":
                nova_tela = "TelaHistorico"
            case _:
                nova_tela = "TelaAcoesDisponiveis"
        self.__aplicativo.exibir_tela(nova_tela)
    
    def __evento_sair(self) -> None:
        Log.trace("Saindo da conta...")
        self.__aplicativo.exibir_tela("TelaLogin")
