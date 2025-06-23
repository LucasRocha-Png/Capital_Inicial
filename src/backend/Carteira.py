# Project
from backend.Acao import Acao
from backend.Boleta import Boleta
from backend.Log import Log

# Python
from typing import Type, Tuple

class Carteira:
    def __init__(self) -> None:
        self.__saldo = 0
        self.__boletas = []
        self.__acoes = []

    # SETTERS AND GETTERS --------------------
    @property
    def saldo(self) -> Type[float]:
        return self.__saldo

    @saldo.setter
    def saldo(self, value: Type[float]) -> None:
        self.__saldo = value

    @property
    def boletas(self) -> Type[list[Boleta]]:
        return self.__boletas
    
    @property
    def acoes(self) -> Type[list[Tuple]]:
        return self.__acoes
    
    # ----------------------------------------

    # SAVE AND LOAD -------------------------
    def to_dict(self) -> Type[dict]:
        return {
            "saldo": self.__saldo,
            "boletas": [boleta.to_dict() for boleta in self.__boletas],
            "acoes": [(acao.to_dict(), quantidade, preco_medio) for acao, quantidade, preco_medio in self.__acoes]        
        }

    def from_dict(self, dict_data: Type[str]) -> 'Carteira':
        self.__saldo = dict_data["saldo"]
        self.__boletas = [Boleta.from_dict(boleta_dict) for boleta_dict in dict_data["boletas"]]
        self.__acoes = [(Acao.from_dict(acao_dict), quantidade, preco_medio) for acao_dict, quantidade, preco_medio in dict_data["acoes"]]
    # -------------------------------------------

    def adicionar_boleta(self, boleta: Type[Boleta]) -> None:
        self.__boletas.append(boleta)

    def adicionar_acao(self, acao: Type[Acao], quantidade: Type[int], preco_medio: Type[float]) -> None:
        for i, (a, q, pm) in enumerate(self.__acoes):
            if a.ticker == acao.ticker:
                q_novo = q + quantidade
                pm_novo = (q * pm + quantidade * preco_medio) / q_novo
                self.__acoes[i] = (a, q_novo, pm_novo)
                return

        self.__acoes.append((acao, quantidade, preco_medio))

    def remover_acao(self, acao: Type[Acao], quantidade: Type[int]) -> None:
        for idx, (a, q, pm) in enumerate(self.__acoes):
            if a.ticker == acao.ticker:
                if q - quantidade <= 0: # Apesar que nunca vai ser ser negativo...
                    self.__acoes.pop(idx)
                else:
                    self.__acoes[idx] = (a, q - quantidade, pm)
                return
    
    def quantidade_acao(self, acao: Type[Acao]) -> int:
        for a, q, pm in self.__acoes:
            if a.ticker == acao.ticker:
                return q
        return 0