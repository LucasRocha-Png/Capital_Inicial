# Python
from datetime import datetime

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

    def fazer_transacao(self, usuario: Usuario, valor: float) -> None:
        carteira = usuario.carteira
        carteira.saldo += valor

        if valor > 0:
            Log.info(f"Adicionando o valor de R$ {valor} à carteira do usuário {usuario.nome}.")
        else:
            Log.info(f"Retirando o valor de R$ {valor} da carteira do usuário {usuario.nome}.")
        Log.info(f"Saldo atual da carteira: R$ {carteira.saldo}")

    def negociar_acao(self, usuario: Usuario, acao: Acao, tipo: str,  quantidade: int) -> None:
        carteira = usuario.carteira
        
        if tipo == "compra":
            valor_total = acao.preco * quantidade
            if carteira.saldo < valor_total:
                Log.error("Saldo insuficiente para compra.")
                return
            self.fazer_transacao(usuario, -valor_total)
            boleta = Boleta.criar_boleta(
                data_operacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ticker=acao.ticker,
                quantidade=quantidade,
                preco_medio=acao.preco,
                taxas=0.0,  # Geralmente as taxas sao calculadas na hora da venda
                tipo="compra"
            )
            carteira.adicionar_acao(acao, quantidade)
            Log.info(f"Comprando {quantidade} ações de {acao.ticker} por R$ {acao.preco} cada. Total: {valor_total}")
        
        elif tipo == "venda":
            if quantidade > carteira.quantidade_acao(acao.ticker):
                Log.error("Quantidade insuficiente de ações para venda.")
                return

            taxas = acao.preco * quantidade * usuario.taxa_corretagem 
            valor_total = acao.preco * quantidade - taxas

            self.fazer_transacao(usuario, valor_total)
            boleta = Boleta.criar_boleta(
                data_operacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ticker=acao.ticker,
                quantidade=quantidade,
                preco_medio=acao.preco,
                taxas=taxas,
                tipo="venda"
            )
            carteira.remover_acao(acao, quantidade)
            Log.info(f"Vendendo {quantidade} ações de {acao.ticker} por R$ {acao.preco} cada. Total: {valor_total}")
        
        carteira.adicionar_boleta(boleta)