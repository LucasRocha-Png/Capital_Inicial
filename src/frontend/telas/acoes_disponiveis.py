import customtkinter as ctk
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from backend.Log import Log
from frontend.tela import Tela
from frontend.dashboard import Dashboard
from frontend.lista_itens import ListaItens
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.aplicativo import Aplicativo

class TelaAcoesDisponiveis(Tela):
    def __init__(self, master: Type["Aplicativo"]) -> None:
        super().__init__(master)
        self.__dashboard = Dashboard(self)

        # Decorativos
        frame_detalhes = ctk.CTkFrame(self, fg_color="#4B0082", corner_radius=6)
        label_pais_topo = ctk.CTkLabel(frame_detalhes, text="País", anchor="w", text_color="white")
        label_pais_base = ctk.CTkLabel(frame_detalhes, text="", anchor="w", text_color="#9370DB")
        label_ticker_topo = ctk.CTkLabel(frame_detalhes, text="Ticker", anchor="w", text_color="white")
        label_ticker_base = ctk.CTkLabel(frame_detalhes, text="", anchor="w", text_color="#9370DB")
        label_nome_topo = ctk.CTkLabel(frame_detalhes, text="Nome da empresa", anchor="w", text_color="white")
        label_nome_base = ctk.CTkLabel(frame_detalhes, text="", anchor="w", text_color="#9370DB")
        label_exchange_topo = ctk.CTkLabel(frame_detalhes, text="Exchange", anchor="w", text_color="white")
        label_exchange_base = ctk.CTkLabel(frame_detalhes, text="", anchor="w", text_color="#9370DB")
        label_preco_topo = ctk.CTkLabel(frame_detalhes, text="Preço médio", anchor="w", text_color="white")
        label_preco_base = ctk.CTkLabel(frame_detalhes, text="", anchor="w", text_color="#9370DB")
        frame_grafico = ctk.CTkFrame(frame_detalhes, fg_color="white", border_width=2)

        # Interativos
        lista_acoes = ListaItens(self)
        button_abas = ctk.CTkSegmentedButton(self, values=["Ações do mercado", "Ações possuídas", "Histórico de negociações"], command=self.__dashboard.evento_mudar_aba)
        button_abas.set("Ações do mercado")

        # Guarda widgets necessários posteriormente
        self._widgets["lista_acoes"] = lista_acoes
        self._widgets["label_pais_base"] = label_pais_base
        self._widgets["label_ticker_base"] = label_ticker_base
        self._widgets["label_nome_base"] = label_nome_base
        self._widgets["label_exchange_base"] = label_exchange_base
        self._widgets["label_preco_base"] = label_preco_base
        self._widgets["frame_grafico"] = frame_grafico

        # Layout dos frames principais
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # O tamanho do dashboard depende do tamanho do desktop
        desktop = self._aplicativo.tamanho_desktop
        dashboard_pady = (0, int(desktop[1] * 0.86))
        self.__dashboard.grid(row=0, column=0, sticky="nsew", pady=dashboard_pady)

        # Layout do conjunto de abas
        abas_padx = int(desktop[0] * 0.27)
        abas_pady = (int(desktop[1] * 0.12), int(desktop[1] * 0.84))
        button_abas.grid(row=0, column=0, sticky="nsew", padx=abas_padx, pady=abas_pady)

        # Layout dos frames de ações
        desktop = self._aplicativo.tamanho_desktop
        porcentagem_margem = 0.09
        lista_padx = (int(desktop[0] * porcentagem_margem), int(desktop[0] * 0.62))
        lista_pady = (int(desktop[1] * 0.20), int(desktop[1] * porcentagem_margem))
        lista_acoes.grid(row=0, column=0, sticky="nsew", padx=lista_padx, pady=lista_pady)
        detalhes_padx = (int(desktop[0] * 0.45), int(desktop[0] * porcentagem_margem))
        detalhes_pady = (int(desktop[1] * 0.20), int(desktop[1] * porcentagem_margem))
        frame_detalhes.grid(row=0, column=0, sticky="nsew", padx=detalhes_padx, pady=detalhes_pady)

        # Layout dos detalhes da ação
        frame_detalhes.columnconfigure(0, weight=1)
        frame_detalhes.columnconfigure(1, weight=2)
        for linha in range(10):
            frame_detalhes.rowconfigure(linha, weight=0)
        margem = 35
        espacamento = margem // 4
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
        frame_grafico.grid(row=0, column=1, rowspan=10, sticky="nsew")

        # Layout interno do frame de gráfico
        frame_grafico.columnconfigure(0, weight=1)
        frame_grafico.rowconfigure(0, weight=1)

    def atualizar_grafico(self, historico: Type[pd.DataFrame]) -> None:
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
        margem = 15
        canvas_grafico = FigureCanvasTkAgg(figure, master=self._widgets["frame_grafico"])
        canvas_grafico.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=margem, pady=margem)
        canvas_grafico.draw()
        self._widgets["canvas_grafico"] = canvas_grafico.get_tk_widget()

    def atualizar_detalhes(self) -> None:
        Log.trace("Atualizando detalhes da ação selecionada...")
        self.__dashboard.atualizar()
        acao_selecionada = self._widgets["lista_acoes"].item_selecionado
        self._widgets["label_pais_base"].configure(text=acao_selecionada.pais)
        self._widgets["label_ticker_base"].configure(text=acao_selecionada.ticker)
        self._widgets["label_nome_base"].configure(text=acao_selecionada.nome)
        self._widgets["label_exchange_base"].configure(text=acao_selecionada.exchange)
        self._widgets["label_preco_base"].configure(text=f"R${acao_selecionada.preco:.2f}")
        self.atualizar_grafico(acao_selecionada.historico)

    def evento_exibido(self) -> None:
        Log.trace("Tela de ações disponíveis exibida.")
        self.__dashboard.atualizar()
        # ----------------------------------- APENAS PARA TESTE -----------------------------------
        import pandas as pd
        from backend.Acao import Acao  # ajuste este import conforme sua estrutura

        # Função interna para criar um DataFrame dummy de 5 dias
        def make_dummy_historico():
            dates = pd.date_range(start="2025-01-01", periods=5, freq="D")
            return pd.DataFrame({
                "Open":   [100 + i for i in range(5)],
                "High":   [105 + i for i in range(5)],
                "Low":    [ 95 + i for i in range(5)],
                "Close":  [102 + i for i in range(5)],
                "Volume": [1000 + 10*i for i in range(5)],
            }, index=dates)

        # Metadados de teste
        metadados = [
            ("Brazil", "PETR4",  "Petrobras",          "B3"),
            ("Brazil", "VALE3",  "Vale",               "B3"),
            ("USA",    "AAPL",   "Apple Inc.",         "NASDAQ"),
            ("USA",    "MSFT",   "Microsoft Corp.",    "NASDAQ"),
            ("Japan",  "7203.T", "Toyota Motor Corp.", "TSE"),
        ]

        # Cria e popula a lista de Acao
        acoes_disponiveis = []
        for pais, ticker, nome, exchange in metadados:
            historico = make_dummy_historico()
            preco = float(historico.iloc[-1]["Close"])
            acoes_disponiveis.append(
                Acao(
                    pais=pais,
                    ticker=ticker,
                    nome=nome,
                    exchange=exchange,
                    preco=preco,
                    historico=historico
                )
            )
        # ----------------------------------- FIM DO TESTE -----------------------------------
        self._widgets["lista_acoes"].atualizar(acoes_disponiveis)
