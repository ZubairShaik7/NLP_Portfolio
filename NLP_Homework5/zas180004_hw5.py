# Homework 5
# CS 4395 NLP
# Zubair Shaik and Dhruv Thoutireddy

from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import requests
import re
import os
import pickle


# function to get the top frequented words from the topkenized files
def getMostFrequentWords(tokenizedFiles):
    readFromPath = os.path.join(os.getcwd(), "tokenizedFiles")
    termFrequency = {}
    for f in tokenizedFiles:
        with open(os.path.join(readFromPath, f), 'r') as currentFile:
            text = currentFile.read()
        # process the words here to ensure valid words are being selected
        intialTokenizedWords = word_tokenize(text)
        finalTokenizedWords = [word.lower() for word in intialTokenizedWords if word.isalpha() and
                               word.lower() not in stopwords.words('english')]
        # update the term frequency dict
        for word in finalTokenizedWords:
            if word in termFrequency:
                termFrequency[word] += 1
            else:
                termFrequency[word] = 1
        # sort the dict and return the 40 most frequent words
        topWords = sorted(termFrequency.items(), key=lambda x: x[1], reverse=True)
        return topWords[:40]


# function to clean the raw url text and write to a new file with tokenized words
def cleanup(counter):
    tokenizedFiles = list()
    writeToPath = os.path.join(os.getcwd(), "tokenizedFiles")
    readFromPath = os.path.join(os.getcwd(), "urlFiles")
    os.mkdir(writeToPath)
    counter = counter - 1
    while counter >= 0:
        with open(os.path.join(readFromPath, 'url_' + str(counter) + '.txt'), 'r') as currentFile:
            text = currentFile.read()
        tokenizedSentences = sent_tokenize(text)

        # if the text is empty no need to add it to a file
        if len(tokenizedSentences) < 1:
            continue

        cleanedUpSentences = list()
        # using regex to remove whitespace from the text and then writing the text to a new file
        for sentence in tokenizedSentences:
            if "$(" not in sentence or "><" not in sentence:
                cleanedUpSentences.append('\n' + re.sub(r'\s+', ' ', sentence))
        file_name = "tokenizedURL_" + str(counter) + ".txt"
        with open(os.path.join(writeToPath, file_name), 'w') as newFile:
            newFile.write(' '.join(cleanedUpSentences))
            tokenizedFiles.append(file_name)
        counter = counter - 1

    return tokenizedFiles


def getAllURLS(dataObject):
    # write urls to a file
    with open('urls.txt', 'w') as f:
        # go through all a tags and check to see if there are any valid links
        for link in dataObject.find_all('a'):
            link_str = str(link.get('href'))
            print("a tag: ", link_str)
            # condition here to get useful info from links only
            if 'messi' in link_str or 'Messi' in link_str:
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                    print('MOD:', link_str)
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if link_str.startswith('http') and 'google' not in link_str and 'wikipedia' not in link_str:
                    f.write(link_str + '\n')


# function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


# this function simply returns unique urls from the list of all urls
def getUniqueURLS(allURLS):
    uniqueURLS = list()

    for i in allURLS:
        if i not in uniqueURLS:
            uniqueURLS.append(i)
    return uniqueURLS


# this function retrieves text from the url list and determines if the info in it is useful to write to a file
def writeURLStoFiles(uniqueURLS):
    counter = 0
    i = 0
    path = os.path.join(os.getcwd(), "urlFiles")
    os.mkdir(path)
    while counter < 30 and i < len(uniqueURLS):
        url = uniqueURLS[i]
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        # using try catch here to catch the request exception and move on to next url
        webpage = ''
        try:
            webpage = requests.get(url, headers=headers, allow_redirects=False, timeout=3)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("URL is Invalid", url)
            i = i + 1
            continue
        if webpage:
            # check to see if the text is valid and then add it to a new file
            dataObject = BeautifulSoup(webpage.text, features="lxml")
            webText = dataObject.findAll(text=True)
            result = filter(visible, webText)
            temp_list = list(result)  # list from filter
            temp_str = ' '.join(temp_list)
            if "messi" not in temp_str or "Messi" not in temp_str:
                i = i + 1
                continue
            file_name = "url_" + str(counter) + ".txt"
            new_file = open(os.path.join(path, file_name), 'w')
            new_file.write(temp_str)
            counter = counter + 1
        i = i + 1
    return counter


def createKnowledgeBase(fileList):
    topicFacts = {}

    readFromPath = os.path.join(os.getcwd(), "tokenizedFiles")
    for f in fileList:
        with open(os.path.join(readFromPath, f), 'r') as currentFile:
            text = currentFile.read()
        text = text.split('\n')
        for sentence in text:
            for word in manuallySelectedWords:
                if word in sentence:
                    if word in topicFacts:
                        topicFacts[word].append(sentence)
                    else:
                        curr = list()
                        curr.append(sentence)
                        topicFacts[word] = curr
    return topicFacts


if __name__ == '__main__':
    # use starter url as source website to start the scraping
    starter_url = 'https://en.wikipedia.org/wiki/Lionel_Messi'
    r = requests.get(starter_url)

    data = r.text
    soup = BeautifulSoup(data, features="lxml")

    # get the list of all urls it can scrape
    getAllURLS(soup)

    file = open('urls.txt', 'r')
    URL_files = file.readlines()

    # filter out the unique urls
    uniqueUrls = getUniqueURLS(URL_files)

    # write the raw url text to new files
    numOfFiles = writeURLStoFiles(uniqueUrls)

    # write the tokenized and cleaned up text to new files
    cleanedFiles = cleanup(numOfFiles)

    # get the most frequent words from the text
    mostFrequentWords = getMostFrequentWords(cleanedFiles)

    print(mostFrequentWords)

    manuallySelectedWords = ["messi", "lionel", "argentina", "psg", "records", "trophies", "goals", "assists",
                             "forward", "stats"]

    knowledgeBase = createKnowledgeBase(cleanedFiles)

    pickle.dump(knowledgeBase, open('knowledgeBase.pickle', 'wb'))

    # end of program
    print("end of crawler")
