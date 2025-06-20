# Project
from backend.Acao import Acao
from backend.Boleta import Boleta
from backend.Log import Log
from typing import Tuple

# Python
import json

class Carteira:
    def __init__(self) -> None:
        self._saldo = 0
        self._boletas = []
        self._acoes = []

    # SETTERS AND GETTERS --------------------
    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, value: float) -> None:
        self._saldo = value

    @property
    def boletas(self) -> list[Boleta]:
        return self._boletas
    
    @property
    def acoes(self) -> list[Tuple]:
        return self._acoes
    
    # ----------------------------------------

    # SAVE AND LOAD -------------------------
    def to_dict(self) -> str:
        return {
            "saldo": self._saldo,
            "boletas": [boleta.to_dict() for boleta in self._boletas],
            "acoes": [(acao.to_dict(), quantidade, preco_medio) for acao, quantidade, preco_medio in self._acoes]        
        }

    def from_dict(self, dict_data: str):
        self._saldo = dict_data["saldo"]
        self._boletas = [Boleta.from_dict(boleta_dict) for boleta_dict in dict_data["boletas"]]
        self._acoes = [(Acao.from_dict(acao_dict), quantidade, preco_medio) for acao_dict, quantidade, preco_medio in dict_data["acoes"]]
    # -------------------------------------------

    def adicionar_boleta(self, boleta: Boleta) -> None:
        self._boletas.append(boleta)

    def adicionar_acao(self, acao: Acao, quantidade: int, preco_medio: float) -> None:
        for i, (a, q, pm) in enumerate(self._acoes):
            if a.ticker == acao.ticker:
                q_novo = q + quantidade
                pm_novo = (q * pm + quantidade * preco_medio) / q_novo
                self._acoes[i] = (a, q_novo, pm_novo)
                return

        self._acoes.append((acao, quantidade, preco_medio))

    def remover_acao(self, acao: Acao, quantidade: int) -> None:
        for idx, (a, q, pm) in enumerate(self._acoes):
            if a.ticker == acao.ticker:
                if q - quantidade <= 0: # Apesar que nunca vai ser ser negativo...
                    self._acoes.pop(idx)
                else:
                    self._acoes[idx] = (a, q_remanescente, pm)
                return
    
    def quantidade_acao(self, acao: Acao) -> None:
        for a, q, pm in self._acoes:
            if a.ticker == acao.ticker:
                return q
        return 0