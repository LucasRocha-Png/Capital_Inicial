"""
10/06/2024 - Lucas Rocha

Corretora. Permite negociações, lista as ações disponíveis.
"""

# Third Party
import pandas as pd

# Project
from backend.Log import Log
from backend.Acao import Acao
from database.ManagerAcao import ManagerAcao

TICKERS_LIST_PATH = "data/tickers.csv"

class Corretora:
    def __init__(self) -> None:
        self.acoes_disponiveis = self.__carregar_acoes_disponiveis()
    
    def __carregar_acoes_disponiveis(self, pais: str) -> None:
        self.manager_acao = ManagerAcao()
        self.acoes_disponiveis = [acao for acao in self.manager_acao.acoes_diponiveis if acao.pais == pais]

    def fazer_transacao(self) -> None:
        pass