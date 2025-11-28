from model.clientes import Cliente
from conexion.mongo_queries import MongoQueries
import pandas as pd

class Controller_Cliente:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_cliente(self) -> Cliente:
        self.mongo.connect()

        nome_cliente = input("Informe o nome do novo Cliente: ")

        if self.verifica_existencia_cliente(nome_cliente):
            cpf = input("Informe o CPF do Cliente: ")

            self.mongo.db["clientes"].insert_one({
                "nome_cliente": nome_cliente,
                "cpf": cpf
            })

            df_cliente = self.recupera_cliente(nome_cliente)
            novo_cliente = Cliente(
                df_cliente.id_cliente.values[0],
                df_cliente.nome_cliente.values[0],
                df_cliente.cpf.values[0]
            )

            print("\nCliente inserido com sucesso!")
            print(novo_cliente.to_string())
            input("\nPressione Enter para prosseguir")

            self.mongo.close()
            return novo_cliente

        else:
            print(f"O Cliente '{nome_cliente}' já está cadastrado no sistema.")
            input("\nPressione Enter para prosseguir")
            return None
    

    def atualizar_cliente(self) -> Cliente:
        self.mongo.connect()

        id_cliente = int(input("Informe o ID do Cliente que deseja atualizar: "))

        if self.verifica_existencia_cliente(id_cliente=id_cliente):

         nome_cliente = input("Informe o novo nome do Cliente: ")
         cpf = input("Informe o novo CPF do Cliente: ")

         self.mongo.db["clientes"].update_one(
            { "id_cliente": id_cliente },
            { "$set": {
                "nome_cliente": nome_cliente,
                "cpf": cpf
            }}
         )

         df_cliente = self.recupera_cliente(id_cliente)

         cliente_atualizado = Cliente(
            df_cliente.id_cliente.values[0],
            df_cliente.nome_cliente.values[0],
            df_cliente.cpf.values[0]
         )

         print("\nCliente atualizado com sucesso!")
         print(cliente_atualizado.to_string())
         input("\nPressione Enter para prosseguir")

         self.mongo.close()
         return cliente_atualizado

        else:
            print(f"O ID {id_cliente} não foi encontrado.")
            input("\nPressione Enter para prosseguir")

            self.mongo.close()
            return None


    def excluir_cliente(self) -> Cliente:
     self.mongo.connect()

     id_cliente = int(input("Informe o ID do Cliente que deseja excluir: "))

     if self.verifica_existencia_cliente(id_cliente=id_cliente):

        df_cliente = self.recupera_cliente(id_cliente)

        self.mongo.db["clientes"].delete_one(
            { "id_cliente": id_cliente }
        )

        cliente_excluido = Cliente(
            df_cliente.id_cliente.values[0],
            df_cliente.nome_cliente.values[0],
            df_cliente.cpf.values[0]
        )

        print("\nCliente removido com sucesso!")
        print(cliente_excluido.to_string())
        input("\nPressione Enter para prosseguir")

        self.mongo.close()
        return cliente_excluido

     else:
        print(f"O ID {id_cliente} não foi encontrado.")
        input("\nPressione Enter para prosseguir")

        self.mongo.close()
        return None

    def verifica_existencia_cliente(self, id_cliente: int = None, nome_cliente: str = None, external: bool = False) -> bool:
     if external:
        self.mongo.connect()

    
     filtro = {}
     if id_cliente is not None:
        filtro["id_cliente"] = id_cliente
     if nome_cliente is not None:
        filtro["nome_cliente"] = nome_cliente

     df_cliente = pd.DataFrame(
        list(
            self.mongo.db["clientes"].find(
                filtro,
                { "id_cliente": 1, "nome_cliente": 1, "cpf": 1 }
            )
        )
    )

     if external:
        self.mongo.close()

     return df_cliente.empty

    def recupera_cliente(self, id_cliente: int = None, external: bool = False) -> pd.DataFrame:
     if external:
        self.mongo.connect()

     df_cliente = pd.DataFrame(
        list(
            self.mongo.db["clientes"].find(
                { "id_cliente": id_cliente },
                { "id_cliente": 1, "nome_cliente": 1, "cpf": 1 }
            )
        )
    )

     if external:
        self.mongo.close()

     return df_cliente
