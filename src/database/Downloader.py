"""
Lucas Rocha - 10/06/2025
"""

# Third Party
import pandas as pd
import yfinance as yf
from typing import Type

# Project
from backend.Log import Log


class Downloader:
    # Baixa um conjunto de tickers
    @staticmethod
    def download_ticker(tickers: Type[list[str]], period: Type[str] = "max") -> dict[pd.DataFrame]:
        df = yf.download(tickers, period=period, interval="1d", auto_adjust=True, group_by='ticker')
        result = {}
        if isinstance(df.columns, pd.MultiIndex):
            for ticker in tickers:
                result[ticker] = df[ticker].dropna().copy()
        else:
            result[tickers[0]] = df.dropna().copy()
        return result

