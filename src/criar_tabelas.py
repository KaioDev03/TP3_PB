import sqlite3
'''Importamos a bilbioteca sqlite3 para a criação de tabelas e logo após de estruturar os arquivos conectamos o banco de dados ao seu diretório e ao abrir conexão com o banco de dados adicionamos as tabelas necessárias. Além das tabelas já interligamos as tabelas com as suas respectivas chaves primárias e estrangeiras.'''
con = sqlite3.connect('../db/empresa.db') #Conectando o banco de dados ao diretório correto e para armazenar dados.
cursor = con.cursor()
'''Criação de todas as tabelas e dados necessários para o trabalho. Tabelas(funcionarios, cargos, departamentos, historico de salários, dependentes.) '''
'''Tabela Funcionarios.'''
cursor.execute('''
    CREATE TABLE funcionarios (
        id integer PRIMARY KEY AUTOINCREMENT,
        nome text not null,
        idade integer,
        cargo_id,
        departamento_id integer,
        FOREIGN KEY (cargo_id) REFERENCES cargos(id),
        FOREIGN KEY (departamentos_id) REFERENCES departamentos(id)
    )
''')
'''Tabela Cargos.'''
cursor.execute('''
    CREATE TABLE cargos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nivel TEXT NOT NULL
    )
''')
'''Tabela Departamentos.'''
cursor.execute('''
    CREATE TABLE departamentos
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    horario_funcionamento TEXT NOT NULL
    )
''')
'''Tabela Histórico de Funcionários.'''
cursor.execute('''
    CREATE TABLE historico_salarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionario_id INTEGER,
    data_aumento TEXT NOT NULL,
    salario_anterior TEXT NOT NULL,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
    )
''')
'''Tabela de Dependentes.'''
cursor.execute('''
    CREATE TABLE dependentes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        funcionario_id INTEGER,
        nome TEXT NOT NULL,
        idade INTEGER,
        parentesco TEXT NOT NULL,
        FOREIGN KEY (funcionario_id) REFERENCES funcionario(id)           
)
''')
'''Fechamento da conexão do banco de dados.'''
con.commit()
con.close()

print("Tabela Criada com sucesso.")