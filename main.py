from pycipher import Vigenere
import sys


def decifrar_com_vigenere(texto_cifrado, chave):
    vigenere = Vigenere(chave)
    return vigenere.decipher(texto_cifrado)


import encontrar_tamanho_chave_ic as etc
import calcular_chave_otimizada as cco
import ler_texto_cifrado as ltc
import lingua_helpers as lh
import determinar_idioma as di
import gerador_de_frequencias as gf

numeroDeCombinacoes = 10

def escolhaDoUsuario():
    opcoes = ''' 
    1 - achei a mensagem cifrada, termine o programa
    2 - quero trocar de língua
    3 - finalize o programa
    '''
    return input(opcoes)


def determinaListaDeIdiomas(texto):
    idiomaProvavel = di.determinar_idioma(texto,lh.frequencia_ingles_10,lh.frequencia_portugues_10 )
    idiomas = ['portugues', 'ingles']
    if idiomas[0] != idiomaProvavel:
        idiomas.reverse()
    return idiomas


def decifraTextoIdiomaDescoberto(texto_cifrado,idioma, frequenciaAlfabeto, tamanho_chave):
    #jeito rapido
    chave = cco.calcular_chave_otimizada_rapido(texto_cifrado, tamanho_chave, 'e')
    texto_decifrado = decifrar_com_vigenere(texto_cifrado, chave)
    print("usando método rápido: Texto Decifrado", texto_decifrado[:40], "no idioma provável:", idioma)
    print("Interrompa no teclado quando achar o texto claro, quiser trocar de lingua ou quiser finalizar")
    #jeito lento
    for frequencia_combinada in gf.gerador_de_frequencias(frequenciaAlfabeto,numeroDeCombinacoes): 
        try:
            chave = cco.calcular_chave_otimizada(texto_cifrado, tamanho_chave, frequencia_combinada)
            texto_decifrado = decifrar_com_vigenere(texto_cifrado, chave)
            print("Texto Decifrado", texto_decifrado[:40], "no idioma provável:", idioma)
        except KeyboardInterrupt:
            escolha = escolhaDoUsuario()
            if escolha == '1' or escolha == '3':
                print("encerrando programa")
                sys.exit()
                return
            if escolha == '2':
                break
            else:
                continue

def decifrar_texto(caminho_do_arquivo):
    texto_cifrado = ltc.ler_texto_cifrado(caminho_do_arquivo).lower()
    idiomas = determinaListaDeIdiomas(texto_cifrado)
    
    for idioma in idiomas:
        IC_ESPERADO = lh.get_IC_Esperado(idioma)
        frequenciaAlfabeto =  lh.frequenciasAlfabetos[idioma]
        tamanho_chave = etc.encontrar_tamanho_chave_ic(texto_cifrado, IC_ESPERADO)
        
        decifraTextoIdiomaDescoberto(texto_cifrado,idioma, frequenciaAlfabeto, tamanho_chave)
        
    return






# Testes
    
caminho_do_arquivo_PT = "./20201-teste-PT.txt"
caminho_do_arquivo_EN = "./20201-teste-EN.txt"
for file in [caminho_do_arquivo_PT, caminho_do_arquivo_EN]:
    decifrar_texto(file)
    

def testFiles(until):
    print("-------Init cyoher tests files")
    def thread_function(i):
        respostas = decifrar_texto("./testFiles/cipher"+str(i)+".txt")
        for r in respostas:
            texto, idioma = r
            print("Decifrando arquivo teste: cipher", i, "Texto Decifrado no idioma", texto[:40], "no idioma:", idioma)
            
        return
    
    
    for i in range(1, until+1):
        thread_function(i)
    
testFiles(31)

# log de encerramento
print("encerrando programa")