from model.funcionarios import Funcionario
from conexion.mongo_queries import MongoQueries
import pandas as pd


class Controller_Funcionario:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_funcionario(self) -> Funcionario:
        self.mongo.connect()

        id_funcionario = int(input("Informe o ID do novo Funcionário: "))

        if self.verifica_existencia_funcionario(id_funcionario):
            nome = input("Informe o Nome do Funcionário: ")
            cargo = input("Informe o Cargo do Funcionário: ")

            self.mongo.db["funcionarios"].insert_one({
                "id_funcionario": id_funcionario,
                "nome": nome,
                "cargo": cargo
            })

            df_funcionario = self.recupera_funcionario(id_funcionario)
            novo_funcionario = Funcionario(
                df_funcionario.id_funcionario.values[0],
                df_funcionario.nome.values[0],
                df_funcionario.cargo.values[0]
            )

            print("\nFuncionário inserido com sucesso!")
            print(novo_funcionario.to_string())
            input("\nPressione Enter para prosseguir")

            self.mongo.close()
            return novo_funcionario

        else:
            print(f"O ID {id_funcionario} já está cadastrado.")
            input("\nPressione Enter para prosseguir")
            return None

    def atualizar_funcionario(self) -> Funcionario:
        self.mongo.connect()

        id_funcionario = int(input("Informe o ID do Funcionário que deseja atualizar: "))

        if not self.verifica_existencia_funcionario(id_funcionario):

            nome = input("Informe o novo Nome do Funcionário: ")
            cargo = input("Informe o novo Cargo do Funcionário: ")

            self.mongo.db["funcionarios"].update_one(
                {"id_funcionario": id_funcionario},
                {"$set": {
                    "nome": nome,
                    "cargo": cargo
                }}
            )

            df_funcionario = self.recupera_funcionario(id_funcionario)
            funcionario_atualizado = Funcionario(
                df_funcionario.id_funcionario.values[0],
                df_funcionario.nome.values[0],
                df_funcionario.cargo.values[0]
            )

            print("\nFuncionário atualizado com sucesso!")
            print(funcionario_atualizado.to_string())
            input("\nPressione Enter para prosseguir")

            self.mongo.close()
            return funcionario_atualizado

        else:
            print(f"O ID {id_funcionario} não foi encontrado.")
            input("\nPressione Enter para prosseguir")

            self.mongo.close()
            return None

    def excluir_funcionario(self) -> Funcionario:
        self.mongo.connect()

        id_funcionario = int(input("Informe o ID do Funcionário que deseja excluir: "))

        if not self.verifica_existencia_funcionario(id_funcionario):

            df_funcionario = self.recupera_funcionario(id_funcionario)

            self.mongo.db["funcionarios"].delete_one(
                {"id_funcionario": id_funcionario}
            )

            funcionario_excluido = Funcionario(
                df_funcionario.id_funcionario.values[0],
                df_funcionario.nome.values[0],
                df_funcionario.cargo.values[0]
            )

            print("\nFuncionário removido com sucesso!")
            print(funcionario_excluido.to_string())
            input("\nPressione Enter para prosseguir")

            self.mongo.close()
            return funcionario_excluido

        else:
            print(f"O ID {id_funcionario} não foi encontrado.")
            input("\nPressione Enter para prosseguir")

            self.mongo.close()
            return None

    def verifica_existencia_funcionario(self, id_funcionario: int = None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()

        filtro = {}
        if id_funcionario is not None:
            filtro["id_funcionario"] = id_funcionario

        df_funcionario = pd.DataFrame(
            list(
                self.mongo.db["funcionarios"].find(
                    filtro,
                    {"id_funcionario": 1, "nome": 1, "_id": 0}
                )
            )
        )

        if external:
            self.mongo.close()

        return df_funcionario.empty

    def recupera_funcionario(self, id_funcionario: int = None, external: bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_funcionario = pd.DataFrame(
            list(
                self.mongo.db["funcionarios"].find(
                    {"id_funcionario": id_funcionario},
                    {"id_funcionario": 1, "nome": 1, "cargo": 1, "_id": 0}
                )
            )
        )

        if external:
            self.mongo.close()

        return df_funcionario
