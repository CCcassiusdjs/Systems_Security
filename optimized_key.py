from collections import Counter


def calcular_chave_otimizada_rapido(texto_cifrado, tamanho_chave, letra_mais_frequente_idioma):
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

        # Corrige o deslocamento para o intervalo de 0-25 e adiciona à chave
        chave_otimizada += chr((deslocamento + 26) % 26 + ord('a'))

    return chave_otimizada


def calcular_chave_otimizada(texto_cifrado, tamanho_chave, frequencia_idioma):
    chave_otimizada = ''

    for i in range(tamanho_chave):
        segmento = texto_cifrado[i::tamanho_chave]
        contador = Counter(segmento)

        melhor_desvio = float('inf')
        melhor_letra = ''

        # Compara cada letra possível com a frequência das letras no segmento
        for letra_chave in frequencia_idioma:
            desvio_total = 0

            # Calcula o desvio entre a frequência observada e esperada
            for letra, freq in contador.items():
                letra_deslocada = chr((ord(letra) - ord(letra_chave)) % 26 + ord('a'))
                desvio_total += abs(frequencia_idioma.get(letra_deslocada, 0) - freq)

            # Seleciona a letra que minimiza o desvio total
            if desvio_total < melhor_desvio:
                melhor_desvio = desvio_total
                melhor_letra = letra_chave

        chave_otimizada += melhor_letra

    return chave_otimizada


# Exemplo das funções otimizadas
texto_cifrado = "exemplo cifrado para teste"
tamanho_chave = 3
letra_mais_frequente_idioma = 'e'
frequencia_idioma = {'e': 0.12702, 't': 0.09056, 'a': 0.08167}  # exemplo de frequências

# Chamada das funções otimizadas
chave_rapida = calcular_chave_otimizada_rapido(texto_cifrado, tamanho_chave, letra_mais_frequente_idioma)
chave_lenta = calcular_chave_otimizada(texto_cifrado, tamanho_chave, frequencia_idioma)

var = chave_rapida, chave_lenta
