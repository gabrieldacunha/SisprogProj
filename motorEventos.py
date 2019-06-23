# -*- coding: utf-8 -*-
import pandas as pd
from tabulate import tabulate
import numpy as np


memoria = []
PC = 0
AC = 0 #Acumulador inicializado em 0


def loader():
    print('Loading...')
    print(' ')
    arquivo = open("loader.txt", 'r') #carrega o arquivo loader em modo de leitura
    cifrao = arquivo.readline() #lê linha de $
    start = arquivo.readline() #lê a primeira linha, correspondente à rotina START
    linha = arquivo.readline() #lê a primeira linha, correspondente ao mnemônico Read File
    i = 0 #variável auxiliar de contagem do vetor de memória
    linha = arquivo.readline() #lê uma linha
    while (linha != "DATA"):
        if (linha[2:4] == "COUNT"):
            memoria[i] = 31
        elif (linha[2:4] == "DATA"):
            memoria[i] = 15
        else:
            memoria[i] = linha[:2]
            memoria[i+1] = linha[2:4]
        linha = arquivo.readline() #lê uma linha
    linha = arquivo.readline() #lê uma linha
    while (linha != "EXE"):
        if (linha[2:4] == "COUNT"):
            memoria[i] = 31
        elif (linha[2:4] == "EXE"):
            memoria[i] = 36
        else:
            memoria[i] = linha[:2]
            memoria[i+1] = linha[2:4]
        linha = arquivo.readline() #lê uma linha
    linha = arquivo.readline() #lê uma linha
    while (linha != "CEM"):
        if (linha[2:4] == "START"):
            memoria[i] = 0
        else:
            memoria[i] = linha[:2]
            memoria[i+1] = linha[2:4]
        linha = arquivo.readline() #lê uma linha
    

def montador_passo2(arquivo, area):
    file = open(arquivo, 'r')
    arquivo_assembly = open(arquivo, 'w')
    linha = file.readline() #le uma linha
    #consulta na tabela de instruções se é pseudo
    i = 0
    while (file.readline()):
        instr = linha[:2]
        #motor de eventos
        if (instr == 'JA'): #JA
            PC = PC + 4
            memoria[i] = '06'
        elif (instr == 'BN'): #BN
            PC = PC + 4
            memoria[i] = '04'
        elif (instr == '+'): #+
            PC = PC + 4
            memoria[i] = '09'
        elif (instr == '0*'): #*
            PC = PC + 4
            memoria[i] = '0B'
        elif (instr == 'LA'): #LA
            PC = PC + 4
            memoria[i] = '00'
        elif (instr == 'SR'): #SR
            PC = PC + 4
            memoria[i] = '05'
        elif (instr == 'OF'): #OF
            PC = PC + 4
            memoria[i] = '0F'
        elif (instr == 'DC'): #DC
            PC = PC + 4
            memoria[i] = '05'
        elif (instr == 'BZ'): #BZ
            PC = PC + 4
            memoria[i] = '03'
        elif (instr == 'SD'): #SD
            PC = PC + 4
            memoria[i] = '02'
        elif (instr == '-'): # -
            PC = PC + 4
            memoria[i] = '0A'
        elif (instr == '/'): # /
            PC = PC + 4
            memoria[i] = '0C'
        elif (instr=='SA'): # SA
            PC = PC + 4
            memoria[i] = '01'
        elif (instr == 'RT'): # RT
            PC = PC + 4
            memoria[i] = '08'
        elif (instr == 'RF'): #RF
            PC = PC + 4
            memoria[i] = '0D'
        elif (instr == 'ON'): # ON
            PC = PC + 4
            memoria[i] = '0E'
        elif (linha[:1] == 'K'):
            PC = PC + 2
        else:
            PC = PC + 2
    file.close()
    arquivo_assembly.close()
    return arquivo_assembly

def montador_passo1(arquivo):
    area = 0
    file = open(arquivo, 'r')
    linha = file.readline() #le uma linha
    pseudo = False
    simbols_df = pd.DataFrame([])
    labels_df = pd.DataFrame([])

    if(linha[0] != ' '):
        if (linha.find(':')!=-1): #existe o simbolo : na linha, entao há rotulo
            #checar se ja ta na tabela de simbolos -> erro
            #incluir na tabela de simbolos
            df['simbolo'] = [linha[:":"]]
            df['valor'] = [linha[":":" "]]
            df['endereco'] = [PC]
            PC = PC + 2
        else:
            PC = PC + 2
            df['simbolo'] = [linha[:":"]]
            df['valor'] = [linha[":":" "]]
            df['endereco'] = [PC]
    else:
        tamanho = linha.split(2)
        area = area + tamanho
        PC = PC + tamanho
    #fim do arquivo
    arquivo_assembly = montador_passo2(arquivo, area)
    return arquivo_assembly


def executar(arquivo):
    #Inicialização de variáveis
    op = None
    parada = False
    while (not parada):
        file = open(arquivo, 'r')
        linha = file.readline()
        instr = linha[:2]
        #motor de eventos
        if (instr == '06'): #JA
            PC = op
        elif (instr == '04'): #BN
            if (AC<0):
                PC = op
            else:
                PC = PC + 2
        elif (instr == '09'): #+
            AC = AC + memoria[op]
            PC = PC + 2
        elif (instr == '0B'): #*
            AC = AC * memoria[op]
            PC = PC + 2
        elif (instr == '00'): #LA
            AC = memoria[op]
            PC = PC + 2
        elif (instr == '05'): #SR
            PC = op + 2
        elif (instr == '0F'): #OF
            #PARAR, QUANDO FOR DADA A PARTIDA continua
            wait = input('')
            PC = op
        elif (instr == '05'): #DC
            #saida do conteudo do AC
            if (op == 0):
                PC = AC
            elif (op == 1):
                PC = PC + 2
            elif (op == 2):
                print (AC)
            elif (op == 3):
                print (AC)
        elif (instr == '03'): #BZ
            if (AC == 0):
                PC = op
            else:
                PC = PC + 2
        elif (instr == '02'): #SD
            AC = op
            PC = PC + 2
        elif (instr == '0A'): # -
            AC = AC - memoria[op]
            PC = PC + 2
        elif (instr == '0C'): # /
            AC = AC / memoria[op]
            PC = PC + 2
        elif (instr=='01'): # SA
            memoria[op] = AC
            PC = PC + 2
        elif (instr == '08'): # RT
            PC = op
        elif (instr == '0D'): #RF
            AC = input('')
            PC = PC + 2
        elif (instr == '0E'): # ON
            #system call
            exit(1)
        else:
            print('Erro na leitura do arquivo')


def main():
    print('')
    print('PCS3216 - Sistemas de Programação')
    print('')
    print('Projeto: Motor de eventos')
    print('')
    
    print('Programas disponíveis:')

    comandos = pd.read_csv('programas.csv')
    print(tabulate(comandos, headers='keys', tablefmt='psql'))
    arquivo = input('Digite o programa a ser simulado:')
    loader()
    arquivo_assembly = montador_passo1(arquivo)
    executar(arquivo_assembly)
    


main()
