import logging as l
from conexion.mongo_queries import MongoQueries
from conexion.oracle_queries import OracleQueries
import json

LISTA_COLECOES = ["carros", "clientes", "funcionarios", "locacoes"]
logger = l.getLogger(name="Example_CRUD_MongoDB")
logger.setLevel(level=l.WARNING)
mongo = MongoQueries()


def createCollections(drop_if_exists:bool=False):

    mongo.connect()
    existing_collections = mongo.db.list_collection_names()
    for colecao in LISTA_COLECOES:
        if colecao in existing_collections:
            if drop_if_exists:
                mongo.db.drop_collection(colecao)
                logger.warning(f"{colecao} droppada!")
                mongo.db.create_collection(colecao)
                logger.warning(f"{colecao} criada!")
        else:
            mongo.db.create_collection(colecao)
            logger.warning(f"{colecao} criada!")
    
    mongo.close()

def insert_many(data:json, colecao:str):
    mongo.connect()
    mongo.db[colecao].insert_many(data)
    mongo.close()


def extract_and_insert():
    oracle = OracleQueries()
    oracle.connect()
    sql = "select * from labdatabase.{table}"
    for colecao in LISTA_COLECOES:
        df = oracle.sqlToDataFrame(sql.format(table=colecao))
        if colecao == "locacoes":
            df["data_inicio"] = df["data_inicio"].dt.strftime("%m-%d-%Y")
            df["data_fim"] = df["data_fim"].dt.strftime("%m-%d-%Y")
        logger.warning(f"Dados extraídos do banco de dados oracle labdatabase.{colecao}")
        records = json.loads(df.T.to_json()).values()
        logger.warning("Dados convertidos para json")
        insert_many(data=records, colecao=colecao)
        logger.warning(f"documentos gerados em {colecao}")

if __name__ == "__main__":
    l.warning("Iniciando")
    createCollections(drop_if_exists=True)
    extract_and_insert()
    l.warning("Finalizado!")