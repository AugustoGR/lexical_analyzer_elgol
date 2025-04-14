import sys
import re

# para rodar basta executar o arquivo main.py passando o arquivo de entrada como argumento
# python main.py <arquivo_de_entrada>
file = open(sys.argv[1], 'r')

symbols = [
    ('int', 'reservada'),
    ('float', 'reservada'),
    ('double', 'reservada'),
    ('char', 'reservada'),
    ('if', 'reservada'),
    ('while', 'reservada'),
    ('for', 'reservada'),
]

tokensList = []

for line in file:
    line = line.strip()

    if len(line) == 0 or line.startswith('#'):
        continue
    tokens = re.split(r'\s+', line)
    
    for token in tokens:
        if re.match(r'^[A-Z][a-zA-Z]*$', token):
            symbols.append((token, 'identificador'))
            tokensList.append(('identificador', len(symbols) - 1))
        elif re.match(r'^[a-z][a-zA-Z]*$', token):
            if token in [symbol[0] for symbol in symbols]:
                idx = symbols.index((token, 'reservada'))
                tokensList.append(('reservada', idx))
        elif re.match(r'^[0-9]+,?[0-9]+$', token):
            symbols.append((token, 'numero'))
            tokensList.append(('numero', len(symbols) - 1))
        elif re.match(r'^[\(\);+\-%\*\[\]=.<>]$', token):
            tokensList.append((token, '-'))

print('Tokens:', tokensList)

print('Simbolos:', symbols)


# Ainda é preciso ajusta a leitura de pontuação colados ao texto "int a = 0;"
# vericar se todos os tokens estão sendo lidos corretamente
# Ter como saida um arquivo com a lista de tokens e uma tabela com os simbolos
