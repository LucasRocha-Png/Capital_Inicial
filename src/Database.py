# Project
from Log import log
from Pessoa import Pessoa

# Third Party
import sqlite3

# Python
import os

DATABASE_PATH = "data/database.db"

class Database:
    def __init__(self) -> None:
        self.path = DATABASE_PATH
        os.makedirs(os.path.dirname(self.path), exist_ok=True) # Cria pasta se não existe
    
    def start(self) -> None:
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        if self.conn:
            log.message("Database iniciado.")
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.create_structure()

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            log.message("Database fechada.")
    
    def table_exists(self) -> list:
        query = """
            SELECT name FROM sqlite_master
            WHERE type='table';
        """
        cursor = self.conn.execute(query)
        return [row[0] for row in cursor.fetchall()]

    def create_structure(self) -> None:
        # Pega as tabelas já existentes
        tables_before = set(self.table_exists())

        # Tabela de ações ------------------------
        query = """
            CREATE TABLE IF NOT EXISTS ACAO (
                TICKER TEXT PRIMARY KEY,
                NOME_EMPRESA TEXT NOT NULL
            );
        """
        self.conn.execute(query)
        # ---------------------------------------   

        # Tabela de pessoas ---------------------
        query = """
            CREATE TABLE IF NOT EXISTS PESSOA (
                PESSOA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME TEXT NOT NULL,
                CPF TEXT UNIQUE NOT NULL,
                DATA_NASCIMENTO TEXT NOT NULL,
                EMAIL TEXT UNIQUE NOT NULL,
                SENHA TEXT NOT NULL
            );
        """
        self.conn.execute(query)
        # -----------------------------------------

        # Tabela de Boletas associada à Pessoa ---------------------
        query = """
            CREATE TABLE IF NOT EXISTS BOLETA (
                BOLETA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                PESSOA_ID INTEGER NOT NULL,
                DATA TEXT NOT NULL,
                TICKER TEXT NOT NULL,
                QUANTIDADE INTEGER NOT NULL,
                PRECO_MEDIO REAL NOT NULL,
                TIPO TEXT NOT NULL,
                FOREIGN KEY (PESSOA_ID) REFERENCES PESSOA(PESSOA_ID),
                FOREIGN KEY (TICKER) REFERENCES ACAO(TICKER)
            );
        """
        self.conn.execute(query)
        # -----------------------------------------

        self.conn.commit()

        # Loga as tabelas criadas
        tables_after = set(self.table_exists())
        created_tables = tables_after - tables_before
        if created_tables:
            for table in created_tables:
                log.message(f"Tabela '{table}' criada.", "INFO")
    
    def salvar_usuario(self, pessoa: Pessoa) -> bool:
        try:
            query = """
                INSERT INTO PESSOA (NOME, CPF, DATA_NASCIMENTO, EMAIL, SENHA)
                VALUES (?, ?, ?, ?, ?);
            """
            self.conn.execute(query, (pessoa.nome, pessoa.cpf, pessoa.data_nascimento, pessoa.email, pessoa.senha_login))
            self.conn.commit()
            log.message(f"Usuário '{pessoa.nome}' salvo com sucesso.", "INFO")
            return True
        except sqlite3.IntegrityError as e:
            log.message(f"Erro ao salvar usuário: {e}", "ERROR")
            return False

    def carregar_usuario(self, cpf: str) -> Pessoa:
        quary = """
            SELECT * FROM PESSOA WHERE cpf = ?
        """
        cursor = self.conn.execute(quary, (cpf,))
        row = cursor.fetchone()
        if row:
            return Pessoa(
                nome=row[1],
                cpf=row[2],
                data_nascimento=row[3],
                email=row[4],
                senha_login=row[5]
            )
        return None

db = Database()