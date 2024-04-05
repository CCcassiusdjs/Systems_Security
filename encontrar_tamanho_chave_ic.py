#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:43:18 2024

@author: hpc
"""
from collections import Counter

def indice_de_coincidencia(segmento):
    n = len(segmento)
    freqs = Counter(segmento)
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
    return ic



def encontrar_tamanho_chave_ic(texto_cifrado, IC_ESPERADO):
    tamanho_max_chave = 20  # Um limite razoável para o tamanho da chave
    melhor_tamanho = 1
    melhor_diferenca = float('inf')

    for tamanho in range(1, tamanho_max_chave + 1):
        segmentos = [''.join(texto_cifrado[i::tamanho]) for i in range(tamanho)]
        ic_medio = sum(indice_de_coincidencia(segmento) for segmento in segmentos) / tamanho
        diferenca = abs(IC_ESPERADO - ic_medio)
        
        if diferenca*1.015 < melhor_diferenca: # tem que ser 1.5% melhor que a ultima chave
            melhor_diferenca = diferenca
            melhor_tamanho = tamanho


    return melhor_tamanho
