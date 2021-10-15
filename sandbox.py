# cran.all.1400 is the text document
# cran.qry is the query
# cranqrel is the answer key

import string 
import numpy as np

def parseWordLine(splits, currentQueryFrequency):
    # Invalid: stop words, punctuation, numbers
    closed_class_stop_words = ['a', 'the', 'an', 'and', 'or', 'but', 'about', 'above', 'after', 'along', 'amid', 'among',
                               'as', 'at', 'by', 'for', 'from', 'in', 'into', 'like', 'minus', 'near', 'of', 'off', 'on',
                               'onto', 'out', 'over', 'past', 'per', 'plus', 'since', 'till', 'to', 'under', 'until', 'up',
                               'via', 'vs', 'with', 'that', 'can', 'cannot', 'could', 'may', 'might', 'must',
                               'need', 'ought', 'shall', 'should', 'will', 'would', 'have', 'had', 'has', 'having', 'be',
                               'is', 'am', 'are', 'was', 'were', 'being', 'been', 'get', 'gets', 'got', 'gotten',
                               'getting', 'seem', 'seeming', 'seems', 'seemed',
                               'enough', 'both', 'all', 'your' 'those', 'this', 'these',
                               'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',
                               'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',
                               'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',
                               'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',
                               'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',
                               'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',
                               'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',
                               'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace',
                               'anything', 'anytime' 'anywhere', 'everybody', 'everyday',
                               'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',
                               'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',
                               'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their', 'theirs',
                               'you', 'your', 'yours', 'me', 'my', 'mine', 'I', 'we', 'us', 'much', 'and/or'
                               ]
    invalidChars = string.punctuation
    for word in splits:
        if not(word.isnumeric() or word in invalidChars or word in closed_class_stop_words):
            currentQueryFrequency[word] = currentQueryFrequency.get(word, 0) + 1

def readFromFile(queryFile):
    currentQueryFrequency = dict()
    accumulatedQueries = []

    line = queryFile.readline()
    isReadingQuery = False

    while line != None:
        splits = line.strip().split(" ")
        if splits[0] == ".W": # start of new query
            isReadingQuery = True
        elif (splits[0] == ".I" or splits[0] == "") and len(currentQueryFrequency) != 0:
            isReadingQuery = False
            accumulatedQueries.append(currentQueryFrequency)
            currentQueryFrequency = dict()
            if splits[0] == "":
                break
        elif isReadingQuery:
            parseWordLine(splits, currentQueryFrequency)
        line = queryFile.readline()
    
    return accumulatedQueries

def tfidf(documents):
    totalDocuments = len(documents)
    documentFrequency = dict() # number of documents a word appears in
    for document in documents:
        for word in document:
            documentFrequency[word] = documentFrequency.get(word, 0) + 1
    for document in documents:
        for word in document:
            idf = np.log(totalDocuments / documentFrequency[word])
            document[word] = document[word] / idf

def cosineSimilarity(queryList, abstractList):
    results = []
    for i, query in enumerate(queryList):
        for j, abstract in enumerate(abstractList):
            score = similarity(query, abstract)
            results.append((i + 1, j + 1, score))
    return results

def similarity(query, abstract):
    queryScores = []
    abstractScores = []
    for word in query:
        queryScore = query[word]
        queryScores.append(queryScore)
        abstractScore = abstract.get(word, 0)
        abstractScores.append(abstractScore)
    queryArray = np.array(queryScores)
    abstractArray = np.array(abstractScores)
    top = np.sum(abstractArray * queryArray)
    bot = np.sqrt(np.sum(abstractArray * queryArray) * np.sum(queryArray * queryArray))
    return top / bot if top != 0 or bot != 0 else 0

def main():
    # First Step: read from query file
    queryFile = open("Cranfield_collection_HW/cran.qry")
    queryList = readFromFile(queryFile)
    queryFile.close()

    # Second Step: read from document
    abstractFile = open("Cranfield_collection_HW/cran.all.1400")
    abstractList = readFromFile(abstractFile)
    abstractFile.close()

    # Third Step: calculate TF-IDF score
    tfidf(queryList)
    tfidf(abstractList)

    # Fourth Step: calculate cosine similarity between each query and each abstract
    print(cosineSimilarity(queryList, abstractList))


if __name__ == '__main__':
    main()
