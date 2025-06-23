# Project
from database.Downloader import Downloader
from database.Manager import Manager
from backend.Acao import Acao
from backend.Log import Log
from typing import Type

# Python
import os

# Third Party
import pandas as pd

TICKER_STORAGE_PATH = "data/acoes"
TICKERS_LIST_PATH = "data/tickers.csv"

class ManagerAcao(Manager):
    def __init__(self, pais: Type[str] = "") -> None:
        super().__init__()
        Log.trace("Inicializando ManagerAcao...")
        self._acoes = self.carregar_acoes_disponiveis(pais)
    
    @property
    def acoes(self) -> Type[list[Acao]]:
        return self._acoes
    
    # Pega o caminho na database da acao
    def __pegar_caminho_acao(self, acao: Type[Acao]) -> Type[str]:
        return os.path.join(TICKER_STORAGE_PATH, acao.pais, f"{acao.ticker}.csv")
    
    # Carrega as acoes disponiveis
    def carregar_acoes_disponiveis(self, pais: Type[str] = "") -> Type[list[Acao]]:
        Log.info("Carregando ações disponíveis...")
        df = pd.read_csv(TICKERS_LIST_PATH)
        
        acoes = []
        for _, row in df.iterrows():
            if pais == "" or row.Country == pais:
                acao = Acao(row.Country, row.Ticker, row.Name, row.Exchange)
                self.carregar_historico(acao)
                acoes.append(acao)

        Log.info(f"Total carregadas: {len(acoes)}")
        return acoes

    # Carrega uma acao pelo ticker
    def carregar(self, ticker: Type[str]) -> Type[Acao] | None:
        for acao in self._acoes:
            if acao.ticker == ticker:
                Log.info(f"Ação {acao.ticker} carregada com sucesso.")
                return acao
            
        Log.error(f"Ação com ticker {ticker} não encontrada.")
        return None

    # Carrega o historico em uma acao
    def carregar_historico(self, acao: Type[Acao]) -> Type[bool]:
            path = self.__pegar_caminho_acao(acao)
            if os.path.isfile(path):
                try:
                    df = pd.read_csv(path, index_col=0, parse_dates=True) 
                    df.index = pd.to_datetime(df.index)

                    acao.atualizar_valores(df)
                    return True
                except Exception as e:
                    return False
            return False
    
    # Salva uma acao
    def salvar(self, acao: Type[Acao]) -> Type[bool]:
        try:
            path = self.__pegar_caminho_acao(acao)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            acao.historico.to_csv(path)
            return True
        
        except Exception as e:
            return False
        
    # Atualiza os preços e os historicos de um conjunto de acoes
    def atualizar(self, acoes: Type[list[Acao]]) -> Type[bool]:
        if len(acoes) == 0:
            Log.info("Nenhuma ação para atualizar.")
            return False
        
        try:
            if len(acoes) == 1:
                Log.info(f"Atualizando {len(acoes)} ação...")
            else:
                Log.info(f"Atualizando {len(acoes)} ações...")
                 
            tickers = [acao.ticker for acao in acoes]
            historicos = Downloader.download_ticker(tickers)
            for acao in acoes:
                if acao.ticker in historicos:
                    acao.atualizar_valores(historicos[acao.ticker])
                    self.salvar(acao)
            
            Log.info("Atualizado com sucesso.")
            return True
        
        except Exception as e:
            return False
    
    # Lista todas acoes disponiveis
    def listar(self) -> None:
        for acao in self._acoes:
            print(acao)