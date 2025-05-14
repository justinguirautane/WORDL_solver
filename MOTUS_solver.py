import json
from collections import defaultdict

from MOTUS_simulator import MotusSimulator

# Open word list
with open("datasets/liste_mots_FR.json", 'r') as f:
    list_words = json.load(f)

with open("datasets/liste_ouvertures_FR.json", 'r') as f:
    list_open = json.load(f)

def solve(compute_result, blues, oranges, starting_letter, word_length):

    # Reduce list word to starting letter and word lenght
    list_words_reduced_start_lenght = [word for word in list_words if word[0] == starting_letter and len(word) == word_length]

    # Reduce to the one with RED first
    list_index_reds = [[i,compute_result[i][0]]  for i in range(len(compute_result)) if compute_result[i][1] == 'RED']
    reduced_list = []
    for word in list_words_reduced_start_lenght:
        found = True
        for index in list_index_reds:
            if word[index[0]] != index[1]:
                found = False
                break
        if found == True:
            reduced_list.append(word)

    # Orange letters must be in the words
    ## Remove words that dont contain the needed letters
    reduced_list = list(set(reduced_list))
    orange_letters = [letter[0] for letter in compute_result if letter[1] == "ORANGE"] + [letter[0] for letter in compute_result if letter[1] == "RED"]
    temp = reduced_list[:]
    to_remove = set()
    for word in temp:
        for oletter in orange_letters:
            if oletter not in word:
                to_remove.add(word)
    for word in to_remove:
        reduced_list.remove(word)
    ## Remove word with placement already tested for orange letters
    temp = reduced_list[:]
    to_remove = set()
    for word in temp:
        for oletter, tried_pos in oranges.items():
            for pos in tried_pos:
                if word[pos] == oletter:
                    to_remove.add(word)
    for word in to_remove:
        reduced_list.remove(word)

    # Blue letters MUST NOT be in the words
    reduced_list = list(set(reduced_list))
    temp = reduced_list[:]
    to_remove = set()
    for word in temp:
        for bletter in blues:
            if bletter not in oranges.keys() and bletter != compute_result[0][0] : # it means that there more than one occurence of the letter
                if bletter in word:
                    to_remove.add(word)
                    break
    for word in to_remove:
        reduced_list.remove(word)

    return list(set(reduced_list))

def choose_words_proposed(propositions):
    # Get the word with the max different letters and max voyelles

    scores = {}
    for word in propositions:
        scores[word] = len(set(word))
    
    sorted_scores = {k:v for k,v in sorted(scores.items(), key=lambda i:i[1], reverse=True)}
    return sorted_scores

def pretty_print(compute_result):

    to_print = ""

    for letter in compute_result:
        if letter[1] == 'RED':
            to_print += "\033[1;31m" + letter[0] + "\033[0m"
        if letter[1] == 'ORANGE':
            to_print += "\033[1;33m" + letter[0] + "\033[0m"
        if letter[1] == 'BLUE':
            to_print += "\033[1;34m" + letter[0] + "\033[0m"
    print(to_print)

def main_simu():

    starting_letter = input("Lettre de départ: ").lower()
    word_length = int(input("Longueur du mot: "))

    # Instantiate simulator
    simulator = MotusSimulator(starting_letter, word_length)
    print("\033[35m" + simulator.selected_word + "\033[0m")
    print("\033[35m______________________________________\033[0m")

    # Select open
    # print([word for word in list_open if word[0] == starting_letter and len(word) == word_length])
    open_word = [word for word in list_open if word[0] == starting_letter and len(word) == word_length][0]

    # Compute result
    result = simulator.compute(open_word)
    pretty_print(result)

    blues = [r[0] for r in result if r[1] == "BLUE"]
    oranges = defaultdict(set)
    for i in range(len(result)):
        if result[i][1] == "ORANGE":
            oranges[result[i][0]].add(i)

    turn = 1
    while result != "FOUND":
        propositions = solve(result, blues, oranges, starting_letter, word_length)
        # print(propositions)
        sorted_scores = choose_words_proposed(propositions)
        chosen_word = list(sorted_scores.keys())[0]
        result = simulator.compute(chosen_word)
        
        if result == "FOUND":
            print("\033[1;31m" + chosen_word + "\033[0m")
        else:
            for i in range(len(result)):
                if result[i][1] == "BLUE" and result[i][0] not in blues:
                    blues.append(result[i][0])
                if result[i][1] == "ORANGE":
                    oranges[result[i][0]].add(i)
            pretty_print(result)

        turn += 1
        if turn > 5:
            break

def main_tusmo():

    starting_letter = input("Lettre de départ: ").lower()
    word_length = int(input("Longueur du mot: "))

    open_word = [word for word in list_open if word[0] == starting_letter and len(word) == word_length]
    print([o for o in open_word])

    found = False

    while found != True:

        result_tusmo = []
        for _i in range(word_length):
            result_tusmo.append(input("Resultat du mot entré (ex: a RED; b ORANGE; c BLUE): "))

        result = [x.split(' ') for x in result_tusmo]
        pretty_print(result)

        blues = [r[0] for r in result if r[1] == "BLUE"]
        oranges = defaultdict(set)
        for i in range(len(result)):
            if result[i][1] == "ORANGE":
                oranges[result[i][0]].add(i)

        propositions = solve(result, blues, oranges, starting_letter, word_length)
        sorted_scores = choose_words_proposed(propositions)
        if len(sorted_scores) != 0:
            chosen_word = list(sorted_scores.keys())[:3]
        else:
            chosen_word = "MOT NON TROUVÉ"
        print(f"> Essais ça: {chosen_word}")

   
# main_simu()

main_tusmo()