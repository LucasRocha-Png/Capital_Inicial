# Third Party
import pandas as pd

# Project
from database.Downloader import Downloader

class Acao:
    def __init__(self, pais: str, ticker: str, nome: str, exchange: str, preco: float = 0, historico: pd.DataFrame = None) -> None:
        self._pais = pais
        self._ticker = ticker
        self._nome = nome
        self._exchange = exchange
        self._preco = preco
        self._historico = historico        
    
    def __str__(self) -> str:
        return f"{self._ticker} ({self._nome}) - {self._pais} ({self._exchange})"

    @property
    def pais(self) -> str:
        return self._pais
    
    @property
    def ticker(self) -> str:
        return self._ticker
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def exchange(self) -> str:
        return self._exchange

    @property  
    def preco(self) -> float:
        return self._preco
    
    @property
    def historico(self) -> pd.DataFrame:
        return self._historico
    
    def atualizar(self, df: pd.DataFrame) -> bool:
        if df is None or df.empty:
            self._historico = None
            self._preco = 0.0
            return False

        else:
            self._historico = df.copy()
            self._preco = self._historico.iloc[-1]['Close']
            return True