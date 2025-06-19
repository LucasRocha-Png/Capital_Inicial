from backend.Log import Log
from frontend.tela_acoes import TelaAcoes
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.aplicativo import Aplicativo

class TelaAcoesDisponiveis(TelaAcoes):
    def __init__(self, master: Type["Aplicativo"]) -> None:
        super().__init__(master)
        self._widgets["label_acoes"].configure(text="Ações disponíveis")
        self._widgets["button_prompt_transacao"].configure(text="Comprar ação selecionada")
        self._widgets["button_confirmar_transacao"].configure(text="Confirmar compra")
    
    def evento_exibido(self) -> None:
        Log.trace("Tela de ações disponíveis exibida.")
        self._dashboard.atualizar()
        self._widgets["button_abas"].set("Ações do mercado")
        self.limpar()
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
    
    def evento_transacao(self) -> None:
        Log.trace("Processando compra de ações...")
        valor_digitado = self._widgets["entry_quantidade"].get()
        if valor_digitado.isdigit() and int(valor_digitado) > 0:
            usuario_atual = self._aplicativo.usuario_atual
            acao_selecionada = self._widgets["lista_acoes"].item_selecionado
            preco_total = float(valor_digitado) * acao_selecionada.preco
            if usuario_atual.carteira.saldo >= preco_total: # Confere saldo suficiente
                self._aplicativo.corretora.negociar_acao(
                    usuario_atual,
                    acao_selecionada,
                    "compra",
                    int(valor_digitado)
                )
            else:
                Log.error(f"Falha em comprar ação. Usuário {usuario_atual.nome} tem saldo de R${usuario_atual.carteira.saldo:.2f}. A quantia necessária é R${preco_total:.2f}.")
                self.mensagem_transacao("Saldo insuficiente", "red")
        else:
            Log.error("Falha em comprar ação. A quantidade especificada não é um valor inteiro positivo.")
            self.mensagem_transacao("Quantidade inválida", "red")
            return
        self._dashboard.atualizar()
        self.evento_atualizar_selecao()

    def evento_atualizar_selecao(self) -> None:
        Log.trace("Atualizando a ação do mercado selecionada...")
        #acao_atualizada =
        #self._widgets["lista_acoes"].item_selecionado = acao_atualizada
    
    def evento_atualizar_lista(self) -> None:
        Log.trace("Atualizando a lista de ações do mercado...")
        #acoes_disponiveis =
        #self._widgets["lista_acoes"].atualizar(acoes_disponiveis)
        self.limpar()
