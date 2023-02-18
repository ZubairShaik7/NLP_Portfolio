# Homework 2
# CS 4395 NLP
# Zubair Shaik

import pathlib
import sys
import nltk
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.text import Text
from random import seed
from random import randint


# this is the word guessing game function which inputs the list of words
def guessingGame(wordBank):
    seed(1234)
    userScore = 5
    print('Lets play a word guessing game!')
    # start the game here and only exit when input is ! or user has negative score
    while True:
        # get the random work from the list and create an empty list with underscores in place of letters
        wordToGuess = wordBank[randint(1, 49)]
        numberOfLetters = len(wordToGuess)
        wordSoFar = []
        for i in range(numberOfLetters):
            wordSoFar.append('_ ')
            print('_ ', end='')
        print('')
        currLetter = ''
        # this loop is to let the user guess another letter until they win or lose
        while userScore > 0 and numberOfLetters > 0:
            currLetter = input('Guess a letter or type ! to exit the game: ')
            if currLetter == '!':
                break
            isGuessTrue = False
            # check if the letter is in the word by going through the for loop
            for i in range(len(wordToGuess)):
                # if the word is in the letter and hasnt already been guessed update the values
                if wordSoFar[i] == '_ ' and wordToGuess[i] == currLetter:
                    isGuessTrue = True
                    wordSoFar[i] = currLetter
                    numberOfLetters -= 1
            # if the letter guessed is correct update the values and output the word with the added letters
            if isGuessTrue:
                userScore += 1
                print('Right! Score is', userScore)
                for letter in wordSoFar:
                    print(letter, end='')
                print('')
                # this means the word has been solved and the game is complete
                if numberOfLetters == 0:
                    print('You solved it! ')
                    print('Current score: ', userScore)
                    print('Guess another word')
            else:
                userScore -= 1
                print('Sorry guess again. Score is ', userScore)
                # this means the user ran out of guesses and the game ends here
                if userScore == 0:
                    print('Game Over')
                    print('The answer was: ', wordToGuess)
                    break
                for letter in wordSoFar:
                    print(letter, end='')
                print('')
        # these are the exit conditions for the game
        if currLetter == '!' or userScore == 0:
            break
    return


def preprocessText(text):
    # tokenize the words followed by lowercase them
    tokens = word_tokenize(text)
    tokens = [t.lower() for t in tokens if t.isalpha()]

    # filter out non alpha tokens, tokens that are stopwords, and tokens that are less than 5 letters long
    tokens = [t for t in tokens if t.isalpha() and
              t not in stopwords.words('english') and len(t) > 5]

    # get the lemmas from the tokens with wnl, and then create a list of unique lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    lemmas_unique = list(set(lemmas))

    # get the pos for the lemmas
    tags = nltk.pos_tag(lemmas_unique)

    print("\nSome POS tagged words are:\n", tags[:20])

    # get all the nouns from the tags list and return them to the main function
    nouns = list()
    for token, pos in tags:
        if pos == 'NN':
            curr = [token, pos]
            nouns.append(curr)
    print("\nThe number of tokens are: ", len(tokens))
    print("\nThe number of nouns are: ", len(nouns))
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

    # create unique set of tokens
    setOfTokens = set(tokens)
    text_const = Text(tokens)

    print("\nLexical diversity: %.2f" % (len(setOfTokens) / len(tokens)))

    # pass in the raw text to the processor function to tokenize and lemmatize it and return nouns
    tokens, nouns = preprocessText(text)

    pos_dict = {}

    # fill in the dictionary with nouns and the occurrences of them as values
    for token, pos in nouns:
        count = 0
        for word in tokens:
            if word == token:
                count += 1
        pos_dict[token] = count

    top50 = 50
    wordBank = []
    # output the top 50 highest occuring nouns from the dict
    for pos in sorted(pos_dict, key=pos_dict.get, reverse=True):
        print(top50, ': ', pos, ':', pos_dict[pos], 'occurrences')
        wordBank.append(pos)
        top50 -= 1
        if top50 == 0:
            break
    print('')
    # Starting the word guessing game by calling the function and passing in the list of words
    guessingGame(wordBank)
