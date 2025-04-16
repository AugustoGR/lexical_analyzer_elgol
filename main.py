import sys
import re
from tabulate import tabulate

# para rodar basta executar o arquivo main.py passando o arquivo de entrada como argumento
# python main.py <arquivo_de_entrada>
if sys.argv[1]:
    file = open(sys.argv[1], 'r')
else:
    file = open('code.txt', 'r')



reservedWords: list[str] = ['int', 'float', 'double', 'char', 'if', 'while', 'for']

tableSymbols: list[tuple[str, str, str]] = []

tokensList: list[str] = []

def register_token(token, tipo):
    newEntrada = len(tableSymbols) + 1
    tableSymbols.append((newEntrada, token, tipo))
    tokensList.append(f'<{tipo},{newEntrada}>')

for line in file:
    line = line.strip()

    if len(line) == 0 or re.match(r'^#', line):
        continue
    tokens =  re.findall(r'[0-9]+,?[0-9]+|[a-zA-Z_]\w*|[()\[\]{}]|==|!=|<=|>=|[+\-*/=<>]', line)
    
    for token in tokens:

        #region VERIFICAR SE O TOKEN TEM #
        if re.match(r'^#', token):
            break
        #endregion VERIFICAR SE O TOKEN TEM #

        #region VERIFICAR SE O TOKEN JÁ ESTÁ NA TABELA DE SÍMBOLOS. SE ESTIVER, ADICIONAR NA LISTA DE TOKENS
        matched = False
        for symbol in tableSymbols:
            if token == symbol[1]:
                tokensList.append(f'<{symbol[2]},{symbol[0]}>')
                matched = True
                break
        if matched:
            continue
        #endregion VERIFICAR SE O TOKEN JÁ ESTÁ NA TABELA DE SÍMBOLOS. SE ESTIVER, ADICIONAR NA LISTA DE TOKENS

        #region VERIFICAR SE O TOKEN É UM IDENTIFICADOR
        if re.match(r'^[A-Z][a-zA-Z]*$', token):
            register_token(token, 'identificador')
        #endregion VERIFICAR SE O TOKEN É UM IDENTIFICADOR

        #region VERIFICAR SE O TOKEN É UMA PALAVRA RESERVADA
        elif re.match(r'^[a-z][a-zA-Z]*$', token):

            if token in reservedWords:
                register_token(token, 'reservada')
        #endregion VERIFICAR SE O TOKEN É UMA PALAVRA RESERVADA

        #region VERIFICAR SE O TOKEN É UM NÚMERO
        elif re.match(r'^[0-9]+,?[0-9]+$', token):
            register_token(token, 'número')
        #endregion VERIFICAR SE O TOKEN É UM NÚMERO

        #region VERIFICAR SE O TOKEN É UM OPERADOR OU PONTUAÇÃO
        elif re.match(r'^[\(\);+\-%\*\[\]=.<>]$', token):
            tokensList.append(f'<{token},>')
        #endregion VERIFICAR SE O TOKEN É UM OPERADOR OU PONTUAÇÃO

print('.:TABELA DE SÍMBOLOS:.')
print(tabulate(tableSymbols, headers=["ID", "Token", "Tipo"], tablefmt="grid"))
print('\n.:LISTA DE TOKENS:.')
for token in tokensList:
    print(token)

with open('tokens_output.txt', 'w') as output_file:
    output_file.write(' '.join(tokensList))

