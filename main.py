from decipher import decrypt_text

# For specific files with user interaction
interactive_files = ["./20201-TESTE-PT.txt", "./20201-TESTE-EN.txt"]
for file in interactive_files:
    if not decrypt_text(file):
        break

# For automatic tests without user interaction
for i in range(1, 32):
    print("Decrypting file {}...".format(i))
    decrypt_text(f"./testFiles/cipher{i}.txt", user_interaction=False)

print("Tests completed.")


