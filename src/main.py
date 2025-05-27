# Project
from Log import log
from Database import db

def main() -> None:
    log.message("Aplicativo iniciado.", "INFO")
    db.start()
    
    db.close()

if __name__ == "__main__":
    main()