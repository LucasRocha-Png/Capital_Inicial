from backend.Usuarios import UsuarioPadrao 
from database.Downloader import Downloader 
from backend.Corretora import Corretora
from backend.Log import Log

from database.ManagerAcao import ManagerAcao

def main():
    Log.trace("Iniciando o aplicativo")
    db = ManagerAcao()
#    db.print()

if __name__ == "__main__":
    main()