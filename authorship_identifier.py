import string
import os

class AuthorshipIdentifier:
    def __init__(self, texts):
        self.authors = [author for author, _ in texts]
        self.texts = [text for _, text in texts]
        self.signatures = self.get_all_signatures()

    def clean_word(self, word):
        return word.strip(string.punctuation).lower()

    def split_text(self, text):
        return [self.clean_word(word) for word in text.split()]

    def average_word_length(self, text):
        words = self.split_text(text)
        words = [self.clean_word(word) for word in words]
        return sum(len(word) for word in words) / len(words)

    def different_to_total(self, text):
        words = self.split_text(text)
        words = [self.clean_word(word) for word in words]
        return len(set(words)) / len(words)

    def exactly_once_to_total(self, text):
        words = self.split_text(text)
        words = [self.clean_word(word) for word in words]
        return len([word for word in set(words) if words.count(word) == 1]) / len(words)

    def average_sentence_length(self, text):
        sentences = text.split('.')
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        total_words = sum(len(sentence.split()) for sentence in sentences)
        return total_words / len(sentences) if sentences else 0

    def average_paragraph_length(self, text):
        paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newlines
        paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
        total_sentences = sum(len(paragraph.split('.')) for paragraph in paragraphs)
        return total_sentences / len(paragraphs) if paragraphs else 0

    def make_signature(self, text):
        return (
            self.average_word_length(text),
            self.different_to_total(text),
            self.exactly_once_to_total(text),
            self.average_sentence_length(text),
            self.average_paragraph_length(text)  # Adding the new feature
        )

    def get_all_signatures(self):
        return [(author, self.make_signature(text)) for (author, text) in zip(self.authors, self.texts)]

    def make_guess(self, text):
        signature = self.make_signature(text)
        return min(self.signatures, key=lambda x: sum((a - b) ** 2 for a, b in zip(signature, x[1])))

def read_texts_from_folder(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                texts.append((filename.split('.')[0], file.read()))
    return texts

known_texts = read_texts_from_folder('./ch7/known_authors')

identifier = AuthorshipIdentifier(known_texts)

unknown_texts = read_texts_from_folder('./ch7')

for i, text in enumerate(unknown_texts):
    guess = identifier.make_guess(text)
    print(f'Unknown text {i+1} is most likely written by the author with signature: {guess}')