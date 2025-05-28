# Project
from Log import log
from Database import db

class Carteira:
    def __init__(self, saldo: float = 0, senha_transacao: str = "") -> None:
        self.saldo = 0
        self.senha_transacao = ""
        self.boletas = []
        self.acoes = {}
    
    def print_info(self) -> None:
        print(f"Saldo: {self.saldo}")
        print(f"Senha de Transação: {self.senha_transacao}")
        print(f"Boletas: {self.boletas}")
        print(f"Ações: {self.acoes}")

    def salvar(self, nome: str, cpf: str) -> bool:
        try:
            query_check = "SELECT COUNT(*) FROM CARTEIRA WHERE CPF = ?"
            result = db.fetchone(query_check, (cpf,))

            if result and result[0] == 0:
                query = """
                    INSERT INTO CARTEIRA (CPF, SALDO, SENHA_TRANSACAO)
                    VALUES (?, ?, ?);
                """
                db.execute(query, (cpf, self.saldo, self.senha_transacao)) 
            else:
                query = """
                    UPDATE CARTEIRA
                    SET SALDO = ?, SENHA_TRANSACAO = ?
                    WHERE CPF = ?;
                """
                db.execute(query, (self.saldo, self.senha_transacao, cpf))

            log.message(f"Carteira do usuário '{nome}' - '{cpf}' salvo com sucesso.", "INFO")
            return True

        except Exception as e:
            log.message(f"Erro ao salvar a carteira do usuário '{nome}' - '{cpf}': {str(e)}", "ERROR")
            return False
    
    @classmethod
    def carregar(cls, cpf: str) -> "Pessoa | None":

        query = """
            SELECT * FROM CARTEIRA WHERE CPF = ?
        """
        row = db.fetchone(query, (cpf,))

        if row:
            _, cpf_, saldo, senha_transacao = row
            return cls(
                saldo=saldo,
                senha_transacao=senha_transacao,
            )

        return None