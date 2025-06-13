"""
Lucas Rocha - 10/06/2025
"""

# Python
from abc import ABC, abstractmethod

# Project
from backend.Carteira import Carteira

class Usuario(ABC):
    def __init__(self, nome: str, cpf: str, data_nascimento: str, pais: str, email: str, senha: str) -> None:
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._pais = pais
        self._email = email
        self._senha = senha

    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def cpf(self) -> str:
        return self._cpf
    
    @property
    def data_nascimento(self) -> str:
        return self._data_nascimento    
    
    @property
    def pais(self) -> str:
        return self._pais
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def senha(self) -> str:
        return self._senha
    
    @property
    def carteira(self) -> Carteira:
        return self._carteira

    @abstractmethod
    def imprimir_dados(self) -> None:
        pass

class UsuarioPadrao(Usuario):
    def __init__(self, nome: str, cpf: str, data_nascimento: str, email: str, senha: str) -> None:
        super().__init__(nome, cpf, data_nascimento, email, senha)
        self._tipo_conta = "padrao"
        self._taxa = 0.01

    def imprimir_dados(self) -> None:
        print(f"Nome: {self._nome}")
        print(f"CPF: {self._cpf}")
        print(f"Data de Nascimento: {self._data_nascimento}")
        print(f"Email: {self._email}")
        print(f"Tipo de Conta: {self._tipo_conta}")
        print(f"Taxa: {self._taxa}")

    @property
    def tipo_conta(self) -> str:
        return self._tipo_conta
    
    @property
    def taxa(self) -> float:
        return self._taxa

class UsuarioDemo(UsuarioPadrao):
    def __init__(self, nome: str, cpf: str, data_nascimento: str, email: str, senha: str) -> None:
        super().__init__(nome, cpf, data_nascimento, email, senha)
        self.tipo_conta = "demo"
        self._taxa = 0.0
