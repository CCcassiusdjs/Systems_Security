from pycipher import Vigenere
from collections import Counter



# Parte 1: Leitura do Texto Cifrado
def ler_texto_cifrado(caminho_do_arquivo):
    with open(caminho_do_arquivo, 'r') as arquivo:
        return arquivo.read()


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
    for i in range(tamanho_chave):
        segmento = texto_cifrado[i::tamanho_chave]
        contador = Counter(segmento)
        letra_mais_frequente = max(contador, key=contador.get)
        deslocamento = ord(letra_mais_frequente) - ord('e')  # 'e' é geralmente a letra mais frequente
        chave_otimizada += chr((deslocamento + 26) % 26 + ord('a'))
    return chave_otimizada






# Função para decifrar o texto usando a Cifra de Vigenère
def decifrar_com_vigenere(texto_cifrado, chave):
    vigenere = Vigenere(chave)
    return vigenere.decipher(texto_cifrado)


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



def calcular_qui_cubo_alterado(observado, esperado):
    qui_quadrado = 0
    for letra in observado:
        if letra in esperado:
            qui_quadrado += ((observado.get(letra, 0) - esperado.get(letra, 0)) ** 3) / esperado.get(letra, 1)
    return qui_quadrado

def determinar_idioma_qui_cubo_alterado(texto_cifrado, frequencia_esperada_ingles, frequencia_esperada_portugues):
    frequencia_observada = calcular_frequencia(texto_cifrado)

    qui_quadrado_ingles = calcular_qui_cubo_alterado(frequencia_observada, frequencia_esperada_ingles)
    qui_quadrado_portugues = calcular_qui_cubo_alterado(frequencia_observada, frequencia_esperada_portugues)


    return "portugues" if float(qui_quadrado_portugues) < float(qui_quadrado_ingles) else "ingles"



# Função principal do programa
def decifrar_texto(caminho_do_arquivo):

    texto_cifrado = ler_texto_cifrado(caminho_do_arquivo).lower()
    
    frequencia_ingles_10 = {
    'E': 12.702,
    'T': 9.056,
    'A': 8.167,
    'O': 7.507,
    'I': 6.966,
    'N': 6.749,
    'S': 6.327,
    'H': 6.094,
    'R': 5.987,
    'D': 4.253,
    'L': 4.025,
    'C': 2.782,
    'U': 2.758
}

    frequencia_portugues_10 = {
    'A': 14.63,
    'E': 12.57,
    'O': 10.73,
    'S': 7.81,
    'R': 6.53,
    'I': 6.18,
    'N': 5.05,
    'D': 4.99,
    'M': 4.74,
    'U': 4.63,
    'T': 4.34,
    'C': 3.88,
    'L': 2.78
}

    idioma = determinar_idioma_qui_cubo_alterado(texto_cifrado,frequencia_ingles_10,frequencia_portugues_10 )
    #idioma = "portugues"
    frequencia_idioma = frequencia_portugues if idioma == "portugues" else frequencia_ingles

    IC_ingles = 0.0667
    IC_portugues = 0.0745
    IC_ESPERADO = IC_ingles if idioma == "ingles" else IC_portugues
    
    tamanho_chave = encontrar_tamanho_chave_ic(texto_cifrado, IC_ESPERADO)

    chave = calcular_chave_otimizada(texto_cifrado, tamanho_chave, frequencia_idioma)

    texto_decifrado = decifrar_com_vigenere(texto_cifrado, chave)

    return (texto_decifrado, idioma)


# Executar o programa
caminho_do_arquivo_PT = "./20201-teste-PT.txt"
caminho_do_arquivo_EN = "./20201-teste-EN.txt"
for file in [caminho_do_arquivo_PT, caminho_do_arquivo_EN]:
    texto, idioma = decifrar_texto(caminho_do_arquivo_PT)
    print("Testes base. Texto Decifrado no idioma", texto[:40], "no idioma:", idioma)
    
print("-------")
import threading

def thread_function(i):
    texto, idioma = decifrar_texto("./testFiles/cipher"+str(i)+".txt")
    print("Decifrando arquivo teste: cipher", i, "Texto Decifrado no idioma", texto[:40], "no idioma:", idioma)

#for i in [1,14,23]:
threads = []
for i in range(1, 31):
    thread = threading.Thread(target=thread_function, args=(i,))
    threads.append(thread)
    thread.start()
    
for thread in threads:
    thread.join()

