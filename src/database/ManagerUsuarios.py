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

    def __checar_se_existe(self, email: str) -> None:
        return self.__pegar_caminho_usuario(email) is None 

    # Carrega o usuario pelo email
    def carregar(self, email: str) -> Usuario | None:
        Log.info(f"Carregando usuário com o Email: {email}")

        if self.__checar_se_existe(email) == False:
            Log.error(f"Usuário com email {email} não encontrado.")
            return None

        try:
            path = self.__pegar_caminho_usuario(email)
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
    def salvar(self, usuario: Usuario) -> None:
        Log.info(f"Salvando usuário {usuario.nome}...")
        os.makedirs(USER_STORAGE_PATH, exist_ok=True)

        path = self.__pegar_caminho_usuario(usuario.email)
        with open(path, 'w') as file:
            file.write(usuario.to_json())

        Log.info(f"Usuário {usuario.nome} salvo com sucesso.")

    # Adiciona usuario. Se ja existe retorna false, se não, true
    def adicionar(self, usuario: Usuario) -> None:
        if self.__checar_se_existe(usuario.email) == True:
            Log.error(f"Usuário já existe. Não foi possível adicionar")
            return False

        self.salvar(usuario)
        return True

    # Lista os usuarios salvos
    def listar(self) -> None:
        Log.info("Listando todos os usuários salvos:")
        for filename in os.listdir(USER_STORAGE_PATH):
            if filename.endswith(".json"):
                print(filename.replace(".json", ""))
