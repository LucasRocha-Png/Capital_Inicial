import customtkinter as ctk
from tkinter import StringVar
from abc import ABC, abstractmethod
import mplfinance as mpf
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from backend.Log import Log
from frontend.tela import Tela
from frontend.lista_itens import ListaItens
from frontend.dashboard import Dashboard
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.aplicativo import Aplicativo

class TelaAcoes(Tela, ABC):
    def __init__(self, master: Type["Aplicativo"]) -> None:
        super().__init__(master)
        self.__transacao_em_andamento = False

        # Decorativos
        label_background = ctk.CTkLabel(self, image=self._aplicativo.imagens["image_background_dashboard"], text="")
        self._dashboard = Dashboard(self)
        fonte_titulo = ctk.CTkFont(family="Roboto", size=26, weight="bold")
        fonte_detalhes = ctk.CTkFont(family="Roboto", size=20, weight="bold")
        frame_detalhes = ctk.CTkFrame(self, fg_color="#4B0082", corner_radius=6)
        label_pais_topo = ctk.CTkLabel(frame_detalhes, text="País", anchor="w", font=fonte_detalhes, text_color="white")
        label_pais_base = ctk.CTkLabel(frame_detalhes, text="", anchor="w", font=fonte_detalhes, text_color="#9370DB")
        label_ticker_topo = ctk.CTkLabel(frame_detalhes, text="Ticker", anchor="w", font=fonte_detalhes, text_color="white")
        label_ticker_base = ctk.CTkLabel(frame_detalhes, text="", anchor="w", font=fonte_detalhes, text_color="#9370DB")
        label_nome_topo = ctk.CTkLabel(frame_detalhes, text="Nome da empresa", font=fonte_detalhes, anchor="w", text_color="white")
        label_nome_base = ctk.CTkLabel(frame_detalhes, text="", anchor="w", font=fonte_detalhes, text_color="#9370DB")
        label_exchange_topo = ctk.CTkLabel(frame_detalhes, text="Exchange", font=fonte_detalhes, anchor="w", text_color="white")
        label_exchange_base = ctk.CTkLabel(frame_detalhes, text="", anchor="w", font=fonte_detalhes, text_color="#9370DB")
        label_preco_topo = ctk.CTkLabel(frame_detalhes, text="Preço médio", font=fonte_detalhes, anchor="w", text_color="white")
        label_preco_base = ctk.CTkLabel(frame_detalhes, text="", anchor="w", font=fonte_detalhes, text_color="#9370DB")
        label_grafico = ctk.CTkLabel(frame_detalhes, text="Histórico de preços", anchor="w", font=fonte_detalhes, text_color="white")
        frame_grafico = ctk.CTkFrame(frame_detalhes, fg_color="white", border_width=2)
        frame_titulo_acoes = ctk.CTkFrame(self, fg_color="transparent")
        label_acoes = ctk.CTkLabel(frame_titulo_acoes, text="", font=fonte_titulo, anchor="w", text_color="white") # Texto depende se é tela de ações disponíveis ou possuídas
        label_icone_acoes = ctk.CTkLabel(frame_titulo_acoes, image=self._aplicativo.imagens["image_acoes"], text="")
        frame_titulo_detalhes = ctk.CTkFrame(self, fg_color="transparent")
        label_detalhes = ctk.CTkLabel(frame_titulo_detalhes, text="Detalhes da ação", font=fonte_titulo, anchor="w", text_color="white")
        label_icone_detalhes = ctk.CTkLabel(frame_titulo_detalhes, image=self._aplicativo.imagens["image_detalhes"], text="")
        label_nenhuma_acao = ctk.CTkLabel(self, fg_color="#4B0082", corner_radius=6, text="Selecione uma ação para ver seus detalhes.", font=fonte_titulo, text_color="white")
        frame_interacao = ctk.CTkFrame(self, fg_color="#4B0082", corner_radius=6)
        frame_transacao = ctk.CTkFrame(self, fg_color="#4B0082", corner_radius=0, border_width=2)
        label_total_titulo = ctk.CTkLabel(frame_transacao, text="Total da transação", anchor="w", font=fonte_detalhes, text_color="white")
        label_total = ctk.CTkLabel(frame_transacao, text="", anchor="w", font=fonte_detalhes, text_color="#9370DB")
        label_quantidade = ctk.CTkLabel(frame_transacao, text="Quantidade", anchor="w", text_color="white")

        # Interativos
        altura = 38
        lista_acoes = ListaItens(self)
        button_abas = ctk.CTkSegmentedButton(self, values=["Ações do mercado", "Ações possuídas", "Histórico de negociações"], command=self._dashboard.evento_mudar_aba)
        button_prompt_transacao = ctk.CTkButton(frame_interacao, text="", command=self.__evento_prompt_transacao, fg_color="white", text_color="#9370DB", height=altura) # Texto definido pela subclasse (comprar ou vender ação)
        button_atualizar_selecao = ctk.CTkButton(frame_interacao, text="Atualizar ação selecionada", command=self.evento_atualizar_selecao, height=altura)
        button_atualizar_lista = ctk.CTkButton(frame_interacao, text="Atualizar lista de ações", command=self.evento_atualizar_lista, height=altura)
        variable_quantidade = StringVar()
        variable_quantidade.trace_add("write", self.__calcular_transacao) # Calcula o total da transação sempre que o usuário digita
        entry_quantidade = ctk.CTkEntry(frame_transacao, placeholder_text="Digite a quantidade", height=altura, textvariable=variable_quantidade)
        button_confirmar_transacao = ctk.CTkButton(frame_transacao, text="", command=self.evento_transacao, height=altura)

        # Guarda widgets necessários posteriormente
        self._widgets["lista_acoes"] = lista_acoes
        self._widgets["label_pais_base"] = label_pais_base
        self._widgets["label_ticker_base"] = label_ticker_base
        self._widgets["label_nome_base"] = label_nome_base
        self._widgets["label_exchange_base"] = label_exchange_base
        self._widgets["label_preco_base"] = label_preco_base
        self._widgets["frame_grafico"] = frame_grafico
        self._widgets["button_abas"] = button_abas
        self._widgets["label_acoes"] = label_acoes
        self._widgets["label_nenhuma_acao"] = label_nenhuma_acao
        self._widgets["button_prompt_transacao"] = button_prompt_transacao
        self._widgets["button_atualizar_selecao"] = button_atualizar_selecao
        self._widgets["frame_transacao"] = frame_transacao
        self._widgets["label_total"] = label_total
        self._widgets["entry_quantidade"] = entry_quantidade
        self._widgets["button_confirmar_transacao"] = button_confirmar_transacao

        # Layout dos frames principais
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        label_background.grid(row=0, column=0, sticky="nsew")
        # O tamanho do dashboard depende do tamanho do desktop
        desktop = self._aplicativo.tamanho_desktop
        dashboard_pady = (0, int(desktop[1] * 0.86))
        self._dashboard.grid(row=0, column=0, sticky="nsew", pady=dashboard_pady)

        # Layout do conjunto de abas
        abas_padx = int(desktop[0] * 0.27)
        abas_pady = (int(desktop[1] * 0.12), int(desktop[1] * 0.85))
        button_abas.grid(row=0, column=0, sticky="nsew", padx=abas_padx, pady=abas_pady)

        # Layout dos frames de ações
        porcentagem_margem_geral = 0.12
        porcentagem_margem_superior = 0.28
        frames_pady = (int(desktop[1] * porcentagem_margem_superior), int(desktop[1] * porcentagem_margem_geral * 2.40))
        lista_padx = (int(desktop[0] * porcentagem_margem_geral), int(desktop[0] * 0.61))
        lista_acoes.grid(row=0, column=0, sticky="nsew", padx=lista_padx, pady=frames_pady)
        detalhes_padx = (int(desktop[0] * 0.41), int(desktop[0] * porcentagem_margem_geral))
        frame_detalhes.grid(row=0, column=0, sticky="nsew", padx=detalhes_padx, pady=frames_pady)
        label_nenhuma_acao.grid(row=0, column=0, sticky="nsew", padx=detalhes_padx, pady=frames_pady)
        titulos_pady = (int(desktop[1] * (porcentagem_margem_superior - 0.07)), int(desktop[1] * (1.01 - porcentagem_margem_superior)))
        frame_titulo_acoes.grid(row=0, column=0, sticky="nsew", padx=lista_padx, pady=titulos_pady)
        frame_titulo_detalhes.grid(row=0, column=0, sticky="nsew", padx=detalhes_padx, pady=titulos_pady)
        interacao_pady = (int(desktop[1] * (1.02 - porcentagem_margem_geral * 2.40)), int(desktop[1] * porcentagem_margem_geral * 1.62))
        interacao_padx = int(desktop[0] * porcentagem_margem_geral)
        frame_interacao.grid(row=0, column=0, sticky="nsew", padx=interacao_padx, pady=interacao_pady)
        transacao_pady = (int(desktop[1] * 0.70), int(desktop[1] * 0.08))
        transacao_padx = (int(desktop[0] * 0.48), int(desktop[0] * 0.40))
        frame_transacao.grid(row=0, column=0, sticky="nsew", padx=transacao_padx, pady=transacao_pady)

        # Layout do frame de interação
        margem = 35
        espacamento = margem // 3
        frame_interacao.rowconfigure(0, weight=1)
        for coluna in range(4):
            peso = 0 if coluna != 1 else 1
            frame_interacao.columnconfigure(coluna, weight=peso)
        button_atualizar_lista.grid(row=0, column=0, sticky="ew", padx=(margem, 0))
        button_prompt_transacao.grid(row=0, column=2, sticky="ew", padx=(0, espacamento))
        button_atualizar_selecao.grid(row=0, column=3, sticky="ew", padx=(espacamento, margem))

        # Layout dos títulos dos frames
        espacamento_titulos = 3
        frame_titulo_acoes.rowconfigure(0, weight=1)
        frame_titulo_acoes.columnconfigure(0, weight=0)
        frame_titulo_acoes.columnconfigure(1, weight=0)
        label_icone_acoes.grid(row=0, column=0, sticky="nsew", padx=(0, espacamento_titulos))
        label_acoes.grid(row=0, column=1, sticky="nsew", padx=(espacamento_titulos, 0))
        frame_titulo_detalhes.rowconfigure(0, weight=1)
        frame_titulo_detalhes.columnconfigure(0, weight=0)
        frame_titulo_detalhes.columnconfigure(1, weight=0)
        label_icone_detalhes.grid(row=0, column=0, sticky="nsew", padx=(0, espacamento_titulos))
        label_detalhes.grid(row=0, column=1, sticky="nsew", padx=(espacamento_titulos, 0))

        # Layout dos detalhes da ação
        frame_detalhes.columnconfigure(0, weight=1)
        frame_detalhes.columnconfigure(1, weight=10)
        for linha in range(10):
            frame_detalhes.rowconfigure(linha, weight=0)
        label_pais_topo.grid(row=0, column=0, sticky="w", padx=margem, pady=(margem, 0))
        label_pais_base.grid(row=1, column=0, sticky="w", padx=margem, pady=(0, espacamento))
        label_ticker_topo.grid(row=2, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        label_ticker_base.grid(row=3, column=0, sticky="w", padx=margem, pady=(0, espacamento))
        label_nome_topo.grid(row=4, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        label_nome_base.grid(row=5, column=0, sticky="w", padx=margem, pady=(0, espacamento))
        label_exchange_topo.grid(row=6, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        label_exchange_base.grid(row=7, column=0, sticky="w", padx=margem, pady=(0, espacamento))
        label_preco_topo.grid(row=8, column=0, sticky="w", padx=margem, pady=(espacamento, 0))
        label_preco_base.grid(row=9, column=0, sticky="w", padx=margem, pady=(0, margem))
        label_grafico.grid(row=0, column=1, sticky="nsew", padx=margem, pady=(margem, 0))
        frame_grafico.grid(row=1, column=1, rowspan=9, sticky="nsew", padx=margem, pady=(0, margem))

        # Layout interno do frame de gráfico
        frame_grafico.columnconfigure(0, weight=1)
        frame_grafico.rowconfigure(0, weight=1)

        # Layout do frame de transação
        frame_transacao.columnconfigure(0, weight=1)
        for linha in range(5):
            frame_transacao.rowconfigure(linha, weight=0)
        margem_transacao = 20
        espacamento_transacao = margem_transacao // 3
        label_total_titulo.grid(row=0, column=0, sticky="w", padx=margem_transacao, pady=(margem_transacao, 0))
        label_total.grid(row=1, column=0, sticky="w", padx=margem_transacao, pady=(0, espacamento_transacao))
        label_quantidade.grid(row=2, column=0, sticky="w", padx=margem_transacao, pady=(espacamento_transacao, 0))
        entry_quantidade.grid(row=3, column=0, sticky="ew", padx=margem_transacao, pady=(0, espacamento_transacao))
        button_confirmar_transacao.grid(row=4, column=0, sticky="ew", padx=margem_transacao, pady=(espacamento_transacao, margem_transacao))

    def _atualizar_grafico(self, historico: Type[pd.DataFrame]) -> None:
        Log.trace("Redesenhando o gráfico da ação...")
        #historico = historico[30:] # Seleciona dados apenas dos últimos 30 dias
        # Deleta canvas já existente para criar um novo
        if "canvas_grafico" in self._widgets:
            self._widgets["canvas_grafico"].destroy()
        # Usa a biblioteca mplfinance para plotar o gráfico numa figura
        figure, _ = mpf.plot(
            historico,
            type="candle",
            style="binance",
            returnfig=True,
            figsize=(3,1)
        )
        margem = 10
        canvas_grafico = FigureCanvasTkAgg(figure, master=self._widgets["frame_grafico"])
        canvas_grafico.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=margem, pady=margem)
        canvas_grafico.draw()
        self._widgets["canvas_grafico"] = canvas_grafico.get_tk_widget()

    def atualizar_detalhes(self) -> None:
        Log.trace("Atualizando detalhes da ação selecionada...")
        self._dashboard.atualizar()
        acao_selecionada = self._widgets["lista_acoes"].item_selecionado
        self._widgets["label_pais_base"].configure(text=acao_selecionada.pais)
        self._widgets["label_ticker_base"].configure(text=acao_selecionada.ticker)
        self._widgets["label_nome_base"].configure(text=acao_selecionada.nome)
        self._widgets["label_exchange_base"].configure(text=acao_selecionada.exchange)
        self._widgets["label_preco_base"].configure(text=f"R${acao_selecionada.preco:.2f}")
        self._atualizar_grafico(acao_selecionada.historico)
        self._widgets["label_nenhuma_acao"].grid_remove()
        self._widgets["button_prompt_transacao"].grid()
        self._widgets["button_atualizar_selecao"].grid()
        if self.__transacao_em_andamento:
            self.__evento_prompt_transacao()
    
    def _limpar(self) -> None:
        Log.trace("Limpando detalhes da ação...")
        self._widgets["label_nenhuma_acao"].grid() # Esconde detalhes da ação por trás de uma label
        self._widgets["button_prompt_transacao"].grid_remove()
        self._widgets["button_atualizar_selecao"].grid_remove()
        self._widgets["frame_transacao"].grid_remove()
        if self.__transacao_em_andamento:
            self.__evento_prompt_transacao()
    
    def _mensagem_transacao(self, mensagem: str, cor: str, duracao: int = 2000) -> None:
        button_confirmar_transacao = self._widgets["button_confirmar_transacao"]
        original_button_color = button_confirmar_transacao.cget("fg_color")
        original_button_text = button_confirmar_transacao.cget("text")
        button_confirmar_transacao.configure(text=mensagem, fg_color=cor, border_color=cor, hover=False, command=None)
        self.after(duracao, lambda: (
            button_confirmar_transacao.configure(text=original_button_text, fg_color=original_button_color, border_color=original_button_color, hover=True, command=self.evento_transacao)
        ))
    
    def __calcular_transacao(self, *args) -> None:
        entry_quantidade = self._widgets["entry_quantidade"]
        label_total = self._widgets["label_total"]
        valor_digitado = entry_quantidade.get()
        total = 0.00
        # Calcula o total da transação se o valor digitado for um dígito
        if valor_digitado.isdigit() and int(valor_digitado) > 0:
            total = float(valor_digitado) * self._widgets["lista_acoes"].item_selecionado.preco
            entry_quantidade.configure(border_color="#9370DB")
        else:
            Log.warning("Aceitam-se apenas valores inteiros positivos para a quantidade de ações.")
            entry_quantidade.configure(border_color="red")
            label_total.configure(text="")
        label_total.configure(text=f"R${total:.2f}")

    def __evento_prompt_transacao(self) -> None:
        frame_transacao = self._widgets["frame_transacao"]
        self._widgets["entry_quantidade"].cget("textvariable").set("1")
        if self.__transacao_em_andamento:
            Log.trace("Fechando janela de transação...")
            frame_transacao.grid_remove()
        else:
            Log.trace("Abrindo janela de transação...")
            frame_transacao.grid()
            self.evento_atualizar_selecao()
        self.__transacao_em_andamento = not self.__transacao_em_andamento

    @abstractmethod
    def evento_transacao(self) -> None:
        pass
    
    @abstractmethod
    def evento_atualizar_selecao(self) -> None: # Atualiza APENAS a ação selecionada da lista de ações
        pass
    
    @abstractmethod
    def evento_atualizar_lista(self) -> None: # Atualiza a lista de ações POR COMPLETO
        pass
    