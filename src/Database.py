# Project
from Log import Log

# Third Party
import sqlite3

DATABASE_PATH = "./database.sql"

class Database:
    def __init__(self) -> None:
        self.path = DATABASE_PATH
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
