from backend.Log import Log
from frontend.tela_acoes import TelaAcoes
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.aplicativo import Aplicativo

class TelaAcoesPossuidas(TelaAcoes):
    def __init__(self, master: Type["Aplicativo"]) -> None:
        super().__init__(master)
        self._widgets["label_acoes"].configure(text="Suas ações")
        self._widgets["button_prompt_transacao"].configure(text="Vender ação selecionada")
        self._widgets["button_confirmar_transacao"].configure(text="Confirmar venda")
    
    def evento_exibido(self) -> None:
        Log.trace("Tela de ações possuídas exibida.")
        self._dashboard.atualizar()
        self._widgets["button_abas"].set("Ações possuídas")
        self.evento_atualizar_lista()
    
    def evento_transacao(self) -> None:
        Log.trace("Processando venda de ações...")
        valor_digitado = self._widgets["entry_quantidade"].get()
        if valor_digitado.isdigit() and int(valor_digitado) > 0:
            self._aplicativo.corretora.negociar_acao(
                self._aplicativo.usuario_atual,
                self._widgets["lista_acoes"].item_selecionado,
                "venda",
                int(valor_digitado)
            )
        else:
            Log.error("Falha em vender ação. A quantidade especificada não é um valor inteiro positivo.")
            # Dica visual de erro
            self._mensagem_transacao("Quantidade inválida", "red")
            return
        self._dashboard.atualizar()
        self.evento_atualizar_selecao()
    
    def evento_atualizar_selecao(self) -> None:
        Log.trace("Atualizando a ação do usuário selecionada...")
        lista_acoes = self._widgets["lista_acoes"]
        self._aplicativo.manager_acao.atualizar([lista_acoes.item_selecionado])
        self.limpar()
    
    def evento_atualizar_lista(self) -> None:
        Log.trace("Atualizando a lista de ações do usuário...")
        # Carrega ações do usuário e atualiza todas antes de desenhar a lista de ações
        lista_acoes = self._widgets["lista_acoes"]
        acoes_possuidas = self._aplicativo.usuario_atual.carteira.acoes
        if len(acoes_possuidas) > 0:
            self._aplicativo.manager_acao.atualizar(acoes_possuidas)
            lista_acoes.atualizar(acoes_possuidas)
        else:
            lista_acoes.atualizar(None)
        self._limpar()