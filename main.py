from decipher import decifrar_texto

# Para os arquivos específicos com interação do usuário
arquivos_interativos = ["./20201-teste-PT.txt", "./20201-teste-EN.txt"]
for arquivo in arquivos_interativos:
    if not decifrar_texto(arquivo):
        break

# Para os testes automáticos sem interação do usuário
for i in range(1, 32):
    print("Decifrando arquivo {}...".format(i))
    decifrar_texto(f"./testFiles/cipher{i}.txt", interacao_usuario=False)

print("Encerramento dos testes.")

