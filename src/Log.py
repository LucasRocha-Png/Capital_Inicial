"""
# TRACE: Informações muito detalhadas para depuração profunda.
# DEBUG: Informações úteis para desenvolvimento e testes.
# INFO: Eventos normais do sistema (inicializações, conexões, etc).
# WARN: Algo inesperado, mas a execução continua.
# ERROR: Erros que afetam uma funcionalidade, mas não travam o sistema.
# FATAL: Erros críticos que impedem a continuação da aplicação.
"""

# Python
import datetime
import os 

LOG_PATH = "data/log.txt"

class Log:
    def __init__(self):
        self.path = LOG_PATH
        os.makedirs(os.path.dirname(self.path), exist_ok=True) # Cria pasta se não existe
        self.message("Log iniciado.")

    def message(self, message, level='INFO'):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f_message = f"[{date}] [{level}] - {message}"
        #print(f_message)
        with open(self.path, 'a') as f:
            f.write(f_message + '\n')
        
log = Log()