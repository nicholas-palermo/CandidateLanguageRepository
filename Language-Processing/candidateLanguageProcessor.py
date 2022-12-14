import nltk, os, wordsegment, re
from nltk import FreqDist, ngrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
from wordsegment import load, segment

class candidateLanguageProcessor:

    def __init__(self, siteFileName, tweetFileName):
        self.candidate = siteFileName.split('/')[-1].split('.')[0]
        self.site = open(siteFileName).read()
        self.tweets = open(tweetFileName).read()
        self.rawText = self.site + ' ' + self.tweets
        self.rawText = (re.sub("(?P<url>https?://[^\s]+)", "gone", self.rawText))
        self.filteredTokensList = None

    def tokenizeFile(self, type):
        if type == 'filtered':
            print('Tokenizing Site File. Filter enabled...')
            unfilteredTokensList = word_tokenize(self.rawText)
            print('Tokenizing Complete.')
            self.getFilteredTokensList(unfilteredTokensList)
        elif type == 'unfiltered':
            print('Tokenizing Site File. Filter disabled...')
            return word_tokenize(self.rawText)

    def getFilteredTokensList(self, tokensList):
        stop_words = [',', '•', '©', '...', '?', '/','!','|','@', '*', '(', ')']
        doNotSegment = ['hochul', 'instagram', 'covid', 'malliotakis']
        load()
        filtered_list = []
        print('Filtering tokens list...')
        for word in tokensList:
            if word.casefold() not in stop_words:
                if word.casefold() not in doNotSegment:
                    filtered_list.extend(segment(word))
                    print(str(len(filtered_list))+'/'+str(len(tokensList)), end="\r")
                else:
                    filtered_list.append(word)
                    print(str(len(filtered_list))+'/'+str(len(tokensList)), end="\r")
        self.filteredTokensList = filtered_list

    def getNgramsList(self, n):
        print('Getting ' + str(n) + '-grams list...')
        n_grams = ngrams(self.filteredTokensList, n)
        return n_grams

    def getNgramsListToFile(self, nGramsList, n):
        print('Writing ' + str(n) + '-grams list to file...')
        with open('/Users/nicholas.palermo/Desktop/CSC450/candidateLanguage/' + self.candidate + '/' + self.candidate + '-' + str(n) + '.txt', 'a') as f:
            for gram in nGramsList:
                f.write(', '.join(gram) + '\n')

    def getNgramsFrequency(self, nGramsList, n):
        print('Getting grams frequencies...')
        gramFreqDist = FreqDist(nGramsList)
        items = sorted(gramFreqDist.items(), key=lambda item: item[1], reverse=True)
        with open('/Users/nicholas.palermo/Desktop/CSC450/candidateLanguage/' + self.candidate + '/' + self.candidate + '-' + 'Frequencies.txt', 'a') as f:
            print('Retriving ' + str(n) + '-grams frequencies.')
            f.write('\n' + str(n) + '-grams:\n')
            for k, v in items:
                gramFrequency = str(k) + ': ' + str(v)
                f.write(str(gramFrequency + '\n'))