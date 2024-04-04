#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 13:08:04 2024

@author: hpc
"""

# Recalculando a frequência do texto cifrado e as similaridades, já que o estado do código foi reiniciado

# Função para calcular a frequência de cada letra no texto

caminho_do_arquivo = "./20201-teste2.txt"

def ler_texto_cifrado(caminho_do_arquivo):
    with open(caminho_do_arquivo, 'r') as arquivo:
        return arquivo.read()


def calcular_frequencia(texto):
    texto = texto.replace(" ", "").upper()
    frequencia = {}
    for letra in texto:
        if letra.isalpha():
            frequencia[letra] = frequencia.get(letra, 0) + 1
    total_letras = sum(frequencia.values())
    for letra in frequencia:
        frequencia[letra] = (frequencia[letra] / total_letras) * 100
    return frequencia

# Frequências médias das letras em inglês e português
frequencias_ingles = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3}
frequencias_portugues = {'A': 14.6, 'E': 12.4, 'O': 10.7, 'S': 7.8, 'R': 6.5, 'I': 6.2, 'N': 5.0, 'D': 4.9, 'M': 4.7, 'U': 4.6}

# Função para calcular a similaridade entre as frequências do texto cifrado e as frequências de uma língua
def calcular_similaridade(frequencias_texto, frequencias_lingua):
    similaridade = 0
    for letra, freq in frequencias_texto.items():
        if letra in frequencias_lingua:
            similaridade += min(freq, frequencias_lingua[letra])
    return similaridade

# Exemplo de uso da função

texto_cifrado = ler_texto_cifrado(caminho_do_arquivo).upper()
frequencia = calcular_frequencia(texto_cifrado)

# Calculando a similaridade com inglês e português
similaridade_ingles = calcular_similaridade(frequencia, frequencias_ingles)
similaridade_portugues = calcular_similaridade(frequencia, frequencias_portugues)




print( similaridade_ingles, similaridade_portugues)

