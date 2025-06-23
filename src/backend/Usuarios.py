# Python
from abc import ABC, abstractmethod
from typing import Type
import json

# Project
from backend.Carteira import Carteira

class Usuario(ABC):
    def __init__(self, nome: Type[str], cpf: Type[str], data_nascimento: Type[str], pais: Type[str], email: Type[str], senha: Type[str]) -> None:
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._pais = pais
        self._email = email
        self._senha = senha
        self._carteira: Carteira = Carteira()

    # SETTERS AND GETTERS -----------------------------
    @property
    def nome(self) -> Type[str]:
        return self._nome
    
    @property
    def cpf(self) -> Type[str]:
        return self._cpf
    
    @property
    def data_nascimento(self) -> Type[str]:
        return self._data_nascimento    
    
    @property
    def pais(self) -> Type[str]:
        return self._pais
    
    @property
    def email(self) -> Type[str]:
        return self._email
    
    @property
    def senha(self) -> Type[str]:
        return self._senha
    
    @property
    def carteira(self) -> Type[Carteira]:
        return self._carteira
    # ---------------------------------------------------------

    # SAVE AND LOAD -------------------------------------------
    @abstractmethod
    def to_json(self) -> Type[str]:
        pass

    @classmethod
    def from_json(cls, json_data: Type[str]) -> 'Usuario':
        usuario = cls(
            nome=json_data['nome'],
            cpf=json_data['cpf'],
            data_nascimento=json_data['data_nascimento'],
            email=json_data['email'],
            senha=json_data['senha']
        )
        
        if 'carteira' in json_data:
            usuario.carteira.from_dict(json_data['carteira'])
        
        return usuario
    # ----------------------------------------------------------

    @abstractmethod
    def __str__(self) -> Type[str]:
        pass


class UsuarioPadrao(Usuario):
    def __init__(self, nome: Type[str], cpf: Type[str], data_nascimento: Type[str], email: Type[str], senha: Type[str]) -> None:
        super().__init__(nome, cpf, data_nascimento, pais="Brazil", email=email, senha=senha)
        self._tipo_conta = "padrao"
        self._taxa_corretagem = 0.01

    # GETTERS AND SETTERS --------------------------
    @property
    def tipo_conta(self) -> Type[str]:
        return self._tipo_conta
    
    @property
    def taxa_corretagem(self) -> Type[float]:
        return self._taxa_corretagem
    # ----------------------------------------------

    # SAVE AND LOAD --------------------------------
    def to_json(self) -> Type[str]:
        data = {
            "nome": self._nome,
            "cpf": self._cpf,
            "data_nascimento": self._data_nascimento,
            "pais": self._pais,
            "email": self._email,
            "senha": self._senha,
            "tipo_conta": self._tipo_conta,
            "taxa_corretagem": self._taxa_corretagem
        }

        try:
            carteira_dict = self.carteira.to_dict()
            data['carteira'] = carteira_dict
        except Exception:
            pass

        return json.dumps(data, ensure_ascii=False)
    # ---------------------------------------------
    def __str__(self) -> Type[str]:
        return f"Usuário: {self._nome}, CPF: {self._cpf}, Data de Nascimento: {self._data_nascimento}, Email: {self._email}, Tipo de Conta: {self._tipo_conta}, taxa_corretagem: {self._taxa_corretagem}"
    
class UsuarioDemo(UsuarioPadrao):
    def __init__(self, nome: Type[str], cpf: Type[str], data_nascimento: Type[str], email: Type[str], senha: Type[str]) -> None:
        super().__init__(nome, cpf, data_nascimento, email, senha)
        self._tipo_conta = "demo"
        self._taxa_corretagem = 0.0
    
    