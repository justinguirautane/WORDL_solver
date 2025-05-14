import pandas as pd
import json
import unidecode

# Source http://www.lexique.org/shiny/openlexicon/
df = pd.read_csv("Lexique383/Lexique383.tsv", sep='\t')

df = df.ortho
df = df.dropna()
df = df.drop_duplicates()

list_words = list(df)
print(len(list_words))
temp = list_words[:]
for word in temp:
    if len(word.split(' ')) != 1:
        list_words.remove(word)
print(len(list_words))

temp = list_words[:]
for word in temp:
    if "'" in word:
        list_words.remove(word)
print(len(list_words))

list_no_accent = []
for word in list_words:
    list_no_accent.append(unidecode.unidecode(word))

print(len(list_no_accent))
print(list_words[-5:])
print(list_no_accent[-5:])

with open("liste_mots_FR.json", 'w') as f:
    json.dump(list_no_accent, f)
