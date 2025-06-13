# Project
from backend.Acao import Acao
from backend.Boleta import Boleta
from backend.Log import Log

# Python
import json

class Carteira:
    def __init__(self) -> None:
        self._saldo = 0
        self._boletas = []
        self._acoes = []

    def to_dict(self) -> str:
        return {
            "saldo": self._saldo,
            "boletas": [boleta.to_dict() for boleta in self._boletas],
            "acoes": [(acao.to_dict(), quantidade) for acao, quantidade in self._acoes]        
        }

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, value: float) -> None:
        self._saldo = value

    @property
    def boletas(self) -> list[Boleta]:
        return self._boletas
    
    def from_dict(self, dict_data: str):
        self._saldo = dict_data["saldo"]
        self._boletas = [Boleta.from_dict(boleta_dict) for boleta_dict in dict_data["boletas"]]
        self._acoes = [(Acao.from_dict(acao_dict), quantidade) for acao_dict, quantidade in dict_data["acoes"]]

    def adicionar_boleta(self, boleta: Boleta) -> None:
        self._boletas.append(boleta)
    
    def adicionar_acao(self, acao: Acao, quantidade: int) -> None:
        for a, q in self._acoes:
            if a.ticker == acao.ticker:
                q += quantidade
                Log.info(f"Adicionados {quantidade} de {acao.ticker} à carteira.")
                return
            
        self._acoes.append((acao, quantidade))
        Log.info(f"Adicionados {quantidade} de {acao.ticker} à carteira.")

    def remover_acao(self, acao: Acao, quantidade: int) -> None:
        for a, q in self._acoes:
            if a.ticker == acao.ticker:
                if (q - quantidade) == 0:
                    self._acoes.remove((a, q))
                else:
                    q -= quantidade
                break

        Log.info(f"Removidos {quantidade} de {acao.ticker} da carteira.")