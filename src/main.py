# Project
"""
from backend.Usuarios import * 
from backend.Corretora import Corretora
from backend.Log import Log
from database.ManagerAcao import ManagerAcao
from database.ManagerUsuarios import ManagerUsuarios
"""
from frontend.aplicativo import Aplicativo

def main():
    """
    Log.trace("Inicializando o aplicativo...")

    db_usuario = ManagerUsuarios()
    corretora = Corretora()
    db_acoes = ManagerAcao("Brazil") 


    usuario = db_usuario.carregar("12345678901") 
    if usuario is None:
        Log.error("Usuário não encontrado. Criando um novo usuário.")
        usuario = UsuarioDemo(nome="Lucas Rocha", cpf="12345678901", data_nascimento="20/03/2004", email="lucas.rocha@ufmg.br", senha="123456")
        db_usuario.adicionar(usuario)

    corretora.fazer_transacao(usuario, 1000.0)
    acao = db_acoes.carregar("PETR4.SA")
    db_acoes.atualizar([acao])
    corretora.negociar_acao(usuario, acao, "compra", 10)
    db_usuario.salvar()
    """
    
    app = Aplicativo()
    app.mainloop()


if __name__ == "__main__":
    main()
