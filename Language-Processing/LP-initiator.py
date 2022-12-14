import os, time
from datetime import datetime

from candidateLanguageProcessor import candidateLanguageProcessor

# For all candidate ngram retrival

def allCandidateRetrieval():
    candidateSiteList = os.listdir("/Users/nicholas.palermo/Desktop/CSC450/candidateSites")
    for candidate in candidateSiteList:
        candidateRetrieval(candidate)
        

# For single candidate ngram retrival

def singleCandidateRetrieval(candidateSite):
    candidateRetrieval(candidateSite)

def candidateRetrieval(candidateSite):

    # Parent Directory path
    parent_dir = "/Users/nicholas.palermo/Desktop/CSC450/candidateLanguage/"
    # Path
    path = os.path.join(parent_dir, candidateSite.split('.')[0])
    os.mkdir(path)

    candidateSiteFile = '/Users/nicholas.palermo/Desktop/CSC450/candidateSites/' + candidateSite
    candidateTweetsFile = '/Users/nicholas.palermo/Desktop/CSC450/candidateTweets/' + candidateSite.split('.')[0] + '/' + candidateSite.split('.')[0] + '-tweets.txt'
    
    currentCandidate = candidateLanguageProcessor(candidateSiteFile, candidateTweetsFile)

    # Tokenize candidate site
    currentCandidate.tokenizeFile('filtered')

    # 5-grams
    FiveGramsList = currentCandidate.getNgramsList(5)
    currentCandidate.getNgramsFrequency(FiveGramsList, 5)

    #  4-grams
    FourGramsList = currentCandidate.getNgramsList(4)
    currentCandidate.getNgramsFrequency(FourGramsList, 4)

    # 3-grams
    TriGramsList = currentCandidate.getNgramsList(3)
    currentCandidate.getNgramsFrequency(TriGramsList, 3)

    # 2-grams
    BiGramsList = currentCandidate.getNgramsList(2)
    currentCandidate.getNgramsFrequency(BiGramsList, 2)

    # 1-grams
    UniGramsList = currentCandidate.getNgramsList(1)
    currentCandidate.getNgramsFrequency(UniGramsList, 1)

    # Print complete statement
    print(str(candidateSite) + ' completed at ' + str(datetime.now()))

    time.sleep(2)
    os.system('clear')

    # Delete object instance
    del currentCandidate



# To retrive ngram frequency
# candidateNgramList = os.listdir("/Users/nicholas.palermo/Desktop/CSC450/candidateLanguage")
# for candidate in candidateNgramList:
#     print(FreqDist(candidate).freq)

os.system('clear')

retrieval = input("Please enter candidate domain name. Enter 'ALL' for mass retrieval: ")
if retrieval.casefold() == 'all':
    allCandidateRetrieval()
else:
    singleCandidateRetrieval(retrieval.casefold() + '.txt')






