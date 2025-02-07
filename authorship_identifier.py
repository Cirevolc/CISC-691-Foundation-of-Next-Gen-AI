import string
import os

class Author:
    def __init__(self, name, signature):
        self.name = name
        self.signature = signature

class AuthorshipIdentifier:
    def __init__(self, known_authors, known_texts):
        self.texts = known_texts
        self.authors = [Author(name, signature) for name, signature in zip(known_authors, self.get_all_signatures())]

    def clean_word(self, word):
        return word.strip(string.punctuation).lower()

    def split_text(self, text):
        return [self.clean_word(word) for word in text.split()]
    
    def get_word_list(self, text):
        return [self.clean_word(word) for word in self.split_text(text)]

    def average_word_length(self, words):
        return sum(len(word) for word in words) / len(words)

    def different_to_total(self, words):
        return len(set(words)) / len(words)

    def exactly_once_to_total(self, words):
        return len([word for word in set(words) if words.count(word) == 1]) / len(words)

    def make_signature(self, text):
        words = self.get_word_list(text)
        return (self.average_word_length(words), self.different_to_total(words), self.exactly_once_to_total(words))

    def get_all_signatures(self):
        return [self.make_signature(text) for text in self.texts]

    def make_guess(self, text):
        signature = self.make_signature(text)
        return min(self.authors, key=lambda author: sum((a - b) ** 2 for a, b in zip(signature, author.signature)))

def read_texts_from_folder(folder_path):
    authors, texts = [], []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                authors.append(' '.join(filename.split('.')[0].split('_')))
                texts.append(file.read())
    return authors, texts

known_authors, known_texts = read_texts_from_folder('./ch7/known_authors')

identifier = AuthorshipIdentifier(known_authors, known_texts)

unkown_authors, unknown_texts = read_texts_from_folder('./ch7')

for i, text in enumerate(unknown_texts):
    guess = identifier.make_guess(text)
    print(f'Unknown author {unkown_authors[i]} is most likely written by the author: {guess.name}')