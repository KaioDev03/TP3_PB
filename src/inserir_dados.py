import sqlite3
import csv
'''Importação das bibliotecas e cada função faz a abertura do arquivo.csv específico para adicionar seus valores.'''
def inserir_departamentos(cursor):
    with open('./data/departamentos.csv', mode = 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            cursor.execute('''
            INSERT INTO departamentos(nome,horario_funcionamento)
            VALUES (?, ?)''', (row['nome'], row['horario_funcionamento']))
            
            print("Dados inseridos com sucesso!")
'''Inserção dos dados da tabela funcionário.'''    
def inserir_funcionarios(cursor):
    with open('./data/funcionarios.csv', mode = 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            cursor.execute('''
            INSERT INTO funcionarios(nome, idade, cargo_id, nome_departamento)
            VALUES (?, ?, ?, ?)''', (row['nome'], int(row['idade']), int(row['cargo_id']), row['nome_departamento']))
            
            print("Dados inseridos com sucesso!")
'''Inserção dos dados da tabela dependentes.'''            
def inserir_dependentes(cursor):
    with open('./data/dependentes.csv', mode = 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            cursor.execute('''
            INSERT INTO dependentes(funcionario_id, nome, idade, parentesco, genero)
            VALUES (?, ?, ?, ?, ?)''', (int(row['funcionario_id']), row['nome'], int(row['idade']), row['parentesco'], row['genero']))
            
            print("Dados inseridos com sucesso!")
'''Inserção dos dados da tabela cargos'''            
def inserir_cargos(cursor):
    with open('./data/cargos.csv', mode = 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            cursor.execute('''
            INSERT INTO cargos(nome,nivel)
            VALUES (?, ?)''', (row['nome'], row['nivel']))
            
            print("Dados inseridos com sucesso!")
'''Inserção dos dados da tabela historico_salario'''            
def inserir_historico_salario(cursor):
    with open('./data/historico_salarios.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            cursor.execute('''
            INSERT INTO historico_salarios (funcionario_id, data_aumento, salario_anterior, salario_atual)
            VALUES (?, ?, ?, ?)''', (row['funcionario_id'], row['data_aumento'], row['salario_anterior'], row['salario_atual']))
            
            print("Dados de histórico de salário inseridos com sucesso!")
            
def main():
    '''Função principal para gerenciar a inserção de dados no banco de dados da empresa
    
    Esta função estabelece uma conexão com o banco de dados da empresa e insere os dados chamando a função específica, após isso realiza o commit das alterações e fecha a conexão com o banco de dados'''
    
    conn = sqlite3.connect('./db/empresa.db', timeout=1000)
    cursor = conn.cursor()
    
    '''Inserção dos dados'''
    
    inserir_departamentos(cursor)
    inserir_dependentes(cursor)
    inserir_funcionarios(cursor)
    inserir_cargos(cursor)
    inserir_historico_salario(cursor)
    
    conn.commit()
    conn.close()
    
main()