
from utils import config

class SplashScreenLocadora:
    def __init__(self):
        self.created_by = (
           ' Emanoel Vitor V. Atanazio | Felipe R. Barzilai'
           '\n\t\t\tJoão Emanoel Justino | Livia Favato B. Neves'
           '\n\t\t\tRogeres Jose P. da Silva\n'
        )
        self.professor = "Howard Roatti"
        self.disciplina = "Banco de Dados\t2025/2"
       

    def get_total(self, collection_name):
        """Retorna o total de registros de uma tabela"""
        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]

    def get_updated_screen(self):
        """Retorna a splash screen atualizada com os totais"""
        total_clientes = str(self.get_documents_count(collection_name="clientes")).rjust(5)
        total_carros = str(self.get_documents_count(collection_name="carros")).rjust(5)
        total_funcionarios = str(self.get_documents_count(collection_name="funcionarios")).rjust(5)
        total_locacoes = str(self.get_documents_count(collection_name="locacoes")).rjust(5)

        return f"""
        ================= SISTEMA DE LOCAÇÃO DE VEÍCULOS =================
                                                                     
         TOTAL DE REGISTROS:                                             
            1 - CLIENTES:        {total_clientes}                   
            2 - CARROS:          {total_carros}                       
            3 - FUNCIONÁRIOS:    {total_funcionarios}               
            4 - LOCAÇÕES:        {total_locacoes}                   
                                                                     
           CRIADO POR: {self.created_by}                         
           PROFESSOR:  {self.professor}                               
           DISCIPLINA: {self.disciplina}                              
                                                     
         ==============================================================

        """