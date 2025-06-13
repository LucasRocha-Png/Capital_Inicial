"""
Lucas Rocha - 10/06/2025
"""

# Third Party
import pandas as pd
import yfinance as yf

# Project
from backend.Log import Log

class Downloader:
    @staticmethod
    def download_ticker(tickers: list[str], period: str = "max") -> dict[pd.DataFrame]:
        df = yf.download(tickers, period=period, interval="1d", auto_adjust=True, group_by='ticker')
        result = {}
        if isinstance(df.columns, pd.MultiIndex):
            for ticker in tickers:
                result[ticker] = df[ticker].dropna().copy().reset_index(drop=True)
        else:
            result[tickers[0]] = df.dropna().copy().reset_index(drop=True)
        return result

