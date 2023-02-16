# Homework 2
# CS 4395 NLP
# Zubair Shaik

import pathlib
import sys
import nltk
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.text import Text

def preprocessText(text):
    tokens = word_tokenize(text)

    tokens = [t.lower() for t in tokens if t.isalpha()]

    tokens = [t for t in tokens if t.isalpha() and
              t not in stopwords.words('english') and len(t) > 5]

    wnl = WordNetLemmatizer()

    lemmas = [wnl.lemmatize(t) for t in tokens]

    lemmas_unique = list(set(lemmas))

    tags = nltk.pos_tag(lemmas_unique)

    print("\nSome POS tagged words are:\n", tags[:20])

    nouns = list()
    for token, pos in tags:
        if pos == 'NN':
            curr = [token, pos]
            nouns.append(curr)
    print("\nThe number of tokens are:\n", len(tokens))
    print("\nThe number of nouns are:\n", len(nouns))
    return tokens, nouns

# This is the main driver function that starts the program and reads and writes to the pickle file
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read()

    # remove newline characters
    text = text_in.replace('\n', ' ')

    tokens = word_tokenize(text)

    # lowercase, get rid of punctuation, numbers
    tokens = [t.lower() for t in tokens if t.isalpha()]

    setOfTokens = set(tokens)

    text_const = Text(tokens)

    print("\nLexical diversity: %.2f" % (len(setOfTokens) / len(tokens)))

    tokens, nouns = preprocessText(text)

    dict = {}

    for token,pos in nouns:
        count = 0
        for word in tokens:
            if word == token:
                count+=1
        dict[token]=count