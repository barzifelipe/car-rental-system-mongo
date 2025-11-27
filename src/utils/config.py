import os
from conexion.mongo_queries import MongoQueries
import pandas as pd

# MENUS

MENU_PRINCIPAL = """
================== MENU PRINCIPAL ==================
1 - Relatórios
2 - Inserir registro
3 - Atualizar registro
4 - Excluir registro
5 - Sair
======================================================
"""

MENU_RELATORIOS = """
================== RELATÓRIOS ==================
1 - Relatório de Clientes
2 - Relatório de Carros
3 - Relatório de Funcionários
4 - Relatório de Locações
5 - Relatório de Valor Diárias por Categoria
6 - Voltar
===============================================
"""

MENU_ENTIDADES = """
================== ENTIDADES ==================
1 - Clientes
2 - Carros
3 - Funcionários
4 - Locações
5 - Voltar
==============================================
"""


# Consulta de contagem de registros por tabela.
def query_count(collection_name):
    mongo = MongoQueries()
    mongo.connect()

    my_collection = mongo.db[collection_name]
    total_documentos = my_collection.count_documents({})

    mongo.close()

    df = pd.DataFrame({f"total_{collection_name}": [total_documentos]})
    return df


# Limpa o console após aguardar um tempo determinado.
def clear_console(wait_seconds: int = 0):
    import time
    if wait_seconds > 0:
        time.sleep(wait_seconds)
    os.system('cls' if os.name == 'nt' else 'clear')


