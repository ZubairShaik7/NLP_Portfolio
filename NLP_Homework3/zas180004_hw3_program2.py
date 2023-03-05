# Homework 4
# CS 4395 NLP
# Zubair Shaik and Dhruv Thoutireddy

import pathlib
import pickle
from nltk import word_tokenize, ngrams


# computes the probability of a language based on the text received
def compute_prob(text, unigram_dict, bigram_dict):
    # get the ungram and bigram dicts for the text
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    unique_tokens = len(unigram_dict)

    p_laplace = 1

    # get the counts of each word in the text to calculate LaPlace probability
    for bigram in bigrams_test:
        bigram_count = bigram_dict[bigram] if bigram in bigram_dict else 0
        unigram_count = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((bigram_count + 1) / (unigram_count + unique_tokens))

    return p_laplace


if __name__ == '__main__':
    # have the names of the languages stored in an arr
    languages = ['English', 'Italian', 'French']
    predictions = list()
    rel_path = 'data/LangId.test'

    # open the test file and split by line, and then iterate over each line
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        lines = f.read()
    text = lines.splitlines()
    for line in text:
        # counters to store the highest prob value and its associated language
        h = 0
        index = 0
        # iterate through each language and calculate its prob
        for i in range(len(languages)):
            unigram_dict = pickle.load(open(languages[i] + '_unigram.pickle', 'rb'))
            bigram_dict = pickle.load(open(languages[i] + '_bigram.pickle', 'rb'))
            prob = compute_prob(line, unigram_dict, bigram_dict)
            if prob is not None and prob > h:
                h = prob
                index = i
        # store the predictions of the lien in the list
        prediction = str(index)
        if prediction == '0':
            predictions.append('English')
        elif prediction == '1':
            predictions.append('Italian')
        else:
            predictions.append('French')

    # calculate the accuracy of the predictions against the correct values from a file
    with open(pathlib.Path.cwd().joinpath('data/LangId.sol'), 'r') as f:
        lines = f.read()
    text = lines.splitlines()
    correct = 0
    total = 0
    for line in text:
        line = line.split()
        correctVal = line[1]
        if correctVal == predictions[total]:
            correct += 1
        else:
            print('Line ' + str(total) + ' is incorrectly classified')
        total += 1
    print('Correctly classified instances accuracy is: ' + str(correct / total) + ' %')
