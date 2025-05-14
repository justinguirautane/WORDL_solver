import pandas as pd

with open("liste_francais/liste_francais.txt", 'r', encoding='utf-8', errors='ignore') as f:
    liste_francais = f.readlines()

print(len(liste_francais))


Lexique383 = pd.read_csv("Lexique383/Lexique383.tsv", sep='\t')
print(Lexique383.head())
print(len(Lexique383))

