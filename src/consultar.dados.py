import sqlite3

# Conectar ao banco de dados
con = sqlite3.connect('./db/empresa.db', timeout = 1000)
cursor = con.cursor()

# 1. Listar individualmente as tabelas de: Funcionários, Cargos, Departamentos, Histórico de Salários e Dependentes em ordem crescente.
# Funcionários
cursor.execute('SELECT * FROM funcionarios ORDER BY nome;')
funcionarios = cursor.fetchall()

# Cargos
cursor.execute('SELECT * FROM cargos ORDER BY nome;')
cargos = cursor.fetchall()

# Departamentos
cursor.execute('SELECT * FROM departamentos ORDER BY nome;')
departamentos = cursor.fetchall()

# Histórico de Salários
cursor.execute('SELECT * FROM historico_salarios ORDER BY data_aumento;')
historico_salarios = cursor.fetchall()

# Dependentes
cursor.execute('SELECT * FROM dependentes ORDER BY nome;')
dependentes = cursor.fetchall()

# 2. Listar os funcionários, com seus cargos, departamentos e os respectivos dependentes.
cursor.execute('''
    SELECT f.nome AS funcionario, c.nome AS cargo, d.nome AS departamento, dep.nome AS dependente
    FROM funcionarios f
    JOIN cargos c ON f.cargo_id = c.id
    JOIN departamentos d ON f.nome_departamento = d.nome
    LEFT JOIN dependentes dep ON f.id = dep.funcionario_id
    ORDER BY f.nome;
''')
funcionarios_info = cursor.fetchall()

# 3. Listar os funcionários que tiveram aumento salarial nos últimos 3 meses.
cursor.execute('''
    SELECT f.nome
    FROM funcionarios f
    JOIN historico_salarios hs ON f.id = hs.funcionario_id
    WHERE hs.data_aumento >= DATE('now', '-3 months')
    ORDER BY hs.data_aumento DESC;
''')
funcionarios_aumento = cursor.fetchall()

# 4. Listar a média de idade dos filhos dos funcionários por departamento.
cursor.execute('''
    SELECT f.nome_departamento, AVG(d.idade) AS media_idade_filhos
    FROM dependentes d
    JOIN funcionarios f ON d.funcionario_id = f.id
    GROUP BY f.nome_departamento;
''')
media_idade_filhos = cursor.fetchall()

# 5. Listar qual estagiário possui filho.
cursor.execute('''
    SELECT f.nome
    FROM funcionarios f
    JOIN dependentes d ON f.id = d.funcionario_id
    WHERE f.cargo_id = (SELECT id FROM cargos WHERE nome = 'Estagiário')
    GROUP BY f.nome;
''')
estagiario_com_filho = cursor.fetchall()

# 6. Listar o funcionário que teve o salário médio mais alto.
cursor.execute('''
    SELECT f.nome, AVG(hs.salario_atual) AS salario_medio
    FROM funcionarios f
    JOIN historico_salarios hs ON f.id = hs.funcionario_id
    GROUP BY f.id
    ORDER BY salario_medio DESC
    LIMIT 1;
''')
funcionario_salario_medio_alto = cursor.fetchone()

# 7. Listar o analista que é pai de 2 (duas) meninas.
cursor.execute('''
    SELECT f.nome
    FROM funcionarios f
    JOIN dependentes d ON f.id = d.funcionario_id
    WHERE f.cargo_id = (SELECT id FROM cargos WHERE nome = 'Analista')
    AND d.genero = 'Feminino'
    GROUP BY f.id
    HAVING COUNT(d.id) = 2;
''')
analista_pai_duas_meninas = cursor.fetchall()

# 8. Listar o analista que tem o salário mais alto, e que ganhe entre 5000 e 9000.
cursor.execute('''
    SELECT f.nome, hs.salario_atual
    FROM funcionarios f
    JOIN historico_salarios hs ON f.id = hs.funcionario_id
    WHERE f.cargo_id = (SELECT id FROM cargos WHERE nome = 'Analista')
    AND hs.salario_atual BETWEEN 5000 AND 9000
    ORDER BY hs.salario_atual DESC
    LIMIT 1;
''')
analista_salario_entre_5000_9000 = cursor.fetchone()

# 9. Listar qual departamento possui o maior número de dependentes.
cursor.execute('''
    SELECT f.nome_departamento, COUNT(d.id) AS numero_dependentes
    FROM dependentes d
    JOIN funcionarios f ON d.funcionario_id = f.id
    GROUP BY f.nome_departamento
    ORDER BY numero_dependentes DESC
    LIMIT 1;
''')
departamento_maior_numero_dependentes = cursor.fetchone()

# 10. Listar a média de salário por departamento em ordem decrescente.
cursor.execute('''
    SELECT f.nome_departamento, AVG(hs.salario_atual) AS media_salario
    FROM funcionarios f
    JOIN historico_salarios hs ON f.id = hs.funcionario_id
    GROUP BY f.nome_departamento
    ORDER BY media_salario DESC;
''')
media_salario_por_departamento = cursor.fetchall()

# Fechar a conexão
con.close()

# Exibindo os resultados
print("\nFuncionários:", funcionarios)
print("\nCargos:", cargos)
print("\nDepartamentos:", departamentos)
print("\nHistórico de Salários:", historico_salarios)
print("\nDependentes:", dependentes)
print("-----------------------------------")
print("\nFuncionários com aumento salarial nos últimos 3 meses:", funcionarios_aumento)
print("-----------------------------------")
print("\nMédia de idade dos filhos por departamento:", media_idade_filhos)
print("-----------------------------------")
print("\nEstagiários com filhos:", estagiario_com_filho)
print("-----------------------------------")
print("\nFuncionário com o salário médio mais alto:", funcionario_salario_medio_alto)
print("-----------------------------------")
print("\nAnalista que é pai de 2 meninas:", analista_pai_duas_meninas)
print("-----------------------------------")
print("\nAnalista com salário entre 5000 e 9000:", analista_salario_entre_5000_9000)
print("-----------------------------------")
print("\nDepartamento com o maior número de dependentes:", departamento_maior_numero_dependentes)
print("-----------------------------------")
print("\nMédia de salário por departamento:", media_salario_por_departamento)