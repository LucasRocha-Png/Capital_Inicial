import customtkinter as ctk
from backend.Log import Log
from backend.Boleta import Boleta
from backend.Acao import Acao
from typing import Type, TYPE_CHECKING
if TYPE_CHECKING:
    from frontend.tela import Tela

class ListaItens(ctk.CTkScrollableFrame):
    def __init__(self, master: Type["Tela"]) -> None:
        super().__init__(master)
        Log.trace("Desenhando lista de itens...")
        self.__tela = master
        self.__widgets = []
        self.__itens = None
        self.__item_selecionado = None
        self.configure(fg_color="#4B0082", corner_radius=6)
    
    @property
    def item_selecionado(self) -> Type[Boleta] | Type[Acao] | None:
        return self.__item_selecionado

    def evento_selecionar(self, linha: int) -> None:
        widget_selecionado = self.__widgets[linha]
        self.__item_selecionado = self.__itens[linha]
        Log.info(f"O usuário {self.__tela._aplicativo.usuario_atual.nome} selecionou o objeto {self.__item_selecionado.__class__.__name__} de índice {linha} da lista. Ticker: {self.__item_selecionado.ticker}.")
        # Pinta o item selecionado de outra cor para destacá-lo
        widget_selecionado.configure(fg_color="#8A2BE2", border_color="#8A2BE2")
        for widget in self.__widgets:
            if widget != widget_selecionado:
                widget.configure(fg_color="#9370DB", border_color="#9370DB")
        self.__tela.atualizar_detalhes()

    def atualizar(self, itens: list | None) -> None:
        Log.trace("Atualizando lista de itens...")
        self.__itens = itens
        # Deleta toda a lista para redesenhá-la completamente
        for widget in self.__widgets:
            widget.destroy()
        self.__widgets = []
        if self.__itens:
            altura = 38
            margem = 35
            espacamento = margem // 4
            for linha, item in enumerate(self.__itens):
                # Detalhes essenciais a exibir por objeto na lista de itens
                detalhes = ""
                if isinstance(item, Boleta):
                    detalhes = f"{item.ticker} | {item.tipo} | {item.data_operacao}"
                elif isinstance(item, Acao):
                    detalhes = f"{item.ticker} | {item.nome} | {item.preco}"
                else:
                    erro = "A lista de itens deve ser composta de objetos Boleta ou Acao."
                    Log.error(erro)
                    raise ValueError(erro)
                # Cada objeto na lista de itens é selecionável por um botão
                button_item = ctk.CTkButton(
                    self,
                    text=detalhes,
                    anchor="w",
                    command=lambda linha=linha: (
                        self.evento_selecionar(linha)
                    ),
                    height=altura
                )
                self.columnconfigure(0, weight=1)
                self.rowconfigure(linha, weight=0)
                item_pady = (espacamento, espacamento)
                if linha == 0:
                    item_pady = (margem, espacamento)
                elif linha == len(self.__itens) - 1:
                    item_pady = (espacamento, margem)
                button_item.grid(row=linha, column=0, sticky="ew", padx=margem, pady=item_pady)
                self.__widgets.append(button_item)
