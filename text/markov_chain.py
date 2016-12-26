# -*- coding: utf-8 -*-

import sys

from collections import *
import random

class MarkovChain:

    def __init__(self, original_text="", chain_length=2):

        self.chain_length = chain_length

        self.original_text = original_text

    def __str__(self):
        return ", ".join(self.splitted_text)

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

    def create_transition_map(self):

        self.transition_map = defaultdict(list)

        for i in range(len(self.splitted_text) - self.chain_length):

            word_tuple = self.get_word_tuple_at(i)
            
            self.transition_map[word_tuple].append(self.splitted_text[i + self.chain_length])

    def get_word_tuple_at(self, i):

        t = ()

        for word in self.splitted_text[i:i+self.chain_length]:
            t = t + tuple([word])

        return t

    def generate_text(self, length=10, first_words=None):

        if length < self.chain_length:
            raise Exception("Generated text length must be atleast {0}".format(self.chain_length))

        if first_words == None:
            first_words = self.get_first_words()
        
        generated_words = first_words

        word_tuple = tuple(first_words)

        for i in range(length - self.chain_length):
            word = self.choose_next_word(word_tuple)

            if word == None:
                break

            generated_words = generated_words + tuple([word])

            word_tuple = word_tuple[1:] + tuple([word])

        return " ".join(generated_words)

    def get_first_words(self):
        return tuple(self.splitted_text[:self.chain_length])

    def choose_next_word(self, word_tuple):
        try:
            return random.choice(self.transition_map[word_tuple])
        except Exception:
            return None

def test_splitted_text():

    markov_chain = MarkovChain()
    
    test_text = "hello there again"
    markov_chain.original_text = test_text

    assert len(markov_chain.splitted_text) == len(test_text.split())
    assert len(markov_chain.transition_map) == len(test_text.split()) - 2
    assert markov_chain.transition_map[("hello", "there")] == ["again"]

    test_text = "lazy dog jumped over another lazy dog"
    markov_chain.original_text = test_text

    assert len(markov_chain.splitted_text) == len(test_text.split())
    assert len(markov_chain.transition_map) == len(test_text.split()) - 2
    assert markov_chain.transition_map[("over", "another")] == ["lazy"]

def usage():
    print("""
    Usage
        python markov_chain.py [input_file] [generated_text_length] [first words]
    """)

def main():

    if len(sys.argv) < 2:
        usage()
        exit()

    f = open(sys.argv[1], 'r')
    original_text = f.read()

    markov_chain = MarkovChain(original_text, chain_length=2)

    first_words = None

    if len(sys.argv) < 3:
        print(markov_chain.generate_text())
        exit()

    if len(sys.argv) > 4:
        first_words = (sys.argv[3], sys.argv[4])

    generated_text_length = int(sys.argv[2])
    print(markov_chain.generate_text(length=generated_text_length, first_words=first_words))

if __name__ == "__main__":
    main()
