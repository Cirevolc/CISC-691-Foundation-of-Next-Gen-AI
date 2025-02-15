import os
import re
import string

class Author:
    def __init__(self, name, signature):
        self.name = name
        self.signature = signature

class AuthorshipIdentifier:
    def __init__(self, known_authors, known_texts):
        self.texts = known_texts
        self.authors = [Author(name, signature) for name, signature in zip(known_authors, self.get_all_signatures())]

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
        return (
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

# Output for known unauthors
for i, text in enumerate(unknown_texts):
    # Output the values for average_sentence_length and average_paragraph_length
    avg_sentence_length = identifier.average_sentence_length(text)
    avg_paragraph_length = identifier.average_paragraph_length(text)
    
    print(f'Unknown author {unknown_authors[i]}:')
    print(f'  Average sentence length: {avg_sentence_length}')
    print(f'  Average paragraph length: {avg_paragraph_length}')
    print('---')

# Output for known authors
for i, text in enumerate(known_texts):
    avg_sentence_length = identifier.average_sentence_length(text)
    avg_paragraph_length = identifier.average_paragraph_length(text)
    
    print(f'Known author {known_authors[i]}:')
    print(f'  Average sentence length: {avg_sentence_length}')
    print(f'  Average paragraph length: {avg_paragraph_length}')
    print('---')
