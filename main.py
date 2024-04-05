from pycipher import Vigenere
from collections import Counter


def decifrar_com_vigenere(texto_cifrado, chave):
    vigenere = Vigenere(chave)
    return vigenere.decipher(texto_cifrado)


import encontrar_tamanho_chave_ic as etc
import calcular_chave_otimizada as cco
import ler_texto_cifrado as ltc
import lingua_helpers as lh
import determinar_idioma as di
import gerador_de_frequencias as gf

numeroDeCombinacoes = 26

def decifrar_texto(caminho_do_arquivo):
    
    texto_cifrado = ltc.ler_texto_cifrado(caminho_do_arquivo).lower()

    idioma = di.determinar_idioma(texto_cifrado,lh.frequencia_ingles_10,lh.frequencia_portugues_10 )

    IC_ESPERADO = lh.get_IC_Esperado(idioma)
    frequenciaAlfabeto =  lh.frequencia_portugues if idioma == 'portugues' else lh.frequencia_ingles
    for frequencia_combinada in gf.gerador_de_frequencias(frequenciaAlfabeto,numeroDeCombinacoes): 
        tamanho_chave = etc.encontrar_tamanho_chave_ic(texto_cifrado, IC_ESPERADO)
        chave = cco.calcular_chave_otimizada(texto_cifrado, tamanho_chave, frequencia_combinada)
        texto_decifrado = decifrar_com_vigenere(texto_cifrado, chave)
        print("Texto Decifrado", texto_decifrado[:40], "no idioma:", idioma)
        #print('está correto?')
        if False:
            break

    return






# Executar o programa
    
caminho_do_arquivo_PT = "./20201-teste-PT.txt"
caminho_do_arquivo_EN = "./20201-teste-EN.txt"
for file in [caminho_do_arquivo_EN, caminho_do_arquivo_PT]:
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
    
  
#testFiles(3)
