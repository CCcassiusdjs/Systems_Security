from pycipher import Vigenere
import re
from collections import defaultdict, Counter
import itertools
import string
from math import gcd
from tqdm import tqdm


# Parte 1: Leitura do Texto Cifrado
def ler_texto_cifrado(caminho_do_arquivo):
    with open(caminho_do_arquivo, 'r') as arquivo:
        return arquivo.read()


def indice_de_coincidencia(segmento):
    n = len(segmento)
    freqs = Counter(segmento)
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
    return ic


def encontrar_tamanho_chave_ic(texto_cifrado, idioma='ingles'):
    IC_ESPERADO = 0.065  # Valor típico para inglês
    tamanho_max_chave = 20  # Um limite razoável para o tamanho da chave
    melhor_tamanho = 1
    melhor_diferenca = float('inf')

    for tamanho in range(1, tamanho_max_chave + 1):
        segmentos = [''.join(texto_cifrado[i::tamanho]) for i in range(tamanho)]
        ic_medio = sum(indice_de_coincidencia(segmento) for segmento in segmentos) / tamanho
        diferenca = abs(IC_ESPERADO - ic_medio)

        if diferenca < melhor_diferenca:
            melhor_diferenca = diferenca
            melhor_tamanho = tamanho

    return melhor_tamanho


# Parte 4: Tabelas de Frequência de Letras
frequencia_portugues = {
    'a': 14.63,
    'b': 1.04,
    'c': 3.88,
    'd': 4.99,
    'e': 12.57,
    'f': 1.02,
    'g': 1.30,
    'h': 1.28,
    'i': 6.18,
    'j': 0.40,
    'k': 0.02,
    'l': 2.78,
    'm': 4.74,
    'n': 5.05,
    'o': 10.73,
    'p': 2.52,
    'q': 1.20,
    'r': 6.53,
    's': 7.81,
    't': 4.34,
    'u': 4.63,
    'v': 1.67,
    'w': 0.01,
    'x': 0.21,
    'y': 0.01,
    'z': 0.47
}

frequencia_ingles = {
    'a': 8.167,
    'b': 1.492,
    'c': 2.782,
    'd': 4.253,
    'e': 12.702,
    'f': 2.228,
    'g': 2.015,
    'h': 6.094,
    'i': 6.966,
    'j': 0.153,
    'k': 0.772,
    'l': 4.025,
    'm': 2.406,
    'n': 6.749,
    'o': 7.507,
    'p': 1.929,
    'q': 0.095,
    'r': 5.987,
    's': 6.327,
    't': 9.056,
    'u': 2.758,
    'v': 0.978,
    'w': 2.360,
    'x': 0.150,
    'y': 1.974,
    'z': 0.074
}


# Implementação para calcular a chave mais provável
def calcular_chave_otimizada(texto_cifrado, tamanho_chave, frequencia_idioma):
    chave_otimizada = ''
    for i in tqdm(range(tamanho_chave), desc="Calculando chave otimizada"):  # Adicionando a barra de progresso aqui
        segmento = texto_cifrado[i::tamanho_chave]
        contador = Counter(segmento)
        letra_mais_frequente = max(contador, key=contador.get)
        deslocamento = ord(letra_mais_frequente) - ord('e')  # 'e' é geralmente a letra mais frequente
        chave_otimizada += chr((deslocamento + 26) % 26 + ord('a'))
    return chave_otimizada


# Implementação para determinar o idioma

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


# Função para decifrar o texto usando a Cifra de Vigenère
def decifrar_com_vigenere(texto_cifrado, chave):
    vigenere = Vigenere(chave)
    return vigenere.decipher(texto_cifrado)



def determinar_idioma(texto_cifrado):

    frequencia = calcular_frequencia(texto_cifrado)
    
    # Calculando a similaridade com inglês e português
    similaridade_ingles = calcular_similaridade(frequencia, frequencias_ingles)
    similaridade_portugues = calcular_similaridade(frequencia, frequencias_portugues)
    return "portugues" if similaridade_portugues > similaridade_ingles else "ingles"

# Função principal do programa
def decifrar_texto(caminho_do_arquivo):
    print("Lendo o texto cifrado...")
    texto_cifrado = ler_texto_cifrado(caminho_do_arquivo).lower()

    print("Determinando o idioma...")
    idioma = determinar_idioma(texto_cifrado)
    frequencia_idioma = frequencia_portugues if idioma == "portugues" else frequencia_ingles

    print("Encontrando o tamanho da chave usando o Índice de Coincidência...")
    tamanho_chave = encontrar_tamanho_chave_ic(texto_cifrado, idioma)

    print("Calculando a chave otimizada...")
    chave = calcular_chave_otimizada(texto_cifrado, tamanho_chave, frequencia_idioma)

    print("Decifrando o texto...")
    texto_decifrado = decifrar_com_vigenere(texto_cifrado, chave)

    return texto_decifrado, idioma


# Executar o programa
caminho_do_arquivo = "./20201-teste2.txt"
resultado = decifrar_texto(caminho_do_arquivo)
print("Texto Decifrado:", resultado)
