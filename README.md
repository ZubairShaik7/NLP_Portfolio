# NLP_Portfolio
Portfolio from NLP class

## Program 1

This program is just to practice adding files to this repository.

You can see the [code here](program1.py) and a [descriptive document here](Sample_Document.pdf)

You can see my overview of NLP so far  through this [descriptive document here](Overview_NLP.pdf)

## Assignment 1 - Text Processing

This program is meant to get comfortable with python coding practices including using file I/O, 
regex, pickling, and working with classes.

The program reads in a csv file containing employee information (one per line) and parses the info
line by line to make sure all the info is formatted correctly. It returns a dictionary containing all the 
correctly formatted employee information.

You can see the [code here](NLP_Homework1/zas180004_hw1.py)

To run the program, use the following command within the same directory as the file:
python3 zas180004_hw1.py (insert path to csv file)

Python is useful for text processing because of its simple syntax and many widely
available packages to make processing even easier. This assignment was a good review
of basic python commands and syntax for me and I got to learn more about pickling as well.
This serves as a good base project to be prepared for the upcoming assignments.


## Assignment 2 - Word Guessing Game

This program is meant to get comfortable with python coding practices as well as using the NLTK library.

The program reads in a text file and tokenizes the words through NLTK to get all the nouns
in the text. It then lets the user play a word guessing game with the nouns as the word bank
for the program to randomly chose from.

You can see the [code here](NLP_Homework2/zas180004_hw2.py)

To run the program, use the following command within the same directory as the file:
python3 zas180004_hw2.py (insert path to text file)

## Assignment 3 - WordNet Usage

This file was meant to gain more familiarity with WordNet

You can see the [code here](WordNet_Assignment.pdf)

## Assignment 4 - N-Grams Model

This program allowed us to create a language model through N-Grams and test it out on a text file to determine
the accuracy of the model.

You can see the code where we created the unigram and bigram dictionaries from the corpus
[here](NLP_Homework3/zas180004_hw3_program1.py)

The code for test our model can be found [here](NLP_Homework3/zas180004_hw3_program2.py)

A short narrative on N-Grams can be found [here](NLP_Homework3/N-gram-narrative.pdf)

## Assignment 5 - Web Crawler

This program allowed us to crawl through websites using BeautifulSoup to scrape data about a certain topic and process
the text by cleaning and tokenizing it. We used the text to create a knowledge base of facts to use in our chatbot

You can see the code where we created the knowledge base
[here](NLP_Homework5/zas180004_hw5.py)

A short narrative on Web Crawling can be found [here](NLP_Homework5/Web_Crawler_Report.pdf)

## Assignment 6: Parsing Sentences

In this assignment, I usaed PSG, dependency, and SRL parsing to anaalyze sentences and understand how they should be parsed.

You can view my paper analyzing complex sentences [here](Sentence-Parsing.pdf)

## Assignment 7: ACL Paper Summary

In this assignment, I analyze a reasearch paper about task oriented dialogue and write a paper over it.

You can view my paper [here](2022.acl-long.425.pdf)

## Assignment 8 - Chatbot

In this project, I created a chatbot which talks about the Champions league and is able to asnwer fact based questions about it.  
I used various NLP techniques including NER, tf-idf, and vectorization along with many more. The knowledge base was generated through datasets
pulled through kaggle and converted into a sqlite database. I used a Naive Bayes model to train the model on a set of questions and return an intent.

You can see the code where we created chatbot  [here](ChatBot_Project/bot.py)

The training model can be found [here](ChatBot_Project/training_model.py)

A report on the project can be found [here](ChatBot_Project/ChatBot_Report.pdf)

To run the program, use the following commands within the same directory as the file:
1. python3 training_model.py
2. python3 bot.py (insert path to text file)

## Assignment 9: Text Classification

In this assignment, I analyzed a dataset which contains true and fake news articles and attempted to classify them based off the text from the articles
using various different NLP algorithms including CNN, Embeddings, and Neural Networks.

You can view my notebook [here](text_classification_hlt.pdf)

## Portfolio Summary
This course has really allowed me to dive deep into the world of Natural Language Processing and has helped me pick up valuable skills for my future career within Software Engineering and Data Science. I really enjoyed learning about topics like Parts of Speech tagging and Neural Netowrks. With the explosion of AI based tools, including ChatGPT, I feel that it is invaluable and essential to be well versed in that domain moving forward and this course has given me the confidence to do so. The ChatBot project was my favorite assignment to work on as it incorporated all of the techniques and skills we were working on throughout the course and allowed me to combine everything to make a useful product. Overall, I will use the skills learned here for a long time and will continue to wet my feet in this domain. Some of the skills I gained from this course can be found [here](skills.md)
