import os
import re
import string
import spacy
from nltk.util import ngrams
from collections import Counter

class Author:
    def __init__(self, name, signature):
        self.name = name
        self.signature = signature

class AuthorshipIdentifier:
    def __init__(self, known_authors, known_texts, n=3):
        self.texts = known_texts
        self.nlp = spacy.load("en_core_web_sm")
        self.n = n # define n for n-grams
        #list of common stopwords (customize as needed)
        self.stopwords = {
            "a", "an", "the", "is", "in", "on", "at", "of", "for", "to", "with", 
            "and", "but", "or", "so", "if", "then", "that", "this", "these", "those",
            "he", "she", "it", "we", "they", "you", "i", "me", "him", "her", "us", "them"
            }
        self.authors = [Author(name, signature) for name, signature in zip(known_authors, self.get_all_signatures())]

    def remove_stopwords(self, text):
        words = text.split()  # Split text into words
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
        # Use regex to find all chapter sections, ignoring the chapter index
        chapters = re.split(r'\bChapter\s+\d+\b', text, flags=re.IGNORECASE)[1:]  # Skip the first empty split before "Chapter"

        if not chapters:
            return 0  # Return 0 if no chapters are found

        # Count words in each chapter (ignoring the chapter title)
        word_counts = [len(chapter.split()) for chapter in chapters]

        # Remove index chapters with less than 10 words
        word_counts = [count for count in word_counts if count>=10]
        
        # Calculate average word count per chapter
        avg_word_count = sum(word_counts) / len(word_counts)
        
        return avg_word_count
    
    def get_hapax_legomena_ratio(self, words):
        """
        Calculate the hapax legomena ratio, which is the ratio of words which occur only once in the text.
        
        :param words: list of words
        :return: hapax legomena ratio
        """
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

    def average_paragraphs_per_chapter(self, text):
        # Use regex to find all chapter sections, ignoring the chapter index
        chapters = re.split(r'\bCHAPTER\s+\w+', text, flags=re.IGNORECASE)[1:]
        def count_valid_paragraphs(chapter):
            paragraphs = chapter.split('\n\n')
            return sum(1 for p in paragraphs if len(p.split()) > 10)  # Count only paragraphs with more than 10 words
        paragraph_counts = [count_valid_paragraphs(chapter) for chapter in chapters if
                            count_valid_paragraphs(chapter) > 10]
        return sum(paragraph_counts) / len(paragraph_counts) if paragraph_counts else 0

    def extract_ngrams(self, text, n):
        doc = self.nlp(text.lower())
        words = [token.text for token in doc if token.is_alpha]
        return list(ngrams(words, n))

    def make_signature(self, text):
        # removing stopwords from text
        text = self.remove_stopwords(text)
        words = self.get_word_list(text)
        ngram_freq = Counter(self.extract_ngrams(text, self.n))
        top_ngram_score = sum(ngram_freq.values()) / len(ngram_freq) if ngram_freq else 1
        
        return (self.average_word_length(words), self.different_to_total(words), self.exactly_once_to_total(words), 
                self.get_hapax_legomena_ratio(words), self.average_words_per_chapter(text),  self.average_sentence_length(text),
            self.average_paragraph_length(text), self.average_paragraphs_per_chapter(text), top_ngram_score)

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

known_authors_, known_texts_ = read_texts_from_folder('./ch7/known_authors')
identifier = AuthorshipIdentifier(known_authors_, known_texts_)

unkown_authors, unknown_texts = read_texts_from_folder('./ch7')

for i, text_ in enumerate(unknown_texts):
    guess = identifier.make_guess(text_)
    print(f'Unknown author {unkown_authors[i]} is most likely written by the author: {guess.name}')