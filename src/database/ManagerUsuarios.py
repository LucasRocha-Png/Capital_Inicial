# Project
from database.Manager import Manager
from backend.Usuarios import *
from backend.Carteira import Carteira
from database.Downloader import Downloader
from database.ManagerAcao import ManagerAcao
from backend.Log import Log
from backend.Acao import Acao

# Python
import os

USER_STORAGE_PATH = "data/usuarios"

class ManagerUsuarios(Manager):
    def __init__(self) -> None:
        super().__init__()
        Log.trace("Inicializando ManagerUsuarios...")
        os.makedirs(USER_STORAGE_PATH, exist_ok=True)
        self.usuarios = self.__carregar_usuarios()

    def __carregar_usuarios(self) -> list[UsuarioPadrao]:
        Log.info("Carregando usuários disponíveis...")
        
        usuarios = []
        for filename in os.listdir(USER_STORAGE_PATH): # Entra nas pasta de usuários
            if filename.endswith(".json"): # Pega os arquivos JSON
                path = os.path.join(USER_STORAGE_PATH, filename)
                with open(path, 'r') as file: # Carrega o usuario
                    json_data = json.loads(file.read())
                    tipo_conta = json_data["tipo_conta"]

                    # Verifica o tipo de conta
                    if tipo_conta == "padrao":
                        usuario = UsuarioPadrao.from_json(json_data)
                    elif tipo_conta == "demo":
                        usuario = UsuarioDemo.from_json(json_data)

                    usuarios.append(usuario)

        return usuarios
    
    def carregar(self, email: str, senha: str) -> Usuario | None:
        Log.info(f"Carregando usuário com e-mail: {email}")
        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                Log.info(f"Usuário {usuario.nome} carregado com sucesso.")
                return usuario
        Log.error(f"Usuário com e-mail {email} e senha especificada não encontrado.")
        return None

    def adicionar(self, novo_usuario: Usuario):
        for usuario in self.usuarios:
            if usuario.email == novo_usuario.email:
                usuario = novo_usuario
                Log.info(f"Usuário {novo_usuario.nome} já existe. Usuário atualizado.")
                return 

        self.usuarios.append(novo_usuario)
        Log.info(f"Usuário {novo_usuario.nome} adicionado com sucesso.")
    
    def salvar(self):
        Log.info("Salvando usuários...")
        os.makedirs(USER_STORAGE_PATH, exist_ok=True)
        for usuario in self.usuarios:
            path = os.path.join(USER_STORAGE_PATH, f"{usuario.email}.json")
            with open(path, 'w') as file:
                file.write(usuario.to_json())
        Log.info(f"Total de usuários salvos: {len(self.usuarios)}")
    
    def listar(self) -> None:
        for usuario in self.usuarios:
            print(usuario)