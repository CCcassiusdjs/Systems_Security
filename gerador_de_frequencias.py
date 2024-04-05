#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 20:11:17 2024

@author: hpc
"""

import itertools

def gerador_de_frequencias(frequencias, n_top_letras):
    # Extrair as n_top_letras mais frequentes
    letras_mais_frequentes = sorted(frequencias, key=frequencias.get, reverse=True)[:n_top_letras]

    # Gerar todas as permutações possíveis dessas letras
    permutacoes = itertools.permutations(letras_mais_frequentes)

    # Para cada permutação, criar e ceder um novo dicionário de frequências
    for permutacao in permutacoes:
        nova_frequencia = frequencias.copy()
        for i, letra in enumerate(letras_mais_frequentes):
            nova_frequencia[letra] = frequencias[permutacao[i]]
        yield nova_frequencia