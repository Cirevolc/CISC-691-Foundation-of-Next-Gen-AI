import string
import os

class Author:
    def __init__(self, name, signature):
        self.name = name
        self.signature = signature

class AuthorshipIdentifier:
    def __init__(self, known_authors, known_texts):
        """
        Initialize AuthorshipIdentifier with known authors and texts.

        :param known_authors: list of known authors
        :param known_texts: list of known texts
        """
        self.texts = known_texts
        self.authors = [Author(name, signature) for name, signature in zip(known_authors, self.get_all_signatures())]

    def clean_word(self, word):
        """
        Cleans a word by stripping punctuation and converting it to lowercase.

        :param word: The word to be cleaned
        :return: The cleaned word
        """

        return word.strip(string.punctuation).lower()

    def split_text(self, text):
        """
        Splits a text into words and cleans them.

        :param text: The text to be split
        :return: List of cleaned words
        """
        return [self.clean_word(word) for word in text.split()]
    
    def get_word_list(self, text):
        """
        Generates a list of cleaned words from the given text.

        This method splits the input text into individual words and 
        applies the cleaning process to each word.

        :param text: The text to be processed
        :return: List of cleaned words
        """

        return [self.clean_word(word) for word in self.split_text(text)]

    def average_word_length(self, words):
        """
        Calculates the average word length of a given list of words.

        :param words: The list of words to calculate the average for
        :return: The average word length
        """
        return sum(len(word) for word in words) / len(words)

    def different_to_total(self, words):
        """
        Calculates the ratio of unique words to the total number of words.

        :param words: The list of words to calculate the ratio for
        :return: The ratio of unique words to the total number of words
        """
        return len(set(words)) / len(words)

    def exactly_once_to_total(self, words):
        """
        Calculates the ratio of words which occur exactly once in the text to the total number of words.

        :param words: The list of words to calculate the ratio for
        :return: The ratio of words which occur exactly once to the total number of words
        """
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
    