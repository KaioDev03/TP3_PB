import sqlite3
import csv
'''Importação das bibliotecas e cada função faz a abertura do arquivo.csv específico para adicionar seus valores.'''
def inserir_departamentos(cursor):
    with open('departamentos.csv', mode = 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            cursor.execute('''
            INSERT INTO departamentos(nome,horario_funcionamento)
            VALUES (?, ?)''', (row['nome'], row['horario_funcionamento']))
'''Inserção dos dados da tabela funcionário.'''          
def inserir_funcionarios(cursor):
    with open('funcionarios.csv', mode = 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            cursor.execute('''
            INSERT INTO funcionarios(nome, idade, cargo_id, nome_departamento, data_contratacao)
            VALUES (?, ?, ?, ?, ?)''', (row['nome'], int(row['idade']), int(row['cargo_id']), row['nome_departamento'], row['data_contratacao']))
'''Inserção dos dados da tabela dependentes.'''            
def inserir_dependentes(cursor):
    with open('dependentes.csv', mode = 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            cursor.execute('''
            INSERT INTO dependentes(funcionario_id, nome, idade, parentesco)
            VALUES (?, ?, ?, ?)''', (int(row['funcionario_id']), row['nome'], int(row['idade']), row['parentesco']))
'''Inserção dos dados da tabela cargos'''            
def inserir_cargos(cursor):
    with open('cargos.csv', mode = 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            cursor.execute('''
            INSERT INTO cargos(nome,salario)
            VALUES (?, ?)''', (row['nome'], row['salario']))
            
def main():
    '''Função principal para gerenciar a inserção de dados no banco de dados da empresa
    
    Esta função estabelece uma conexão com o banco de dados da empresa e insere os dados chamando a função específica, após isso realiza o commit das alterações e fecha a conexão com o banco de dados'''
    
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    
    '''Inserção dos dados'''
    
    inserir_departamentos(cursor)
    inserir_dependentes(cursor)
    inserir_funcionarios(cursor)
    inserir_cargos(cursor)
    
    conn.commit()
    conn.close()