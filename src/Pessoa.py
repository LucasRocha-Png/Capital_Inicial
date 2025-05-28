class Pessoa:
    def __init__(self, nome: str, cpf: str, data_nascimento: str, email: str, senha_login: str) -> None:
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.email = email
        self.senha_login = senha_login
    
    def print_info(self)-> None:
        print(f"Nome: {self.nome}")
        print(f"CPF: {self.cpf}")
        print(f"Data de Nascimento: {self.data_nascimento}")
        print(f"Email: {self.email}")
        print(f"Senha: {self.senha_login}")