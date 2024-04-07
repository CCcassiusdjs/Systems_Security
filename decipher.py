from pycipher import Vigenere
import estimate_language as di
import language_helpers as lh
import frequence_generator as gf
import optimized_key as cco
import key_size as etc
import read_ciphered_text as ltc

numeroDeCombinacoes = 10


# Decifra um texto cifrado usando a cifra de Vigenère.
def decifrar_com_vigenere(texto_cifrado, chave):
    vigenere = Vigenere(chave)
    return vigenere.decipher(texto_cifrado)


# Solicita ao usuário para escolher uma das opções fornecidas.
def escolhaDoUsuario():
    opcoes = ''' 
    1 - achei a mensagem cifrada, termine o programa
    2 - quero trocar de língua
    3 - finalize o programa
    '''
    return input(opcoes)


# Determina os idiomas a serem testados com base na análise de frequência de letras.
def determinaListaDeIdiomas(texto):
    idiomaProvavel = di.determinar_idioma(texto, lh.frequencia_ingles_10, lh.frequencia_portugues_10)
    idiomas = ['portugues', 'ingles']
    if idiomas[0] != idiomaProvavel:
        idiomas.reverse()
    return idiomas


# Permite ao usuário substituir uma letra na chave por outra.
def substituirLetraNaChave(chave):
    print("Digite a posição da letra que deseja substituir e a nova letra (separados por espaço):")
    pos, nova_letra = input().split()
    pos = int(pos)
    chave = list(chave)
    chave[pos] = nova_letra
    return ''.join(chave)


# Realiza a decifração do texto cifrado, tentando diferentes chaves.
def decifraTextoIdiomaDescoberto(texto_cifrado, idioma, frequenciaAlfabeto, tamanho_chave, interacao_usuario=True):
    print("Texto Cifrado (primeiros 40 caracteres):", texto_cifrado[:40])

    # Método rápido de decifração.
    chave = cco.calcular_chave_otimizada_rapido(texto_cifrado, tamanho_chave, 'e')

    # Lógica para substituição de letras na chave, com interação do usuário.
    while True:
        texto_decifrado = decifrar_com_vigenere(texto_cifrado, chave)
        print("\nChave Atual:", chave)
        print("Texto Decifrado (primeiros 40 caracteres):", texto_decifrado[:40])

        if interacao_usuario:
            escolha = input("Deseja substituir uma letra na chave? (s/n): ")
            if escolha.lower() == 's':
                chave = substituirLetraNaChave(chave)
            else:
                break
        else:
            break

    # Método lento de decifração.
    print("\nIniciando Método Lento:")
    for frequencia_combinada in gf.gerador_de_frequencias(frequenciaAlfabeto, numeroDeCombinacoes):
        chave = cco.calcular_chave_otimizada(texto_cifrado, tamanho_chave, frequencia_combinada)
        while True:
            texto_decifrado = decifrar_com_vigenere(texto_cifrado, chave)
            print("\nChave Atual:", chave)
            print("Tamanho da Chave:", len(chave))
            print("Texto Decifrado (primeiros 40 caracteres):", texto_decifrado[:40])

            if interacao_usuario:
                escolha = input("Deseja substituir uma letra na chave? (s/n): ")
                if escolha.lower() == 's':
                    chave = substituirLetraNaChave(chave)
                else:
                    break
            else:
                return True

        if interacao_usuario:
            escolha = escolhaDoUsuario()
            if escolha in ['1', '3']:
                return False
            elif escolha == '2':
                return True

    return True

# Principal função para decifrar textos cifrados.
def decifrar_texto(caminho_do_arquivo, interacao_usuario=True):
    texto_cifrado = ltc.ler_texto_cifrado(caminho_do_arquivo).lower()
    idiomas = determinaListaDeIdiomas(texto_cifrado)

    for idioma in idiomas:
        IC_ESPERADO = lh.get_IC_Esperado(idioma)
        frequenciaAlfabeto = lh.frequenciasAlfabetos[idioma]
        tamanho_chave = etc.encontrar_tamanho_chave_ic(texto_cifrado, IC_ESPERADO)

        precisaTrocarIdioma = decifraTextoIdiomaDescoberto(texto_cifrado, idioma, frequenciaAlfabeto, tamanho_chave,
                                                           interacao_usuario)
        if precisaTrocarIdioma and interacao_usuario:
            idiomas.reverse()
            break

    return
