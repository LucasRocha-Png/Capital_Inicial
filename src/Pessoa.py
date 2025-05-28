#Project
from Database import db
from Log import log
from Carteira import Carteira

class Pessoa:
    def __init__(self, nome: str = "", cpf: str = "", data_nascimento: str = "", email: str = "", senha_login: str = "", carteira: Carteira = Carteira()) -> None:
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.email = email
        self.senha_login = senha_login
        self.carteira = carteira
    
    def print_info(self)-> None:
        print(f"Nome: {self.nome}")
        print(f"CPF: {self.cpf}")
        print(f"Data de Nascimento: {self.data_nascimento}")
        print(f"Email: {self.email}")
        print(f"Senha: {self.senha_login}")

    def salvar(self) -> bool:
        try:
            query_check = "SELECT COUNT(*) FROM PESSOA WHERE CPF = ?"
            result = db.fetchone(query_check, (self.cpf,))

            if result and result[0] == 0:
                query = """
                    INSERT INTO PESSOA (NOME, CPF, DATA_NASCIMENTO, EMAIL, SENHA)
                    VALUES (?, ?, ?, ?, ?);
                """
                db.execute(query, (self.nome, self.cpf, self.data_nascimento, self.email, self.senha_login)) 
            else:
                query = """
                    UPDATE PESSOA
                    SET NOME = ?, DATA_NASCIMENTO = ?, EMAIL = ?, SENHA = ?
                    WHERE CPF = ?;
                """
                db.execute(query, (self.nome, self.data_nascimento, self.email, self.senha_login, self.cpf))

            log.message(f"Usuário '{self.nome}' - '{self.cpf}' salvo com sucesso.", "INFO")
        except Exception as e:
            log.message(f"Erro ao salvar usuário '{self.nome}': {str(e)}", "ERROR")
            return False
    
        return self.carteira.salvar(self.nome, self.cpf)

    @classmethod
    def carregar(cls, cpf: str) -> "Pessoa | None":
        try:
            query = "SELECT * FROM PESSOA WHERE CPF = ?"
            row = db.fetchone(query, (cpf,))      

            if row:
                _, cpf_, nome, data_nascimento, email, senha = row

                # carrega a carteira pelo CPF
                carteira = Carteira.carregar(cpf_)
        
                return cls(
                    nome=nome,
                    cpf=cpf_,
                    data_nascimento=data_nascimento,
                    email=email,
                    senha_login=senha,
                    carteira=carteira
                )

            log.message(f"Nenhum usuário encontrado para CPF '{cpf}'.", "WARN")
            return None

        except Exception as e:
            log.message(f"Erro ao carregar usuário com CPF '{cpf}': {e}", "ERROR")
            return None
