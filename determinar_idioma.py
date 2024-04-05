#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 18:37:54 2024

@author: hpc
"""


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


#método inspirado no qui quadrado, porém alterado baseado em testes
def calcular_qui_cubo_alterado(observado, esperado):
    qui_quadrado = 0
    for letra in observado:
        if letra in esperado:
            qui_quadrado += ((observado.get(letra, 0) - esperado.get(letra, 0)) ** 3) / esperado.get(letra, 1)
    return qui_quadrado


def determinar_idioma(texto_cifrado, frequencia_esperada_ingles, frequencia_esperada_portugues):
    frequencia_observada = calcular_frequencia(texto_cifrado)

    qui_quadrado_ingles = calcular_qui_cubo_alterado(frequencia_observada, frequencia_esperada_ingles)
    qui_quadrado_portugues = calcular_qui_cubo_alterado(frequencia_observada, frequencia_esperada_portugues)


    return "portugues" if float(qui_quadrado_portugues) < float(qui_quadrado_ingles) else "ingles"

