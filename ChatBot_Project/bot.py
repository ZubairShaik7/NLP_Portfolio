import os
import pickle
import sqlite3

import pandas as pd
from nltk.corpus.reader import nltk
from difflib import SequenceMatcher

nltk.download('stopwords')
from nltk.corpus import stopwords
import spacy

# load a model
nlp = spacy.load('en_core_web_md')

stopwords = set(stopwords.words('english'))

with open('classifier', 'rb') as training_model:
    model = pickle.load(training_model)

loaded_vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))


# questions = list()
# questions.append("What is Ronaldo's total goals?")
# questions.append("How many Champions League trophies does Real Madrid have?")
# questions.append("How tall is Messi?")
# questions.append("Where is FC Barcelona from?")

def getClosestMatch(df, name, columns):
    highest_name = ''
    highest_score = 0
    for (columnName, columnData) in df[columns].iteritems():
        for value in columnData.values:
            currScore = SequenceMatcher(None, value, name)
            print(currScore.ratio(), value, highest_score)
            if currScore.ratio() > highest_score:
                highest_score = currScore.ratio()
                highest_name = value
    return str(highest_name)


def runModel(question):
    curr = list(question)
    X_test = loaded_vectorizer.transform(curr).toarray()
    pred = model.predict(X_test)
    return pred[0]


class UserModel:
    def __init__(self):
        self.name = ''
        self.isNewUser = True
        self.context = ''
        self.question = ''
        self.logout = False
        self.introduction = False
        self.likes = ''
        self.dislikes = ''
        self.intent = ''
        self.subintent = ''
        self.playersDF = pd.read_sql('SELECT * FROM players', conn)
        self.winnersDF = pd.read_sql('SELECT * FROM winners', conn)
        self.clubsDF = pd.read_sql('SELECT * FROM clubs', conn)


def runBot():
    if user.isNewUser:
        if not user.introduction:
            print("Hey I'm Marcus, your personal assistant for Champions League info! You can ask me questions"
                  "about the clubs historically present in the Champions League, or even about players that played in "
                  "it! Some sample questions would be:"
                  "- Who does Messi play for?"
                  "- What country is Real Madrid located in?"
                  "- How many trophies does Liverpool have?"
                  "Additionally if you would like to leave the chat please enter logout")
            user.name = input("To start, please enter your name so I can remember you for next time.")
            user.introduction = True
        else:
            if os.path.exists(f'users/{user.name}.txt'):
                with open(f'users/{user.name}.txt', 'r', encoding='utf-8') as f:
                    user.context = f.read()
            print(f"Hello {user.name}, Welcome back! I remember you liked {user.likes}")
            user.introduction = False
    while not user.logout:
        user.question = input(f"So {user.name}, What would you like answered today?")
        if user.question == 'logout':
            if user.name:
                filename = f'users/{user.name}.txt'
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(user.context)
            user.logout = True
            user.introduction = True
            print(f"Thanks for stopping by {user.name}!")
            continue
        user.intent = runModel(user.question)
        user.context = 'misc stuff'
        if user.intent == 'Player':
            doc = nlp(user.question)
            person = ''
            for token in doc:
                print(token, token.lemma_, token.pos_, token.tag_)
                if token.tag_ == 'NNP' or token.tag_ == 'NN':
                    person = str(token)
            if person != '':
                person = getClosestMatch(user.playersDF, person, ['Player'])
                print(person)
                if 'goal' in user.question.lower() or 'score' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(playerAtts.iloc[0]['Goals'])
                    if playerAtts.iloc[0]['Goals'] == None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'appear' in user.question.lower() or 'caps' in user.question.lower() or \
                        'played' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(playerAtts.iloc[0]['Appearances'])
                    if playerAtts.iloc[0]['Appearances'] == None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'country' in user.question.lower() or 'nation' in user.question.lower() or \
                        'from' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(playerAtts.iloc[0]['Nationality'])
                    if playerAtts.iloc[0]['Nationality'] == None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'club' in user.question.lower() or 'team' in user.question.lower() or \
                        'play for' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(playerAtts.iloc[0]['Club'])
                    if playerAtts.iloc[0]['Club'] == None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'height' in user.question.lower() or 'tall' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(playerAtts.iloc[0]['Height'])
                    if playerAtts.iloc[0]['Height'] == None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'weigh' in user.question.lower() or 'heavy' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(playerAtts.iloc[0]['Weight'])
                    if playerAtts.iloc[0]['Weight'] == None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'age' in user.question.lower() or 'old' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(playerAtts.iloc[0]['Age'])
                    if playerAtts.iloc[0]['Age'] == None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'born' in user.question.lower() or 'birthday' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(playerAtts.iloc[0]['Birth_Date'])
                    if playerAtts.iloc[0]['Birth_Date'] == None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'position' in user.question.lower() or 'role' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(playerAtts.iloc[0]['Preffered_Position'])
                    if playerAtts.iloc[0]['Preffered_Position'] == None:
                        print(f"Sorry, we dont have that information on {person}")
            else:
                print(
                    "I couldn't find that person in my records unfortunately, try specifying or ask another question.")


if __name__ == "__main__":
    conn = sqlite3.connect("champions_league_database2")
    user = UserModel()
    runBot()
