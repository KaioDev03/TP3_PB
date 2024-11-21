import sqlite3
'''Importamos a bilbioteca sqlite3 para a criação de tabelas e logo após de estruturar os arquivos conectamos o banco de dados ao seu diretório e ao abrir conexão com o banco de dados adicionamos as tabelas necessárias. Além das tabelas já interligamos as tabelas com as suas respectivas chaves primárias e estrangeiras.'''
con = sqlite3.connect('./db/empresa.db') #Conectando o banco de dados ao diretório correto e para armazenar dados.
cursor = con.cursor()
'''Criação de todas as tabelas e dados necessários para o trabalho. Tabelas(funcionarios, cargos, departamentos, historico de salários, dependentes.) '''
'''Tabela Funcionarios.'''
cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        cargo_id INTEGER,
        nome_departamento TEXT NOT NULL,
        FOREIGN KEY (cargo_id) REFERENCES cargos(id)
    )
''')
'''Tabela Cargos.'''
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cargos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nivel TEXT NOT NULL
    )
''')
'''Tabela Departamentos.'''
cursor.execute('''
    CREATE TABLE IF NOT EXISTS departamentos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    horario_funcionamento TEXT NOT NULL
    )
''')
'''Tabela Histórico de Historico salários.'''
cursor.execute('''
    CREATE TABLE IF NOT EXISTS historico_salarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionario_id INTEGER,
    data_aumento TEXT,
    salario_anterior FLOAT,
    salario_atual FLOAT,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
    )
''')
'''Tabela de Dependentes.'''
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dependentes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        funcionario_id INTEGER,
        nome TEXT NOT NULL,
        idade INTEGER,
        parentesco TEXT NOT NULL,
        genero TEXT NOT NULL,
        FOREIGN KEY (funcionario_id) REFERENCES funcionario(id)           
)
''')
'''Tabela de Projetos'''
cursor.execute('''
   CREATE TABLE IF NOT EXISTS projetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_projeto TEXT NOT NULL,
    descricao TEXT,
    data_inicio TEXT NOT NULL,
    data_conclusao TEXT,
    funcionario_responsavel_id INTEGER,
    custo FLOAT,
    status TEXT CHECK(status IN ('Em Planejamento', 'Em Execução', 'Concluído', 'Cancelado')) NOT NULL,
    FOREIGN KEY (funcionario_responsavel_id) REFERENCES funcionarios(id)
);
''')
'''Tabela de Recursos do Projeto'''
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recursos_do_projeto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    projeto_id INTEGER,
    descricao TEXT NOT NULL,
    tipo_recurso TEXT CHECK(tipo_recurso IN ('financeiro', 'material', 'humano')) NOT NULL,
    quantidade_utilizada FLOAT,
    data_utilizacao TEXT NOT NULL,
    FOREIGN KEY (projeto_id) REFERENCES projetos(id)
);
''')
'''Fechamento da conexão do banco de dados.'''
con.commit()
con.close()

print("Tabelas Criadas com sucesso.")