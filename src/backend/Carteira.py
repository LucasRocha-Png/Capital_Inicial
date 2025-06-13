"""
Lucas Rocha - 10/06/2025

Cria a classe da Carteira, é responsável por armazenar o saldo, senha de transacao, acoes e as boletas do usuario
"""

class Carteira:
    def __init__(self, cpf: str) -> None:
        self.saldo = 0
        self.senha = ""
        self.acoes = {}
        self.boletas = []
