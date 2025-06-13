# Python
from abc import ABC, abstractmethod
import json

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
        self._carteira: Carteira = Carteira()

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
    def __str__(self) -> None:
        pass

    @abstractmethod
    def to_json(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, json_data: str) -> 'Usuario':
        pass

    @classmethod
    def from_json(cls, json_data: str) -> 'Usuario':
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

class UsuarioPadrao(Usuario):
    def __init__(self, nome: str, cpf: str, data_nascimento: str, email: str, senha: str) -> None:
        super().__init__(nome, cpf, data_nascimento, pais="Brazil", email=email, senha=senha)
        self._tipo_conta = "padrao"
        self._taxa_corretagem = 0.01

    def __str__(self) -> None:
        return f"Usuário: {self._nome}, CPF: {self._cpf}, Data de Nascimento: {self._data_nascimento}, Email: {self._email}, Tipo de Conta: {self._tipo_conta}, taxa_corretagem: {self._taxa_corretagem}"
    
    @property
    def tipo_conta(self) -> str:
        return self._tipo_conta
    
    @property
    def taxa_corretagem(self) -> float:
        return self._taxa_corretagem
    
    def to_json(self) -> str:
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

class UsuarioDemo(UsuarioPadrao):
    def __init__(self, nome: str, cpf: str, data_nascimento: str, email: str, senha: str) -> None:
        super().__init__(nome, cpf, data_nascimento, email, senha)
        self._tipo_conta = "demo"
        self._taxa_corretagem = 0.0
    
    