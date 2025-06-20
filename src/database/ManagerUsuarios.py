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
import json

USER_STORAGE_PATH = "data/usuarios"

class ManagerUsuarios(Manager):
    def __init__(self) -> None:
        super().__init__()
        Log.trace("Inicializando ManagerUsuarios...")
        os.makedirs(USER_STORAGE_PATH, exist_ok=True)

    # Pega o caminho na database do usuario
    def __pegar_caminho_usuario(self, email: str) -> str:
        return os.path.join(USER_STORAGE_PATH, f"{email}.json")

    # Carrega o usuario pelo email
    def carregar(self, email: str) -> Usuario | None:
        Log.info(f"Carregando usuário com o Email: {email}")

        path = self.__pegar_caminho_usuario(email)
        if not path:
            Log.error(f"Usuário com email {email} não encontrado.")
            return None

        try:
            with open(path, 'r') as file:
                json_data = json.load(file)
                tipo_conta = json_data.get("tipo_conta")

                if tipo_conta == "padrao":
                    usuario = UsuarioPadrao.from_json(json_data)
                elif tipo_conta == "demo":
                    usuario = UsuarioDemo.from_json(json_data)
                else:
                    Log.error(f"Tipo de conta desconhecido: {tipo_conta}")
                    return None

                Log.info(f"Usuário {usuario.nome} carregado com sucesso.")
                return usuario

        except Exception as e:
            Log.error(f"Erro ao carregar usuário: {e}")
            return None

    # Salva o usuario. Leva como argumento um Usuario.
    def salvar(self, usuario: Usuario):
        Log.info(f"Salvando usuário {usuario.nome}...")
        os.makedirs(USER_STORAGE_PATH, exist_ok=True)

        path = self.__pegar_caminho_usuario(usuario.email)
        with open(path, 'w') as file:
            file.write(usuario.to_json())

        Log.info(f"Usuário {usuario.nome} salvo com sucesso.")

    # Lista os usuarios salvos
    def listar(self) -> None:
        Log.info("Listando todos os usuários salvos:")
        for filename in os.listdir(USER_STORAGE_PATH):
            if filename.endswith(".json"):
                print(filename.replace(".json", ""))
