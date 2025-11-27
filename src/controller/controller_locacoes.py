from datetime import datetime
from model.locacoes import Locacao
from model.clientes import Cliente
from model.carros import Carro
from model.funcionarios import Funcionario
from conexion.mongo_queries import MongoQueries
import pandas as pd


class Controller_Locacao:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_locacao(self) -> Locacao:
        self.mongo.connect()

        id_cliente = int(input("ID do Cliente: "))
        id_carro = int(input("ID do Veículo: "))
        id_funcionario = int(input("ID do Funcionário: "))
        data_inicio = input("Data de Início (dd/mm/aaaa): ")
        data_fim = input("Data de Fim (dd/mm/aaaa): ")

        df_cliente = pd.DataFrame(
            list(
                self.mongo.db["clientes"].find(
                    {"id_cliente": id_cliente}, {"id_cliente": 1, "nome_cliente": 1, "cpf": 1, "_id": 0}
                )
            )
        )
        df_carro = pd.DataFrame(
            list(
                self.mongo.db["carros"].find(
                    {"id_carro": id_carro}, {"id_carro": 1, "modelo": 1, "placa": 1, "_id": 0}
                )
            )
        )
        df_func = pd.DataFrame(
            list(
                self.mongo.db["funcionarios"].find(
                    {"id_funcionario": id_funcionario}, {"id_funcionario": 1, "nome": 1, "_id": 0}
                )
            )
        )

        if df_cliente.empty:
            print(f"Cliente com ID {id_cliente} não encontrado.")
            input("\nPressione Enter para prosseguir")
            self.mongo.close()
            return None
        if df_carro.empty:
            print(f"Veículo com ID {id_carro} não encontrado.")
            input("\nPressione Enter para prosseguir")
            self.mongo.close()
            return None
        if df_func.empty:
            print(f"Funcionário com ID {id_funcionario} não encontrado.")
            input("\nPressione Enter para prosseguir")
            self.mongo.close()
            return None

        data_inicio_dt = datetime.strptime(data_inicio, "%d/%m/%Y")
        data_fim_dt = datetime.strptime(data_fim, "%d/%m/%Y")

        df_reserva = pd.DataFrame(
            list(
                self.mongo.db["locacoes"].find(
                    {"id_carro": id_carro},
                    {"numero_reserva": 1, "data_inicio": 1, "data_fim": 1, "_id": 0}
                )
            )
        )

        for _, locacao in df_reserva.iterrows():
            data_inicio_existente = self._converte_data(locacao["data_inicio"])
            data_fim_existente = self._converte_data(locacao["data_fim"])

            if data_inicio_existente <= data_fim_dt and data_fim_existente >= data_inicio_dt:
                print(f"O carro {id_carro} já está reservado neste período.")
                input("\nPressione Enter para prosseguir")
                self.mongo.close()
                return None

        df_locacoes = pd.DataFrame(
            list(
                self.mongo.db["locacoes"].find(
                    {}, {"numero_reserva": 1, "_id": 0}
                )
            )
        )
        proximo_id = 1 if df_locacoes.empty else int(df_locacoes["numero_reserva"].max() + 1)

        self.mongo.db["locacoes"].insert_one({
            "numero_reserva": proximo_id,
            "data_inicio": data_inicio_dt,
            "data_fim": data_fim_dt,
            "id_cliente": id_cliente,
            "id_carro": id_carro,
            "id_funcionario": id_funcionario
        })

        df_loc = self.recupera_locacao(numero_reserva=proximo_id)

        cliente = Cliente(df_cliente.id_cliente.values[0], df_cliente.nome_cliente.values[0], df_cliente.cpf.values[0])
        carro = Carro(df_carro.id_carro.values[0], df_carro.modelo.values[0])
        funcionario = Funcionario(df_func.id_funcionario.values[0], df_func.nome.values[0])

        nova_locacao = Locacao(
            df_loc.numero_reserva.values[0],
            df_loc.data_inicio.values[0],
            df_loc.data_fim.values[0],
            cliente,
            carro,
            funcionario
        )

        print("\nLocação inserida com sucesso!")
        print(nova_locacao.to_string())
        input("\nPressione Enter para prosseguir")

        self.mongo.close()
        return nova_locacao

    def atualizar_locacao(self) -> Locacao:
        self.mongo.connect()

        numero_reserva = int(input("Número da reserva que deseja atualizar: "))

        if self.verifica_existencia_locacao(numero_reserva=numero_reserva):
            print(f"A reserva {numero_reserva} não existe.")
            input("\nPressione Enter para prosseguir")
            self.mongo.close()
            return None

        data_fim = input("Nova Data de Fim (dd/mm/aaaa): ")
        data_fim_dt = datetime.strptime(data_fim, "%d/%m/%Y")

        self.mongo.db["locacoes"].update_one(
            {"numero_reserva": numero_reserva},
            {"$set": {"data_fim": data_fim_dt}}
        )

        df_loc = self.recupera_locacao(numero_reserva=numero_reserva)
        df_cliente = pd.DataFrame(
            list(
                self.mongo.db["clientes"].find(
                    {"id_cliente": df_loc.id_cliente.values[0]}, {"id_cliente": 1, "nome_cliente": 1, "cpf": 1, "_id": 0}
                )
            )
        )
        df_carro = pd.DataFrame(
            list(
                self.mongo.db["carros"].find(
                    {"id_carro": df_loc.id_carro.values[0]}, {"id_carro": 1, "modelo": 1, "placa": 1, "_id": 0}
                )
            )
        )
        df_func = pd.DataFrame(
            list(
                self.mongo.db["funcionarios"].find(
                    {"id_funcionario": df_loc.id_funcionario.values[0]}, {"id_funcionario": 1, "nome": 1, "_id": 0}
                )
            )
        )

        cliente = Cliente(df_cliente.id_cliente.values[0], df_cliente.nome_cliente.values[0], df_cliente.cpf.values[0])
        carro = Carro(df_carro.id_carro.values[0], df_carro.modelo.values[0])
        funcionario = Funcionario(df_func.id_funcionario.values[0], df_func.nome.values[0])

        loc_atualizada = Locacao(
            df_loc.numero_reserva.values[0],
            df_loc.data_inicio.values[0],
            df_loc.data_fim.values[0],
            cliente,
            carro,
            funcionario
        )

        print("\nLocação atualizada com sucesso!")
        print(loc_atualizada.to_string())
        input("\nPressione Enter para prosseguir")

        self.mongo.close()
        return loc_atualizada

    def excluir_locacao(self):
        self.mongo.connect()

        numero_reserva = int(input("Número da reserva que deseja excluir: "))

        if self.verifica_existencia_locacao(numero_reserva=numero_reserva):
            print(f"A reserva {numero_reserva} não existe.")
            input("\nPressione Enter para prosseguir")
            self.mongo.close()
            return None

        df_loc = self.recupera_locacao(numero_reserva=numero_reserva)

        self.mongo.db["locacoes"].delete_one(
            {"numero_reserva": numero_reserva}
        )

        print("\nLocação removida com sucesso!")
        print(f"Reserva: {df_loc.numero_reserva.values[0]} | ID Cliente: {df_loc.id_cliente.values[0]} | Veículo: {df_loc.id_carro.values[0]}")
        input("\nPressione Enter para prosseguir")

        self.mongo.close()
        return None

    def verifica_existencia_locacao(self, numero_reserva: int = None, id_carro: int = None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()

        filtro = {}
        if numero_reserva is not None:
            filtro["numero_reserva"] = numero_reserva
        if id_carro is not None:
            filtro["id_carro"] = id_carro

        df_loc = pd.DataFrame(
            list(
                self.mongo.db["locacoes"].find(
                    filtro,
                    {"numero_reserva": 1, "id_carro": 1, "_id": 0}
                )
            )
        )

        if external:
            self.mongo.close()

        return df_loc.empty

    def recupera_locacao(self, numero_reserva: int = None, id_carro: int = None, external: bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        filtro = {}
        if numero_reserva is not None:
            filtro["numero_reserva"] = numero_reserva
        if id_carro is not None:
            filtro["id_carro"] = id_carro

        df_loc = pd.DataFrame(
            list(
                self.mongo.db["locacoes"].find(
                    filtro,
                    {"numero_reserva": 1, "data_inicio": 1, "data_fim": 1, "id_cliente": 1, "id_carro": 1, "id_funcionario": 1, "_id": 0}
                )
            )
        )

        if external:
            self.mongo.close()

        return df_loc

    def _converte_data(self, data_valor):
        if isinstance(data_valor, datetime):
            return data_valor
        for formato in ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"]:
            try:
                return datetime.strptime(str(data_valor), formato)
            except ValueError:
                continue
        return datetime.strptime(str(data_valor), "%Y-%m-%d %H:%M:%S")
