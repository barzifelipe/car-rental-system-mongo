from utils import config
from utils.splash_screen import SplashScreenLocadora
from controller.controller_cliente import Controller_Cliente
from controller.controller_carros import Controller_Carro
from controller.controller_funcionarios import Controller_Funcionario
from controller.controller_locacoes import Controller_Locacao
from reports.relatorios import Relatorio
import time

tela_inicial = SplashScreenLocadora()
relatorio = Relatorio()
ctrl_cliente = Controller_Cliente()
ctrl_carro = Controller_Carro()
ctrl_funcionario = Controller_Funcionario()
ctrl_locacao = Controller_Locacao()


def reports(opcao_relatorio: int = 0):
    if opcao_relatorio == 1:
        relatorio.get_relatorio_clientes_mongo() 
    elif opcao_relatorio == 2:
        relatorio.get_relatorios_carros_mongo() 
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_funcionarios_mongo() 
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_locacoes_mongo() 
    elif opcao_relatorio == 5:
        relatorio.get_relatorio_total_valor_diarias() 

def inserir(opcao_inserir: int = 0):
    if opcao_inserir == 1:
        ctrl_cliente.inserir_cliente()
    elif opcao_inserir == 2:
        ctrl_carro.inserir_carro()
    elif opcao_inserir == 3:
        ctrl_funcionario.inserir_funcionario()
    elif opcao_inserir == 4:
        ctrl_locacao.inserir_locacao()


def atualizar(opcao_atualizar: int = 0):
    if opcao_atualizar == 1:
        relatorio.get_relatorio_clientes()
        ctrl_cliente.atualizar_cliente()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_carros_sistema()
        ctrl_carro.atualizar_carro()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_funcionarios()
        ctrl_funcionario.atualizar_funcionario()
    elif opcao_atualizar == 4:
        relatorio.get_relatorio_locacao()
        ctrl_locacao.atualizar_locacao()


def excluir(opcao_excluir: int = 0):
    if opcao_excluir == 1:
        relatorio.get_relatorio_clientes()
        ctrl_cliente.excluir_cliente()
    elif opcao_excluir == 2:
        relatorio.get_relatorio_carros_sistema()
        ctrl_carro.excluir_carro()
    elif opcao_excluir == 3:
        relatorio.get_relatorio_funcionarios()
        ctrl_funcionario.excluir_funcionario()
    elif opcao_excluir == 4:
        relatorio.get_relatorio_locacao()
        ctrl_locacao.excluir_locacao()


def run():
    print(tela_inicial.get_updated_screen())
    time.sleep(4)
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)

        if opcao == 1:
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [1-6]: "))
            config.clear_console(1)
            if opcao_relatorio != 0:
                reports(opcao_relatorio)
            config.clear_console()

        elif opcao == 2:
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)
            inserir(opcao_inserir)
            config.clear_console()
            print(tela_inicial.get_updated_screen())
            time.sleep(1)
            config.clear_console()

        elif opcao == 3:
            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-4]: "))
            config.clear_console(1)
            atualizar(opcao_atualizar)
            config.clear_console()
            print(tela_inicial.get_updated_screen())
            time.sleep(1)
            config.clear_console()

        elif opcao == 4:
            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-4]: "))
            config.clear_console(1)
            excluir(opcao_excluir)
            config.clear_console()
            print(tela_inicial.get_updated_screen())
            time.sleep(1)
            config.clear_console()

        elif opcao == 5:
            print(tela_inicial.get_updated_screen())
            time.sleep(2)
            config.clear_console()
            print("Obrigado por utilizar o Sistema da Locadora!")
            break

        else:
            print("Opção inválida. Tente novamente.")
            config.clear_console(2)

if __name__ == "__main__":
    run()
