import random
import json
from collections import Counter, defaultdict

class MotusSimulator:

    def __init__(self, starting_letter, word_length):
        with open("datasets/liste_mots_FR.json", 'r') as f:
            list_words = json.load(f)

        reduced_list = [word for word in list_words if word[0] == starting_letter and len(word) == word_length]
        
        # self.selected_word = random.choice(reduced_list)
        # self.selected_word = "secourue"
        # self.selected_word = "prolongees"
        # self.selected_word = "rentree"
        self.selected_word = "virtuose"

    def compute(self, proposed_word):

        result = []

        if proposed_word == self.selected_word:
            return "FOUND"

        # Start with Reds (well placed letters)
        for i in range(len(proposed_word)):
            if proposed_word[i] == self.selected_word[i]:
                result.append([proposed_word[i], "RED"])
            else:
                result.append([proposed_word[i], "BLUE"])

        # Then oranges (not well placed letters)
        counter_found_letters = defaultdict(int)
        counter_selected_word = Counter(self.selected_word)
        for i in range(len(result)):
            counter_found_letters[result[i][0]] += 1

            if result[i][1] == "BLUE":
                if result[i][0] in counter_selected_word.keys() and counter_selected_word[result[i][0]] >= counter_found_letters[result[i][0]]:
                    result[i][1] = "ORANGE"
        
        return result

# MS = MotusSimulator('t', 5)