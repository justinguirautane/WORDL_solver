import json

with open("liste_ouverture_FR.txt", 'r', encoding='utf-8', errors='ignore') as f:
    liste_francais = f.readlines()

print(liste_francais)

clean_list = []

for w in liste_francais:
    clean_list.append(w.lower().replace('\n', ''))

print(clean_list)


with open("liste_ouvertures_FR.json", 'w') as f:
    json.dump(clean_list, f)