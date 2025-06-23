# Python
from datetime import datetime
from typing import Type

# Third Party
import pandas as pd

# Project
from backend.Log import Log
from backend.Acao import Acao
from database.ManagerAcao import ManagerAcao
from backend.Carteira import Carteira
from backend.Boleta import Boleta
from backend.Usuarios import *

TICKERS_LIST_PATH = "data/tickers.csv"

class Corretora:
    def __init__(self) -> None:
        Log.trace("Inicializando Corretora...")

    def fazer_transacao(self, usuario: Type[Usuario], valor: Type[float]) -> None:
        carteira = usuario.carteira
        carteira.saldo += valor

        if valor > 0:
            Log.info(f"Adicionando o valor de R$ {valor} à carteira do usuário {usuario.nome}.")
        else:
            Log.info(f"Retirando o valor de R$ {valor} da carteira do usuário {usuario.nome}.")

        Log.info(f"Saldo atual da carteira: R$ {carteira.saldo}.")

    def negociar_acao(self, usuario: Type[Usuario], acao: Type[Acao], tipo: Type[str],  quantidade: Type[int]) -> Type[bool]:
        data_operacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        carteira = usuario.carteira
        preco_medio = acao.preco
        ticker = acao.ticker

        if tipo == "compra":
            # Checa se o valor da compra é maior que o saldo
            valor_total = preco_medio * quantidade
            if carteira.saldo < valor_total:
                Log.error("Saldo insuficiente para compra.")
                return False
            
            boleta = Boleta.criar_boleta(
                data_operacao=data_operacao,
                ticker=ticker,
                quantidade=quantidade,
                preco_medio=preco_medio,
                taxas=0.0,  # Geralmente as taxas sao calculadas na hora da venda
                tipo="compra"
            )

            self.fazer_transacao(usuario, -valor_total)
            carteira.adicionar_acao(acao, quantidade, preco_medio)
            Log.info(f"Comprando {quantidade} ações de {ticker} por R$ {preco_medio} cada. Total: {valor_total}.")
        
        elif tipo == "venda":
            # Checa se a quantidade de ações é maior do que a quantidade na carteira
            if quantidade > carteira.quantidade_acao(acao):
                Log.error("Quantidade insuficiente de ações para venda.")
                return False

            taxas = preco_medio * quantidade * usuario.taxa_corretagem 
            valor_total = preco_medio * quantidade - taxas
            boleta = Boleta.criar_boleta(
                data_operacao=data_operacao,
                ticker=ticker,
                quantidade=quantidade,
                preco_medio=preco_medio,
                taxas=taxas,
                tipo="venda"
            )

            self.fazer_transacao(usuario, valor_total)
            carteira.remover_acao(acao, quantidade)
            Log.info(f"Vendendo {quantidade} ações de {ticker} por R$ {preco_medio} cada. Total: {valor_total}.")
        
        carteira.adicionar_boleta(boleta)
        return True