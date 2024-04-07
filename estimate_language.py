
def calcular_frequencia(texto):
    # Remove espaços e converte para letras maiúsculas
    texto = texto.replace(" ", "").upper()
    frequencia = {}

    # Conta a frequência de cada letra
    for letra in texto:
        if letra.isalpha():  # Verifica se é uma letra
            frequencia[letra] = frequencia.get(letra, 0) + 1

    # Calcula o total de letras para normalizar a frequência
    total_letras = sum(frequencia.values())

    # Normaliza a frequência para percentual
    for letra in frequencia:
        frequencia[letra] = (frequencia[letra] / total_letras) * 100

    return frequencia


def calcular_qui_cubo_alterado(observado, esperado):
    qui_quadrado = 0
    for letra in observado:
        if letra in esperado:
            # Calcula o qui-quadrado usando a terceira potência
            qui_quadrado += ((observado.get(letra, 0) - esperado.get(letra, 0)) ** 3) / esperado.get(letra, 1)

    return qui_quadrado


def determinar_idioma(texto_cifrado, frequencia_esperada_ingles, frequencia_esperada_portugues):
    # Calcula a frequência das letras no texto cifrado
    frequencia_observada = calcular_frequencia(texto_cifrado)

    # Calcula o qui-cubo alterado para inglês e português
    qui_quadrado_ingles = calcular_qui_cubo_alterado(frequencia_observada, frequencia_esperada_ingles)
    qui_quadrado_portugues = calcular_qui_cubo_alterado(frequencia_observada, frequencia_esperada_portugues)

    # Determina o idioma baseado no menor valor de qui-quadrado
    return "portugues" if qui_quadrado_portugues < qui_quadrado_ingles else "ingles"


