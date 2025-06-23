"""
Lucas Rocha - 10/06/2025

Serve para armazenar no arquivo data/log.txt mensagens de log
"""

# Python
from datetime import datetime
from typing import Type
import os

LOG_PATH = "data/log.txt"

class Log:
    @staticmethod
    def message(level: Type[str], message: Type[str]) -> None:
        horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{horario}] [{level}] - {message}"
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as file:
            print(log_line)
            file.write(log_line+"\n")

    @classmethod
    def info(cls, message: Type[str]) -> None:
        cls.message("INFO", message)

    @classmethod
    def trace(cls, message: Type[str]) -> None:
        cls.message("TRACE", message)

    @classmethod
    def debug(cls, message: Type[str]) -> None:
        cls.message("DEBUG", message)
    
    @classmethod
    def warning(cls, message: Type[str]) -> None:
        cls.message("WARNING", message)

    @classmethod
    def error(cls, message: Type[str]) -> None:
        cls.message("ERROR", message)
