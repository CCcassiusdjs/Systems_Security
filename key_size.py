from collections import Counter


def indice_de_coincidencia(segmento):
    n = len(segmento)  # Número de caracteres no segmento
    freqs = Counter(segmento)  # Conta a frequência de cada letra

    # Calcula o IC com base na frequência de cada letra
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
    return ic


def encontrar_tamanho_chave_ic(texto_cifrado, IC_ESPERADO):
    tamanho_max_chave = 20  # Limite para o tamanho da chave

    melhor_tamanho = 1
    melhor_diferenca = float('inf')

    # Testa cada tamanho de chave possível até o limite
    for tamanho in range(1, tamanho_max_chave + 1):
        # Divide o texto cifrado em segmentos com base no tamanho da chave
        segmentos = [''.join(texto_cifrado[i::tamanho]) for i in range(tamanho)]

        # Calcula o IC médio para todos os segmentos
        ic_medio = sum(indice_de_coincidencia(segmento) for segmento in segmentos) / tamanho

        # Calcula a diferença entre o IC médio e o IC esperado
        diferenca = abs(IC_ESPERADO - ic_medio)

        # Adiciona um limiar de melhoria de 1.5% para escolher um novo melhor tamanho
        if diferenca * 1.015 < melhor_diferenca:
            melhor_diferenca = diferenca
            melhor_tamanho = tamanho

    return melhor_tamanho
