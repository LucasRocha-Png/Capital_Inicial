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
from typing import Type

USER_STORAGE_PATH = "data/usuarios"

class ManagerUsuarios(Manager):
    def __init__(self) -> None:
        super().__init__()
        Log.trace("Inicializando ManagerUsuarios...")
        os.makedirs(USER_STORAGE_PATH, exist_ok=True)

    # Pega o caminho na database do usuario
    def __pegar_caminho_usuario(self, email: Type[str]) -> Type[str]:
        return os.path.join(USER_STORAGE_PATH, f"{email}.json")

    def checar_se_existe(self, email: Type[str]) -> Type[bool]:
        path = self.__pegar_caminho_usuario(email)
        return os.path.isfile(path)

    # Carrega o usuario pelo email e pela senha
    def carregar(self, email: Type[str], senha: Type[str]) -> Type[Usuario] | None:
        Log.info(f"Carregando usuário com o Email: {email}")

        if self.checar_se_existe(email) == False:
            Log.error(f"Usuário com email {email} não encontrado.")
            return None

        try:
            path = self.__pegar_caminho_usuario(email)
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            Log.error(f"Erro ao ler dados do usuário {email}: {e}")
            return None

        if data.get("senha") != senha:
            Log.warning(f"Falha de autenticação para {email}: senha incorreta.")
            return None

        tipo = data.get("tipo_conta")
        if tipo == "padrao":
            usuario = UsuarioPadrao.from_json(data)
        elif tipo == "demo":
            usuario = UsuarioDemo.from_json(data)
        else:
            Log.error(f"Tipo de conta desconhecido: {tipo}")
            return None

        Log.info(f"Usuário {usuario.email} carregado com sucesso.")
        return usuario        

    # Salva o usuario. Leva como argumento um Usuario.
    def salvar(self, usuario: Type[Usuario]) -> None:
        if not usuario:
            Log.warning("Ao salvar o usuario, foi passado um None.")
            return 

        Log.info(f"Salvando usuário {usuario.nome}...")
        os.makedirs(USER_STORAGE_PATH, exist_ok=True)

        path = self.__pegar_caminho_usuario(usuario.email)
        with open(path, 'w') as file:
            file.write(usuario.to_json())

        Log.info(f"Usuário {usuario.nome} salvo com sucesso.")

    # Adiciona usuario. Se ja existe retorna false, se não, true
    def adicionar(self, usuario: Type[Usuario]) -> Type[bool]:
        if self.checar_se_existe(usuario.email) == True:
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
