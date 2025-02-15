import os
import re
import string
from collections import Counter

class Author:
    def __init__(self, name, signature):
        self.name = name
        self.signature = signature

class AuthorshipIdentifier:
    def __init__(self, known_authors, known_texts):
        self.texts = known_texts
        self.stopwords = {
            "a", "an", "the", "is", "in", "on", "at", "of", "for", "to", "with", 
            "and", "but", "or", "so", "if", "then", "that", "this", "these", "those",
            "he", "she", "it", "we", "they", "you", "i", "me", "him", "her", "us", "them"
        }
        self.authors = [Author(name, signature) for name, signature in zip(known_authors, self.get_all_signatures())]

    def remove_stopwords(self, text):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.stopwords]
        return " ".join(filtered_words)

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
    
    def average_words_per_chapter(self, text):
        chapters = re.split(r'\bChapter\s+\d+\b', text, flags=re.IGNORECASE)[1:]
        if not chapters:
            return 0
        word_counts = [len(chapter.split()) for chapter in chapters]
        word_counts = [count for count in word_counts if count >= 10]
        avg_word_count = sum(word_counts) / len(word_counts) if word_counts else 0
        return avg_word_count

    def get_hapax_legomena_ratio(self, words):
        return sum(1 for word, count in Counter(words).items() if count == 1) / len(words)

    def average_sentence_length(self, text):
        sentences = re.split(r'[.!?]', text)
        valid_sentences = [sentence for sentence in sentences if len(sentence.strip().split()) > 0]
        word_counts = [len(sentence.strip().split()) for sentence in valid_sentences]
        return sum(word_counts) / len(word_counts) if word_counts else 0

    def average_paragraph_length(self, text):
        paragraphs = text.split('\n\n')
        valid_paragraphs = [para for para in paragraphs if len(para.strip().split()) > 0]
        word_counts = [len(para.strip().split()) for para in valid_paragraphs]
        return sum(word_counts) / len(word_counts) if word_counts else 0

    def make_signature(self, text):
        words = self.get_word_list(text)
        return (
            self.average_word_length(words),
            self.different_to_total(words),
            self.exactly_once_to_total(words),
            self.get_hapax_legomena_ratio(words),
            self.average_words_per_chapter(text),
            self.average_sentence_length(text),
            self.average_paragraph_length(text)
        )

    def get_all_signatures(self):
        return [self.make_signature(text) for text in self.texts]

    def make_guess(self, text):
        signature = self.make_signature(text)
        return min(self.authors, key=lambda author: sum((a - b) ** 2 for a, b in zip(signature, author.signature)))

def read_texts_from_folder(folder_path):
    authors, texts = [], []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                authors.append(' '.join(filename.split('.')[0].split('_')))
                texts.append(file.read())
    return authors, texts

# Adjust the path if needed
known_authors, known_texts = read_texts_from_folder(r'C:\Users\vikramp\OneDrive - School Health Corporation\Desktop\ch7\known_authors')

identifier = AuthorshipIdentifier(known_authors, known_texts)

# Adjust the path if needed
unknown_authors, unknown_texts = read_texts_from_folder(r'C:\Users\vikramp\OneDrive - School Health Corporation\Desktop\ch7\unknown_authors')

# Output for unknown authors
for i, text in enumerate(unknown_texts):
    words = identifier.get_word_list(text)
    print(f'Unknown author {unknown_authors[i]}:')
    print(f'  Average word length: {identifier.average_word_length(words)}')
    print(f'  Different words to total words ratio: {identifier.different_to_total(words)}')
    print(f'  Words occurring exactly once to total words ratio: {identifier.exactly_once_to_total(words)}')
    print(f'  Hapax legomena ratio: {identifier.get_hapax_legomena_ratio(words)}')
    print(f'  Average words per chapter: {identifier.average_words_per_chapter(text)}')
    print(f'  Average sentence length: {identifier.average_sentence_length(text)}')
    print(f'  Average paragraph length: {identifier.average_paragraph_length(text)}')
    print('---')

# Output for known authors
for i, text in enumerate(known_texts):
    words = identifier.get_word_list(text)
    print(f'Known author {known_authors[i]}:')
    print(f'  Average word length: {identifier.average_word_length(words)}')
    print(f'  Different words to total words ratio: {identifier.different_to_total(words)}')
    print(f'  Words occurring exactly once to total words ratio: {identifier.exactly_once_to_total(words)}')
    print(f'  Hapax legomena ratio: {identifier.get_hapax_legomena_ratio(words)}')
    print(f'  Average words per chapter: {identifier.average_words_per_chapter(text)}')
    print(f'  Average sentence length: {identifier.average_sentence_length(text)}')
    print(f'  Average paragraph length: {identifier.average_paragraph_length(text)}')
    print('---')
#Note this code has all functions for other functions you guys have to add your syntax it should work
