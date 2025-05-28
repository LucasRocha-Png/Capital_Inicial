# Project
from Log import log
from Database import db
from Pessoa import Pessoa

def main() -> None:
    log.message("Aplicativo iniciado.", "INFO")
    db.start()
    
    user = Pessoa("Lucas", "123.456.789-00", "20/03/2004", "lucasrocha.20166@gmail.com", "senha123")
    db.salvar_usuario(user)
    user.print_info()

    user1 = db.carregar_usuario("123.456.789-00")
    if (user1):
        user1.print_info()

    db.close()

if __name__ == "__main__":
    main()