from conexion.oracle_queries import OracleQueries
from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        with open("/home/labdatabase/Documents/car_rental_system/src/sql/relatorio_carros_sistema.sql") as f:
            self.query_relatorio_carros_sistema = f.read()

        with open("/home/labdatabase/Documents/car_rental_system/src/sql/relatorio_clientes.sql") as f:
            self.query_relatorio_clientes = f.read()

        with open("/home/labdatabase/Documents/car_rental_system/src/sql/relatorio_funcionarios.sql") as f:
            self.query_relatorio_funcionarios = f.read()

        with open("/home/labdatabase/Documents/car_rental_system/src/sql/relatorio_locacao.sql") as f:
            self.query_relatorio_locacao = f.read()

        with open("/home/labdatabase/Documents/car_rental_system/src/sql/relatorio_total_valor_diarias.sql") as f:
            self.query_relatorio_total_valor_diarias = f.read()

    
   # INICIO DOS RELATÓRIOS DO ORACLE !!!!!!!!
    
    def get_relatorio_carros_sistema(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_carros_sistema))
        input("\nPressione Enter para prosseguir ou sair\n")

    def get_relatorio_clientes(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_clientes))
        input("\nPressione Enter para prosseguir ou sair\n")
    
    def get_relatorio_funcionarios(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_funcionarios))
        input("\nPressione Enter para prosseguir ou sair\n")

    def get_relatorio_locacao(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_locacao))
        input("\nPressione Enter para prosseguir ou sair\n")

    def get_relatorio_total_valor_diarias(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_total_valor_diarias))
        input("\nPressione Enter para prosseguir ou sair\n")


# FIM DOS RELATÓRIOS ORACLE !!!!

#INICO DOS RELATÓRIOS DO MONGO !!

# CLIENTES MONGO
def get_relatorio_clientes_mongo(self):
    mongo = MongoQueries()
    mongo.connect()
    query_result = mongo.db["clientes"].find({}, 
                                             {"ID_CLIENTE": 1,
                                              "NOME_CLIENTE": 1,
                                              "CPF": 1,
                                              "_id":0
                                            }).sort("NOME_CLIENTE", ASCENDING)

    df_cliente = pd.DataFrame(list(query_result))
    mongo.close()
    print(df_cliente)
    input("Pressione Enter para sair do relatório de clientes")



#FUNCIONARIOS MONGO
def get_relatorio_funcionarios_mongo(self):
    mongo = MongoQueries()
    mongo.connect()
    query_result = mongo.db["funcionarios"].find({}, 
                                                {"ID_FUNCIONARIO": 1,
                                                 "NOME": 1,
                                                 "CARGO": 1,
                                                 "_id": 0
                                                }).sort("nome", ASCENDING)
    
    df_funcionario = pd.DataFrame(list(query_result))
    mongo.close()
    print(df_funcionario)
    input("Pressioone Enter para sair do relatório de funcionários")


#CARROS MONGO
def get_relatorios_carros_mongo(self):
    mongo = MongoQueries()
    mongo.connect()
    query_results = mongo.db["carros"].find({}, 
                                            {"ID_CARRO": 1,
                                             "MODELO": 1,
                                             "PLACA": 1,
                                             "CATEGORIA": 1,
                                             "VALOR_DIARIA": 1,
                                             "_id": 0
                                            }).sort("MODELO", ASCENDING)
    
    df_carro = pd.DataFrame(list(query_results))
    mongo.close()
    print(df_carro)
    input("Pressione Enter para sair do relatório de carros")


#LOCACOES MONGO
def get_relatorio_locacoes_mongo(self):
    mongo = MongoQueries()
    mongo.connect()
    query_result = mongo.db["locacoes"].aggregate([
                                                  {
                                                      '$lookup':{
                                                          'from': 'clientes',
                                                          'localField': 'ID_CLIENTE',
                                                          'foreignField': 'ID_CLIENTE',
                                                          'as': 'cliente'
                                                      }
                                                  }, {
                                                      '$unwind':{
                                                          'path': '$cliente'
                                                      }
                                                  },{
                                                      '$lookup': {
                                                          'from': 'carros',
                                                          'localField': 'id_carro',
                                                          'foreignField': 'id_carro',
                                                          'as': 'carro'
                                                      }
                                                  }, {
                                                      '$unwind':{
                                                          'path': '$carro'
                                                      }
                                                  }, {
                                                      '$lookup':{
                                                          'from': 'funcionarios',
                                                          'localField': 'id_funcionario',
                                                          'foreignField': 'id_funcionario',
                                                          'as': 'funcionario'
                                                      }
                                                  }, {
                                                      '$unwind':{
                                                          'path': '$funcionario'
                                                      }
                                                  }, {
                                                      '$project':{
                                                          '_id': 0,
                                                          'numero_reserva': 1,
                                                          'data_inicio': {
                                                              '$dateToString': {'format: "%d/%m/%Y", date: $data_inicio'}
                                                          },
                                                          'data_fim': {
                                                              '$dateToString': {'format: "%d/%m/%Y", date: $data_fim'}
                                                          },
                                                          'nome_cliente': '$cliente.nome_cliente',
                                                          'modelo_carro': '$carro.modelo',
                                                          'nome_funcionario': '$funcionario.nome'
                                                      }
                                                  },
                                                  {'$sort': {'numero_reserva': 1}}
                                                 ])
    
    df_locaco = pd.DataFrame(list(query_result))
    mongo.close()
    print(df_locaco[["numero_reserva", "data_inicio", "data_fim", "nome_cliente", "modelo_carro", "nome_funcionario"]])
    input("Pressione Enter para sair do relatório de locações")