# Project
from database.Downloader import Downloader
from database.Manager import Manager
from backend.Acao import Acao
from backend.Log import Log

# Python
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third Party
import pandas as pd

TICKER_STORAGE_PATH = "data/acoes"
TICKERS_LIST_PATH = "data/tickers.csv"
_MAX_WORKERS = min(32, (os.cpu_count() or 1) * 5)


class ManagerAcao(Manager):
    def __init__(self, pais: str = "") -> None:
        super().__init__()
        Log.trace("Inicializando ManagerAcao...")
        self.acoes = self.__carregar_disponiveis(pais)
    
    def __pegar_caminho_acao(self, acao: Acao) -> str:
        return os.path.join(TICKER_STORAGE_PATH, acao.pais, f"{acao.ticker}.csv")
    
    def __carregar_disponiveis(self, pais: str = "") -> list[Acao]:
        Log.info("Carregando ações disponíveis...")
        df = pd.read_csv(TICKERS_LIST_PATH)
        
        acoes = []
        for _, row in df.iterrows():
            if pais == "" or row.Country == pais:
                acoes.append(Acao(row.Country, row.Ticker, row.Name, row.Exchange))

        Log.info(f"Total carregadas: {len(acoes)}")
        return acoes

    def carregar(self, ticker: str) -> Acao | None:
        for acao in self.acoes:
            if acao.ticker == ticker:
                Log.info(f"Ação {acao.ticker} carregada com sucesso.")
                return acao
            
        Log.error(f"Ação com ticker {ticker} não encontrada.")
        return None

    def carregar_historico(self, acao: Acao) -> bool:
        try:
            path = self.__pegar_caminho_acao(acao)
            df = pd.read_csv(path, index_col=0, parse_dates=True) 
            acao.atualizar(df)
            return True
        
        except Exception as e:
            return False
    

    def salvar(self, acao: Acao) -> bool:
        try:
            path = self.__pegar_caminho_acao(acao)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            acao.historico.to_csv(path)
            return True
        
        except Exception as e:
            return False
        
    def atualizar(self, acoes: list[Acao]) -> bool:
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
            return True
        
        except Exception as e:
            return False
    
    def listar(self) -> None:
        for acao in self.acoes:
            print(acao)