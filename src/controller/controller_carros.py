from model.carros import Carro
from conexion.mongo_queries import MongoQueries
import pandas as pd

class Controller_Carro:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_carro(self) -> Carro:
        self.mongo.connect()

        placa = input("Informe a placa do novo Carro: ")

       
        if not self.verifica_existencia_carro(placa=placa):
            print(f"A placa '{placa}' já está cadastrada no sistema.")
            input("\nPressione Enter para prosseguir")
            self.mongo.close()
            return None

        modelo = input("Informe o modelo do Carro: ")
        categoria = input("Informe a categoria do Carro: ")
        valor_diaria = float(input("Informe o valor da diária de locação: "))

        df_carros = pd.DataFrame(
            list(
                self.mongo.db["carros"].find(
                    {},
                    {"id_carro": 1, "_id": 0}
                )
            )
        )

        proximo_id = 1 if df_carros.empty else int(df_carros["id_carro"].max() + 1)

        self.mongo.db["carros"].insert_one({
            "id_carro": proximo_id,
            "modelo": modelo,
            "placa": placa,
            "categoria": categoria,
            "valor_diaria": valor_diaria
        })

        df_carro = self.recupera_carro(placa=placa)

        novo_carro = Carro(
            df_carro.id_carro.values[0],
            df_carro.modelo.values[0],
            df_carro.placa.values[0],
            df_carro.categoria.values[0],
            df_carro.valor_diaria.values[0]
        )

        print("\nCarro inserido com sucesso!")
        print(novo_carro.to_string())
        input("\nPressione Enter para prosseguir")

        self.mongo.close()
        return novo_carro

    def atualizar_carro(self) -> Carro:
        self.mongo.connect()

        id_carro = int(input("Informe o ID do Carro que deseja alterar: "))

        if self.verifica_existencia_carro(id_carro=id_carro):
            print(f"O Carro com ID {id_carro} não foi encontrado.")
            input("\nPressione Enter para prosseguir")
            self.mongo.close()
            return None

        novo_modelo = input("Informe o novo modelo do Carro: ")
        nova_placa = input("Informe a nova placa do Carro: ")
        nova_categoria = input("Informe a nova categoria do Carro: ")
        novo_valor_diaria = float(input("Informe o novo valor da diária do Carro: "))

        self.mongo.db["carros"].update_one(
            {"id_carro": id_carro},
            {"$set": {
                "modelo": novo_modelo,
                "placa": nova_placa,
                "categoria": nova_categoria,
                "valor_diaria": novo_valor_diaria
            }}
        )

        df_carro = self.recupera_carro(id_carro=id_carro)

        carro_atualizado = Carro(
            df_carro.id_carro.values[0],
            df_carro.modelo.values[0],
            df_carro.placa.values[0],
            df_carro.categoria.values[0],
            df_carro.valor_diaria.values[0]
        )

        print("\nCarro atualizado com sucesso!")
        print(carro_atualizado.to_string())
        input("\nPressione Enter para prosseguir")

        self.mongo.close()
        return carro_atualizado

    def excluir_carro(self) -> Carro:
        self.mongo.connect()

        id_carro = int(input("Informe o ID do Carro a ser excluído: "))

        if self.verifica_existencia_carro(id_carro=id_carro):
            print(f"O Carro com ID {id_carro} não foi encontrado.")
            input("\nPressione Enter para prosseguir")
            self.mongo.close()
            return None

        df_carro = self.recupera_carro(id_carro=id_carro)

        self.mongo.db["carros"].delete_one(
            {"id_carro": id_carro}
        )

        carro_excluido = Carro(
            df_carro.id_carro.values[0],
            df_carro.modelo.values[0],
            df_carro.placa.values[0],
            df_carro.categoria.values[0],
            df_carro.valor_diaria.values[0]
        )

        print("\nCarro removido com sucesso!")
        print(carro_excluido.to_string())
        input("\nPressione Enter para prosseguir")

        self.mongo.close()
        return carro_excluido

    def verifica_existencia_carro(self, placa: str = None, id_carro: int = None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()

        filtro = {}
        if placa is not None:
            filtro["placa"] = placa
        if id_carro is not None:
            filtro["id_carro"] = id_carro

        df_carro = pd.DataFrame(
            list(
                self.mongo.db["carros"].find(
                    filtro,
                    {"id_carro": 1, "placa": 1, "_id": 0}
                )
            )
        )

        if external:
            self.mongo.close()

       
        return df_carro.empty

    def recupera_carro(self, id_carro: int = None, placa: str = None, external: bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        filtro = {}
        if id_carro is not None:
            filtro["id_carro"] = id_carro
        if placa is not None:
            filtro["placa"] = placa

        df_carro = pd.DataFrame(
            list(
                self.mongo.db["carros"].find(
                    filtro,
                    {"id_carro": 1, "modelo": 1, "placa": 1, "categoria": 1, "valor_diaria": 1, "_id": 0}
                )
            )
        )

        if external:
            self.mongo.close()

        return df_carro
