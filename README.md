# SISTEMA DE LOCAÇÃO DE VEÍCULOS 
Este sistema é baseado em um fluxo híbrido Oracle - MongoDB, onde os dados armazenados no Oracle são extraídos e enviados para coleções MongoDB que serão utilizadas pelo restante da aplicação. 
O sistema representa um ambiente de locação de veículos, contendo as seguintes coleções no MongoDB: 

- Carros;
- Cliente;
- Funcionário;
- Locações;

Essas coleções são povoadas automaticamente a partir das tabelas equivalentes existentes no banco Oracle.

## Criação das Coleções e Inserção dos Documentos 
Antes de executar o sistema, é obrigatório criar as coleções e preencher o MongoDB com os dados extraídos do Oracle. 
$ python createCollectionsAndData.py 

Esse script realiza automaticamente: 
- Criação das coleções no MongoDB (carros, cliente, funcionario, locacoes);
- Drop das coleções caso já existam;
- Extração de dados das tabelas do Oracle;
- Conversão dos registros para JSON;
- Inserção dos documentos no MongoDB;

*Para o script funcionar corretamente, é necessário que as tabelas já existam no Oracle e estejam preenchidas.*

## Criar as Tabelas e Populá-las no Oracle 
Antes de sincronizar para o MongoDB, execute: 
$ python create_tables_and_records.py 

Esse script: 
- Cria as tabelas necessárias no Oracle (carros, cliente, funcionario, locacoes);
- Insere registros de exemplo.

## Como Executar o Projeto:
1. Clone o repositório:
git clone https://github.com/barzifelipe/car_rental_system.git

2. Crie as tabelas:
[Executar create_tables_and_records.py](./src/create_tables_and_records.py)

3. Execute o sistema:
[Executar principal.py](./src/principal.py)

## Organização do Projeto
-src/conexion:
 Contém os módulos de conexão com Oracle e MongoDB.
 
-src/controller:
 Classes responsáveis por inserir, atualizar e remover documentos.

-src/model:
 Classes que representam as entidades do sistema.

-src/reports
 Classe responsável por gerar relatórios.

-src/utils
 Scripts auxiliares: config.py / splash_screen.py

-createCollectionsAndData.py:
 Cria coleções e popula o MongoDB com dados do Oracle.

-principal.py:
 Interface principal com o usuário.

## Tecnologias Utilizadas
>Python;
>POO;
>Oracle;
>MongoDB
>pymongo;
>oracledb;
>pandas;
>json;
>logging;
>Mermaid (para o diagrama ER);
>GitHub.

## Autores:
Emanoel Vitor Atanazio Ventura;
Felipe Rodrigues Barzilai;
João Emanoel Justino;
Rogeres José Prates da Silva;
Livia Favato Bastos Neves.












