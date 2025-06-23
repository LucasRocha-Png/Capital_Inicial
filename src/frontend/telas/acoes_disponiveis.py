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
        acoes_disponiveis = self._aplicativo.manager_acao.acoes
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
                self._mensagem_transacao("Saldo insuficiente", "red")
        else:
            Log.error("Falha em comprar ação. A quantidade especificada não é um valor inteiro positivo.")
            self._mensagem_transacao("Quantidade inválida", "red")
            return
        self._dashboard.atualizar()
        self.evento_atualizar_selecao()

    def evento_atualizar_selecao(self) -> None:
        Log.trace("Atualizando a ação do mercado selecionada...")
        lista_acoes = self._widgets["lista_acoes"]
        self._aplicativo.manager_acao.atualizar([lista_acoes.item_selecionado])
        self.limpar()
        #acao_atualizada =
        #self._widgets["lista_acoes"].item_selecionado = acao_atualizada
    
    def evento_atualizar_lista(self) -> None:
        Log.trace("Atualizando a lista de ações do mercado...")
        lista_acoes = self._aplicativo.manager_acao.acoes
        self._aplicativo.manager_acao.atualizar(lista_acoes)
        #acoes_disponiveis =
        #self._widgets["lista_acoes"].atualizar(acoes_disponiveis)
        self._limpar()
