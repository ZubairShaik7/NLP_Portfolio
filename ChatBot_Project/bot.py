import os
import pickle
import sqlite3
import pandas as pd
import spacy
from nltk.corpus.reader import nltk
from difflib import SequenceMatcher
from nltk.corpus import stopwords

nltk.download('stopwords')

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

country_dict = {"ESP": "Spain", "ENG": "England", "ITA": "Italy", "GER": "Germany", "POR": "Portugal",
                "FRA": "France", "NED": "Netherlands", "POL": "Poland", "ROU": "Romania", "RUS": "Russia",
                "AUT": "Austria", "SCO": "Scotland", "SRB": "Serbia", "SUI": "Switzerland", "SVK": "Slovakia",
                "SVN": "SLovenia", "TUR": "Turkey", "NOR": "Norway", "ISR": "Israel", "KAZ": "Kazakhstan",
                "AZE": "Azerbaijan", "HUN": "Hungary", "GRE": "Greece", "FIN": "Finland", "DEN": "Denmark",
                "SWE": "Sweden", "CZE": "Czech Republic", "CYP": "Cyprus", "CRO": "Croatia", "BUL": "Bulgaria",
                "BLR": "Belarus", "BEL": "Belguim", "UKR": "Ukraine", "MDA": "Moldova", "IRL": "Ireland",
                "ALB": "Albania", "MLT": "Malta", "LVA": "Latvia", "NIR": "Northern Ireland", "LTU": "Lithuania",
                "GEO": "Georgia", "ISL": "Iceland", "ARM": "Armenia", "BIH": "Bosnia and Herzegovina",
                "LUX": "Luxemborg", "MKD": "North Macedonia", "EST": "Estonia", "WAL": "Wales", "FRO": "Faroe Island",
                "MNE": "Montegro", "KOS": "Kosovo", "GIB": "Gibraltar", "AND": "Andorra", "SMR": "San Marino"}


# Use this function to get the closest similarity between two words using SequenceMatcher
def getClosestMatch(df, name, columns):
    highest_name = ''
    highest_score = 0
    for (columnName, columnData) in df[columns].iteritems():
        for value in columnData.values:
            currScore = SequenceMatcher(None, value, name)
            if currScore.ratio() > highest_score:
                highest_score = currScore.ratio()
                highest_name = value
    return str(highest_name)


# run the model on the user input to get the predictions
def runModel(question):
    question = [question]
    X_test = loaded_vectorizer.transform(question).toarray()
    pred = model.predict(X_test)
    return pred


# instantiate the user with a new model to store all the personal info
class UserModel:
    def __init__(self):
        self.name = ''
        self.isNewUser = True
        self.question = ''
        self.logout = False
        self.introduction = False
        self.likes = list()
        self.dislikes = list()
        self.context = list()
        self.intent = ''
        self.playersDF = pd.read_sql('SELECT * FROM players', conn)
        self.winnersDF = pd.read_sql('SELECT * FROM winners', conn)
        self.clubsDF = pd.read_sql('SELECT * FROM clubs', conn)
        self.firstTime = True


