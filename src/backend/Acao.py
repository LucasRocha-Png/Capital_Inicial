# Third Party
import pandas as pd

# Python
from typing import Type

# Project
from database.Downloader import Downloader

class Acao:
    def __init__(self, pais: Type[str], ticker: Type[str], nome: Type[str], exchange: Type[str], preco: Type[float] = 0, historico: Type[pd.DataFrame] = None) -> None:
        self._pais = pais
        self._ticker = ticker
        self._nome = nome
        self._exchange = exchange
        self._preco = preco
        self._historico = historico        
    
    def __str__(self) -> Type[str]:
        return f"{self._ticker} ({self._nome}) - {self._pais} ({self._exchange})"

    @property
    def pais(self) -> Type[str]:
        return self._pais
    
    @property
    def ticker(self) -> Type[str]:
        return self._ticker
    
    @property
    def nome(self) -> Type[str]:
        return self._nome
    
    @property
    def exchange(self) -> Type[str]:
        return self._exchange

    @property  
    def preco(self) -> Type[float]:
        return self._preco
    
    @property
    def historico(self) -> Type[pd.DataFrame]:
        return self._historico
    
    def atualizar_valores(self, df: Type[pd.DataFrame]) -> Type[bool]:
        if df is None or df.empty:
            self._historico = None
            self._preco = 0.0
            return False

        else:
            self._historico = df.copy()
            self._preco = round(self._historico.iloc[-1]['Close'],2)
            return True
    
    def to_dict(self) -> Type[dict]:
        return {
            "pais": self._pais,
            "ticker": self._ticker,
            "nome": self._nome,
            "exchange": self._exchange,
            "preco": self._preco,
        }
    
    @classmethod
    def from_dict(cls, dict_data: Type[dict]) -> 'Acao':
        return cls(
            pais=dict_data['pais'],
            ticker=dict_data['ticker'],
            nome=dict_data['nome'],
            exchange=dict_data['exchange'],
            preco=dict_data.get('preco', 0.0),
            historico=None
        )