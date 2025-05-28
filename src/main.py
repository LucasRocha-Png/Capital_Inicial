# Project
from Log import log
from Database import db
from Pessoa import Pessoa

def main() -> None:
    log.message("Aplicativo iniciado.", "INFO")
    db.start()
    
    user = Pessoa("Lucas", "123.456.789-00", "20/03/2004", "lucasrocha.20166@gmail.com", "senha123")
    print("USUARIO CRIADO-------------------------")
    user.print_info()
    user.carteira.print_info()
    user.salvar()

    print("USUARIO CARREGADO---------------------------")
    user_1 = Pessoa.carregar("123.456.789-00")
    user_1.print_info()
    user_1.carteira.print_info()

    db.close()

if __name__ == "__main__":
    main()