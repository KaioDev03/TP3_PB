import sqlite3
import json
import csv

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

print("---------------------------------------------")
print("Novas consultas: ")
print("Média dos salários dos funcionários responsáveis por projetos concluídos, agrupados por departamento:")
con = sqlite3.connect('./db/empresa.db', timeout = 1000)
cursor = con.cursor()
cursor.execute('''
    SELECT d.nome AS departamento, AVG(h.salario_atual) AS media_salario
    FROM projetos p
    JOIN funcionarios f ON p.funcionario_responsavel_id = f.id
    JOIN departamentos d ON f.nome_departamento = d.nome
    JOIN historico_salarios h ON f.id = h.funcionario_id
    WHERE p.status = 'Concluído'
    AND h.id IN (SELECT MAX(id) FROM historico_salarios WHERE funcionario_id = f.id)
    GROUP BY d.nome
''')
resultado = cursor.fetchall()
for row in resultado:
    print(row)

print("Identificar os três recursos materiais mais usados nos projetos, listando a descrição do recurso e a quantidade total usada:\n")   
cursor.execute('''
    SELECT r.descricao, SUM(r.quantidade_utilizada) AS total_quantidade
    FROM recursos_do_projeto r
    WHERE r.tipo_recurso = 'material'
    GROUP BY r.descricao
    ORDER BY total_quantidade DESC
    LIMIT 3
''')
resultado = cursor.fetchall()
for row in resultado:
    print(row)

print("Calcular o custo total dos projetos por departamento, considerando apenas os projetos 'Concluídos':\n")
cursor.execute('''
    SELECT d.nome AS departamento, SUM(p.custo) AS custo_total
    FROM projetos p
    JOIN funcionarios f ON p.funcionario_responsavel_id = f.id
    JOIN departamentos d ON f.nome_departamento = d.nome
    WHERE p.status = 'Concluído'
    GROUP BY d.nome
''')
resultado = cursor.fetchall()
for row in resultado:
    print(row)

print("Listar todos os projetos com seus respectivos nomes, custo, data de início, data de conclusão e o nome do funcionário responsável, que estejam 'Em Execução': \n")
cursor.execute('''
    SELECT p.nome_projeto, p.custo, p.data_inicio, p.data_conclusao, f.nome
    FROM projetos p
    JOIN funcionarios f ON p.funcionario_responsavel_id = f.id
    WHERE p.status = 'Em Execução'
''')
resultado = cursor.fetchall()
for row in resultado:
    print(row)

print("Identificar o projeto com o maior número de dependentes envolvidos, considerando que os dependentes são associados aos funcionários que estão gerenciando os projetos: \n")
cursor.execute('''
    SELECT p.id, p.nome_projeto, COUNT(d.id) AS num_dependentes
    FROM projetos p
    JOIN funcionarios f ON p.funcionario_responsavel_id = f.id
    JOIN dependentes d ON f.id = d.funcionario_id
    GROUP BY p.id
    ORDER BY num_dependentes DESC
    LIMIT 1
''')
resultado = cursor.fetchall()
for row in resultado:
    print(row)

con.close()

conn = sqlite3.connect('./db/empresa.db')
cursor = conn.cursor()

print("Consulta escolhida 1: Média dos salários dos funcionários responsáveis por projetos concluídos, agrupados por departamento")
cursor.execute('''
    SELECT d.nome AS departamento, AVG(h.salario_atual) AS media_salario
    FROM projetos p
    JOIN funcionarios f ON p.funcionario_responsavel_id = f.id
    JOIN departamentos d ON f.nome_departamento = d.nome
    JOIN historico_salarios h ON f.id = h.funcionario_id
    WHERE p.status = 'Concluído'
    AND h.id IN (SELECT MAX(id) FROM historico_salarios WHERE funcionario_id = f.id)
    GROUP BY d.nome
''')
consulta1_resultado = cursor.fetchall()

print("Consulta escolhida 2: Três recursos materiais mais usados nos projetos")
cursor.execute('''
    SELECT r.descricao, SUM(r.quantidade_utilizada) AS total_quantidade
    FROM recursos_do_projeto r
    WHERE r.tipo_recurso = 'material'
    GROUP BY r.descricao
    ORDER BY total_quantidade DESC
    LIMIT 3
''')
consulta2_resultado = cursor.fetchall()

print("Consulta escolhida 3: Custo total dos projetos por departamento, considerando projetos concluídos")
cursor.execute('''
    SELECT d.nome AS departamento, SUM(p.custo) AS custo_total
    FROM projetos p
    JOIN funcionarios f ON p.funcionario_responsavel_id = f.id
    JOIN departamentos d ON f.nome_departamento = d.nome
    WHERE p.status = 'Concluído'
    GROUP BY d.nome
''')
consulta3_resultado = cursor.fetchall()

# Fechando a conexão
conn.close()

def converter_para_json(resultados, campos):
    dados_json = []
    for linha in resultados:
        item = dict(zip(campos, linha))
        dados_json.append(item)
    return json.dumps(dados_json, indent=4)

campos_consulta1 = ['departamento', 'media_salario']
campos_consulta2 = ['descricao', 'total_utilizado']
campos_consulta3 = ['departamento', 'custo_total']

# Conversão dos arquivos em JSON
json_consulta1 = converter_para_json(consulta1_resultado, campos_consulta1)
json_consulta2 = converter_para_json(consulta2_resultado, campos_consulta2)
json_consulta3 = converter_para_json(consulta3_resultado, campos_consulta3)

with open('consulta1_resultados.json', 'w') as f:
    f.write(json_consulta1)

with open('consulta2_resultados.json', 'w') as f:
    f.write(json_consulta2)

with open('consulta3_resultados.json', 'w') as f:
    f.write(json_consulta3)

print("Arquivos JSON gerados com sucesso!")

#Conversão dos arquivos jsons em CSV para leitura no Loocker studio.
def converter_para_csv(resultados, campos, nome_arquivo):
    with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(campos)  # Escrever o cabeçalho
        escritor.writerows(resultados)  # Escrever as linhas

# Convertendo os resultados para CSV
converter_para_csv(consulta1_resultado, campos_consulta1, 'consulta1_resultados.csv')
converter_para_csv(consulta2_resultado, campos_consulta2, 'consulta2_resultados.csv')
converter_para_csv(consulta3_resultado, campos_consulta3, 'consulta3_resultados.csv')