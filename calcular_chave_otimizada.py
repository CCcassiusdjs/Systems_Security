#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:53:32 2024

@author: hpc
"""
from collections import Counter


def calcular_chave_otimizada(texto_cifrado, tamanho_chave, letra_mais_frequente_idioma):
    chave_otimizada = ''
    for i in range(tamanho_chave):
        # Extrai o segmento do texto que corresponde à mesma posição da chave
        segmento = texto_cifrado[i::tamanho_chave]

        # Conta a frequência das letras no segmento
        contador = Counter(segmento)

        # Encontra a letra mais frequente no segmento
        letra_mais_frequente = max(contador, key=contador.get)

        # Calcula o deslocamento da letra mais frequente até a letra mais frequente do idioma
        deslocamento = ord(letra_mais_frequente) - ord(letra_mais_frequente_idioma)

        # Corrige o deslocamento e adiciona à chave
        chave_otimizada += chr((deslocamento + 26) % 26 + ord('a'))
    return chave_otimizada