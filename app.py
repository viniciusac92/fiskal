from fiskal import Fiskal
import csv


# arquivo de entrada de dados
csv_file_path = 'entrada_de_dados.csv'

# lista que armazena os dados da planilha
planilha_entrada_dados = []

# abre o arquivo apenas no modo leitura
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # fazendo a iteração sobre o arquivo csv na primeira coluna
    planilha_entrada_dados = [row[0] for row in csv_reader]

# preparação de dados como JSON
# OBS: nomes das chaves são os labels
dados = {
    "Address": planilha_entrada_dados[0],
    "Phone Number": planilha_entrada_dados[1],
    "Company Name": planilha_entrada_dados[2],
    "Email": planilha_entrada_dados[3],
    "Last Name": planilha_entrada_dados[4],
    "Role in Company": planilha_entrada_dados[5],
    "First Name": planilha_entrada_dados[6]
}

# instancia a classe do robô
robo = Fiskal(dados)

# coloca o script em execução
robo.run()
