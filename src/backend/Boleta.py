# Python
from typing import Type

class Boleta:
    def __init__(self, data_operacao: Type[str], ticker: Type[str], quantidade: Type[int], preco_medio: Type[float], taxas: Type[float], tipo: Type[str]) -> None:
        self.__data_operacao = data_operacao
        self.__ticker = ticker
        self.__quantidade = quantidade
        self.__preco_medio = preco_medio
        self.__taxas = taxas
        self.__tipo = tipo

    # GETTERS AND SETTERS --------------------------
    @property
    def data_operacao(self) -> Type[str]:
        return self.__data_operacao

    @property
    def ticker(self) -> Type[str]:
        return self.__ticker

    @property
    def quantidade(self) -> Type[int]:
        return self.__quantidade

    @property
    def preco_medio(self) -> Type[float]:
        return self.__preco_medio

    @property
    def taxas(self) -> Type[float]:
        return self.__taxas
    
    @property
    def tipo(self) -> Type[str]:
        return self.__tipo
    # ----------------------------------------------

    # SAVE AND LOAD --------------------------------
    def to_dict(self) -> Type[dict]:
        return {
            "data_operacao": self.__data_operacao,
            "ticker": self.__ticker,
            "quantidade": self.__quantidade,
            "preco_medio": self.__preco_medio,
            "taxas": self.__taxas,
            "tipo": self.__tipo
        }
    
    @classmethod
    def from_dict(cls, dict_data_operacao: Type[str]) -> 'Boleta':
        boleta = cls(
            data_operacao=dict_data_operacao['data_operacao'],
            ticker=dict_data_operacao['ticker'],
            quantidade=dict_data_operacao['quantidade'],
            preco_medio=dict_data_operacao['preco_medio'],
            taxas=dict_data_operacao['taxas'],
            tipo=dict_data_operacao['tipo']
        )
        return boleta
    # --------------------------------------------------
    
    @classmethod
    def criar_boleta(cls, data_operacao: Type[str], ticker: Type[str], quantidade: Type[int], preco_medio: Type[float], taxas: Type[float], tipo: Type[str]) -> 'Boleta':
        boleta = cls(
            data_operacao = data_operacao,
            ticker = ticker,
            quantidade = quantidade,
            preco_medio = preco_medio,
            taxas = taxas,
            tipo = tipo
        )
        return boleta