# Homework 4
# CS 4395 NLP
# Zubair Shaik and Dhruv Thoutireddy

from nltk import word_tokenize
from nltk.util import ngrams
import sys
import pathlib
import pickle


def process_text(filename):
    rel_path = filename
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        lines = f.read()
    text = lines.replace('\n', ' ')

    unigrams = word_tokenize(text)
    tokens = word_tokenize(text)

    bigrams = list(ngrams(tokens, 2))

    # print(bigrams)

    unigram_dict = {u: unigrams.count(u) for u in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    return unigram_dict, bigram_dict


if __name__ == '__main__':
    for i in range(3):
        if len(sys.argv) < 2:  # if arguments in control line are not the python file and csv, program will quit
            currentData = input('Please enter a file: ')
            if currentData == '':
                quit()

        name = currentData
        name = name.split(".")
        print('Processing the text for ' + name + ' language')
        uni_dict, bi_dict = process_text(currentData)
        bigram_pickle_name = name[2] + "_bigram.pickle"
        unigram_pickle_name = name[2] + "_unigram.pickle"

        pickle.dump(uni_dict, open(unigram_pickle_name, 'wb'))
        pickle.dump(bi_dict, open(bigram_pickle_name, 'wb'))
        print("Pickling for " + name[2] + " ngrams has been completed")