def runBot():
    user.name = input("To start, please enter your name so I can remember you for next time or remember you from "
                      "before. ")
    # check if user has file stored already and read context from it
    if os.path.exists(f'users/{user.name}.txt'):
        with open(f'users/{user.name}.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('+'):
                    user.context.append(line)
                else:
                    user.context.append(line)
            for l in user.context:
                if l.startswith('+'):
                    user.likes.append(l)
                else:
                    user.dislikes.append(l)
            f.close()
        print(f"Hello {user.name}, Welcome back! I remember you liked {user.likes}")
    else:
        print("Hey I'm Marcus, your personal assistant for Champions League info! You can ask me questions \n"
              "about the clubs historically present in the Champions League, or even about players that played in \n"
              "it! Some sample questions would be: \n"
              "- Who does Messi play for? \n"
              "- What country is Real Madrid located in? \n"
              "- How many trophies does Liverpool have? \n"
              "Please make sure to capitalize all players and club names, as well as type out the full form \n"
              "Additionally if you would like to leave the chat please enter logout \n")
    user.isNewUser = False
    user.introduction = True
    while not user.logout:
        if user.firstTime:
            user.question = input(f"So {user.name}, What would you like answered today? ")
        else:
            user.question = input(f"Anything else you want answered {user.name}? ")
        if user.question == 'logout':
            if user.name:
                filename = f'users/{user.name}.txt'
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'a', encoding='utf-8') as f:
                    for item in user.likes:
                        flag = False
                        for ctx in user.context:
                            if item in ctx:
                                flag = True
                        if not flag:
                            f.write('+ ' + item + ' \n')
                    for item in user.dislikes:
                        flag = False
                        for ctx in user.context:
                            if item in ctx:
                                flag = True
                        if not flag:
                            f.write('- ' + item + ' \n')
                    f.close()
            user.logout = True
            user.introduction = True
            print(f"Thanks for stopping by {user.name}!")
            continue
        user.intent = runModel(user.question)
        # base the responses off the user intent from the question they asked
        if 'dont like' in user.question or 'hate' in user.question or 'dislike' in user.question:
            print('Got it! I will remember that for next time.')
            doc = nlp(user.question)
            targetWord = ''
            counter = 0
            targetIDX = 0
            for token in doc:
                counter += 1
                if token.tag_ == 'VBP':
                    if str(token) == 'do':
                        targetIDX = counter
                if counter == targetIDX + 2:
                    targetWord = str(token)
            idx = user.question.index(targetWord)
            user.dislikes.append(user.question[idx:])
        elif 'like' in user.question or 'love' in user.question or 'enjoy' in user.question:
            print('Got it! I will remember that for next time.')
            doc = nlp(user.question)
            targetWord = ''
            for token in doc:
                if token.tag_ == 'VBP':
                    targetWord = str(token)
            idx = user.question.index(targetWord)
            user.likes.append(user.question[idx:])
        elif user.intent == 'Player':
            doc = nlp(user.question)
            person = ''
            for token in doc:
                if token.tag_ == 'NNP' or token.tag_ == 'NN':
                    person = str(token)
            if person != '':
                for like in user.likes:
                    if person in like.upper():
                        print("This player must be your favorite, since you ask about him a lot!")
                for dislike in user.dislikes:
                    if person in dislike.upper():
                        print("You still want to know about him? Even though you dont like him.")
                person = getClosestMatch(user.playersDF, person, ['Player'])
                if 'goal' in user.question.lower() or 'score' in user.question.lower():
                    if 'most' in user.question.lower() or 'highest' in user.question.lower() \
                            or 'top' in user.question.lower():
                        playerAtts = user.playersDF.loc[user.playersDF['Player'] == 'Cristiano Ronaldo']
                        print('Cristiano Ronaldo has scored a champions league total of ' + str(
                            playerAtts.iloc[0]['Goals']) + ' scored.')
                        if playerAtts.iloc[0]['Goals'] is None:
                            print(f"Sorry, we dont have that information on {person}")
                    else:
                        playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                        print(person + ' has scored a champions league total of ' + str(
                            playerAtts.iloc[0]['Goals']) + ' scored.')
                        if playerAtts.iloc[0]['Goals'] is None:
                            print(f"Sorry, we dont have that information on {person}")
                elif 'appear' in user.question.lower() or 'caps' in user.question.lower() or \
                        'played' in user.question.lower():
                    if 'most' in user.question.lower() or 'highest' in user.question.lower() \
                            or 'top' in user.question.lower():
                        playerAtts = user.playersDF.loc[user.playersDF['Player'] == 'Cristiano Ronaldo']
                        print('Cristiano Ronaldo has scored a champions league total of ' + str(
                            playerAtts.iloc[0]['Goals']) + ' scored.')
                        if playerAtts.iloc[0]['Goals'] is None:
                            print(f"Sorry, we dont have that information on {person}")
                    else:
                        playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                        print(person + ' has a total of ' + str(playerAtts.iloc[0]['Appearances']) + ' appearances')
                        if playerAtts.iloc[0]['Appearances'] is None:
                            print(f"Sorry, we dont have that information on {person}")
                elif 'country' in user.question.lower() or 'nation' in user.question.lower() or \
                        'from' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(person + ' is from ' + str(playerAtts.iloc[0]['Nationality']))
                    if playerAtts.iloc[0]['Nationality'] is None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'club' in user.question.lower() or 'team' in user.question.lower() or \
                        'play for' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(person + ' plays for ' + str(playerAtts.iloc[0]['Club']))
                    if playerAtts.iloc[0]['Club'] is None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'height' in user.question.lower() or 'tall' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(person + ' is ' + str(playerAtts.iloc[0]['Height']) + ' tall')
                    if playerAtts.iloc[0]['Height'] is None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'weigh' in user.question.lower() or 'heavy' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(person + ' weighs ' + str(playerAtts.iloc[0]['Weight']))
                    if playerAtts.iloc[0]['Weight'] is None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'age' in user.question.lower() or 'old' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(person + ' is ' + str(playerAtts.iloc[0]['Age']) + ' years old')
                    if playerAtts.iloc[0]['Age'] is None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'born' in user.question.lower() or 'birthday' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(person + ' was born on ' + str(playerAtts.iloc[0]['Birth_Date']))
                    if playerAtts.iloc[0]['Birth_Date'] is None:
                        print(f"Sorry, we dont have that information on {person}")
                elif 'position' in user.question.lower() or 'role' in user.question.lower():
                    playerAtts = user.playersDF.loc[user.playersDF['Player'] == person]
                    print(person + ' plays ' + str(playerAtts.iloc[0]['Preffered_Position']) + ' position')
                    if playerAtts.iloc[0]['Preffered_Position'] is None:
                        print(f"Sorry, we dont have that information on {person}")
        elif user.intent == 'Team':
            doc = nlp(user.question)
            team = ''
            for token in doc:
                if token.tag_ == 'NNP' or token.tag_ == 'NN':
                    team += str(token) + ' '
            if team != '':
                for like in user.likes:
                    if team in like:
                        print("This team must be your favorite, since you ask about them a lot!")
                for dislike in user.dislikes:
                    if team in dislike:
                        print("You still want to know about this team, even though you dont like them?")
                team = getClosestMatch(user.clubsDF, team, ['Club'])
                if 'country' in user.question.lower() or 'nation' in user.question.lower() \
                        or 'origin' in user.question.lower() or 'from' in user.question.lower():
                    clubAtts = user.clubsDF.loc[user.clubsDF['Club'] == team]
                    print(team + ' is located in ' + country_dict[str(clubAtts.iloc[0]['Country'])] + '.')
                    if clubAtts.iloc[0]['Country'] is None:
                        print(f"Sorry, we dont have that information on {team}")
                elif 'titles' in user.question.lower() or 'trophies' in user.question.lower() \
                        or 'first' in user.question.lower():
                    if 'most' in user.question.lower() or 'highest' in user.question.lower() \
                            or 'top' in user.question.lower():
                        clubAtts = user.clubsDF.loc[user.clubsDF['Club'] == 'Real Madrid CF']
                        print('Real Madrid CF has won the most Champions League, winning '
                              + str(clubAtts.iloc[0]['Titles']) + ' times.')
                        if clubAtts.iloc[0]['Titles'] is None:
                            print(f"Sorry, we dont have that information on {team}")
                    else:
                        clubAtts = user.clubsDF.loc[user.clubsDF['Club'] == team]
                        print(team + ' has won the Champions League ' + str(clubAtts.iloc[0]['Titles'])
                              + ' times.')
                        if clubAtts.iloc[0]['Titles'] is None:
                            print(f"Sorry, we dont have that information on {team}")
                elif 'wins' in user.question.lower() or 'won' in user.question.lower() \
                        or 'loss' in user.question.lower() or 'lost' in user.question.lower() \
                        or 'draw' in user.question.lower() or 'tie' in user.question.lower():
                    if 'most' in user.question.lower() or 'highest' in user.question.lower() \
                            or 'top' in user.question.lower():
                        clubAtts = user.clubsDF.loc[user.clubsDF['Club'] == 'Real Madrid CF']
                        print('Real Madrid CF has won the most Champions League games, winning '
                              + str(clubAtts.iloc[0]['Win']) + ' times.')
                        if clubAtts.iloc[0]['Win'] is None:
                            print(f"Sorry, we dont have that information on {team}")
                    else:
                        clubAtts = user.clubsDF.loc[user.clubsDF['Club'] == team]
                        print(team + ' has won ' + str(clubAtts.iloc[0]['Win'])
                              + ' times, drawn ' + str(clubAtts.iloc[0]['Draw'])
                              + ' times, and lost ' + str(clubAtts.iloc[0]['Loss'])
                              + ' times.')
                        if clubAtts.iloc[0]['Win'] is None:
                            print(f"Sorry, we dont have that information on {team}")
                elif 'goals' in user.question.lower() or 'scored' in user.question.lower():
                    if 'most' in user.question.lower() or 'highest' in user.question.lower() \
                            or 'top' in user.question.lower():
                        clubAtts = user.clubsDF.loc[user.clubsDF['Club'] == 'Real Madrid CF']
                        print('Real Madrid CF has won the most Champions League games, winning '
                              + str(clubAtts.iloc[0]['Goals For']) + ' times.')
                        if clubAtts.iloc[0]['Goals For'] is None:
                            print(f"Sorry, we dont have that information on {team}")
                    else:
                        clubAtts = user.clubsDF.loc[user.clubsDF['Club'] == team]
                        print(team + ' has scored ' + str(clubAtts.iloc[0]['Goals For'])
                              + ' times in the Champions League.')
                        if clubAtts.iloc[0]['Goals For'] is None:
                            print(f"Sorry, we dont have that information on {team}")
        elif user.intent == 'Final':
            doc = nlp(user.question)
            date = ''
            for token in doc:
                if token.pos_ == 'NUM' or token.tag_ == 'CD':
                    date += str(token) + '-'
            date = getClosestMatch(user.winnersDF, date, ['SEASONS'])
            if 'where' in user.question.lower() or 'location' in user.question.lower() \
                    or 'held' in user.question.lower():
                clubAtts = user.winnersDF.loc[user.winnersDF['SEASONS'] == date]
                print('The ' + date + ' Champions League final was held in ' + str(clubAtts.iloc[0]['VENUE'])
                      + ' with an attendance of ' + str(clubAtts.iloc[0]['ATTENDANCE']) + '.')
                if clubAtts.iloc[0]['VENUE'] is None:
                    print(f"Sorry, we dont have that information on the {date} Champions League final.")
            elif 'won' in user.question.lower() or 'champion' in user.question.lower() \
                    or 'winner' in user.question.lower():
                clubAtts = user.winnersDF.loc[user.winnersDF['SEASONS'] == date]
                print('The ' + date + ' Champions League final winner was ' + str(clubAtts.iloc[0]['WINNERS_TEAM'])
                      + ' from ' + country_dict[str(clubAtts.iloc[0]['WINNERS_NATION'])] + '.')
                if clubAtts.iloc[0]['WINNERS_TEAM'] is None:
                    print(f"Sorry, we dont have that information on the {date} Champions League final.")
            elif 'lost' in user.question.lower() or 'runner up' in user.question.lower() \
                    or 'second' in user.question.lower() or 'loser' in user.question.lower():
                clubAtts = user.winnersDF.loc[user.winnersDF['SEASONS'] == date]
                print('The ' + date + ' Champions League final runner up was '
                      + str(clubAtts.iloc[0]['RUNNERS_UP_TEAM']) + ' from '
                      + country_dict[str(clubAtts.iloc[0]['RUNNERS_UP_NATION'])] + '.')
                if clubAtts.iloc[0]['RUNNERS_UP_TEAM'] is None:
                    print(f"Sorry, we dont have that information on the {date} Champions League final.")
            elif 'score' in user.question.lower() or 'result' in user.question.lower() \
                    or 'outcome' in user.question.lower() or 'loser' in user.question.lower():
                clubAtts = user.winnersDF.loc[user.winnersDF['SEASONS'] == date]
                print('The ' + date + ' Champions League final score was ' + str(clubAtts.iloc[0]['SCORE'])
                      + ' between ' + str(clubAtts.iloc[0]['WINNERS_TEAM']) + ' and '
                      + str(clubAtts.iloc[0]['RUNNERS_UP_TEAM']))
                if clubAtts.iloc[0]['SCORE'] is None:
                    print(f"Sorry, we dont have that information on the {date} Champions League final.")
        else:
            print("I couldn't find that person in my records unfortunately, try specifying or ask another question.")


# run the main app
if __name__ == "__main__":
    conn = sqlite3.connect("champions_league_database2")
    user = UserModel()
    runBot()
