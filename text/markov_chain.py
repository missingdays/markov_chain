
import sys

from collections import namedtuple
import random

WordTuple = namedtuple("WordTuple", ["first_word", "second_word"])

class MarkovChain:

    def __init__(self, original_text=""):

        self.original_text = original_text

    @property
    def original_text(self):
        return self._original_text

    @original_text.setter
    def original_text(self, value):

        self._original_text = value
        self.create_splitted_text()
        self.create_transition_map()

    def create_splitted_text(self):
        self.splitted_text = self.original_text.split()

        if len(self.splitted_text) < 2:
            raise Exception("Original text must contain atleast two words")

    def create_transition_map(self):

        self.transition_map = {}

        first_word = self.splitted_text[0]
        second_word = self.splitted_text[1]

        for word in self.splitted_text[2:]:

            word_tuple = WordTuple(first_word=first_word, second_word=second_word)

            self.insert_to_transition_map(word_tuple, word)

            first_word = second_word
            second_word = word

    def insert_to_transition_map(self, word_tuple, word):
        if word_tuple in self.transition_map:
            self.transition_map[word_tuple].append(word)
        else:
            self.transition_map[word_tuple] = [word]

    def generate_text(self, length=10, first_word=None, second_word=None):

        if length < 2:
            raise Exception("Generated text length must be atleast two")
        
        if first_word == None:
            first_word = self.splitted_text[0]
        if second_word == None:
            second_word = self.splitted_text[1]

        generated_text = first_word + " " + second_word

        for i in range(length - 2):
            word_tuple = WordTuple(first_word=first_word, second_word=second_word)

            word = self.choose_next_word(word_tuple)

            if word == None:
                break

            generated_text += " " + word

            first_word = second_word
            second_word = word

        return generated_text

    def choose_next_word(self, word_tuple):
        try:
            return random.choice(self.transition_map[word_tuple])
        except(Exception):
            return None

def test_splitted_text():

    markov_chain = MarkovChain()
    
    test_text = "hello there again"
    markov_chain.original_text = test_text

    assert len(markov_chain.splitted_text) == len(test_text.split())
    assert len(markov_chain.transition_map) == len(test_text.split()) - 2
    assert markov_chain.transition_map[WordTuple(first_word="hello", second_word="there")] == ["again"]

    test_text = "lazy dog jumped over another lazy dog"
    markov_chain.original_text = test_text

    assert len(markov_chain.splitted_text) == len(test_text.split())
    assert len(markov_chain.transition_map) == len(test_text.split()) - 2
    assert markov_chain.transition_map[WordTuple(first_word="over", second_word="another")] == ["lazy"]

def usage():
    print("""
    Usage
        python markov_chain.py [input_file] [generated_text_length]
    """)

def main():

    if len(sys.argv) < 2:
        usage()
        exit()

    f = open(sys.argv[1], 'r')
    original_text = f.read()

    markov_chain = MarkovChain(original_text)

    if len(sys.argv) < 3:
        print(markov_chain.generate_text())
        exit()

    generated_text_length = int(sys.argv[2])
    print(markov_chain.generate_text(length=generated_text_length))

if __name__ == "__main__":
    main()
