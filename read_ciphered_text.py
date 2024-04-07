def ler_texto_cifrado(caminho_do_arquivo):
    with open(caminho_do_arquivo, 'r') as arquivo:
        return arquivo.read()