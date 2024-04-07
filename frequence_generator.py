import itertools


def gerador_de_frequencias(frequencias, n_top_letras):
    # Ordenar as letras pela frequência e pegar as top N mais frequentes
    letras_mais_frequentes = sorted(frequencias, key=frequencias.get, reverse=True)[:n_top_letras]

    # Gerar todas as permutações possíveis dessas letras
    permutacoes = itertools.permutations(letras_mais_frequentes)

    # Iterar sobre cada permutação para criar um novo dicionário de frequências
    for permutacao in permutacoes:
        nova_frequencia = frequencias.copy()  # Copia o dicionário de frequências original

        # Atribuir as frequências das letras permutadas
        for i, letra in enumerate(letras_mais_frequentes):
            nova_frequencia[letra] = frequencias[permutacao[i]]

        yield nova_frequencia  # Retorna o novo dicionário de frequências
