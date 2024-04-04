#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 18:24:55 2024

@author: hpc
"""

def ler_texto_cifrado(caminho_do_arquivo):
    with open(caminho_do_arquivo, 'r') as arquivo:
        return arquivo.read()