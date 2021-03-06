# cran.all.1400 is the text document
# cran.qry is the query
# cranqrel is the answer key

import string 
import numpy as np
import re

def parseWord(word, currentFrequency):
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
    newWord = re.sub(r'[^\w\s0-9\,.]*', '', word)
    if not(newWord.isnumeric() or newWord in invalidChars or newWord in closed_class_stop_words or newWord == ''):
        currentFrequency[newWord] = currentFrequency.get(newWord, 0) + 1

def readFromFile(abstractFile, type):
    accumulated = []
    rawText = abstractFile.read()
    lst = rawText.split(".I ")
    idx = 1
    while idx < len(lst):
        if type == "abstract":
            summary = lst[idx].split(".T")[1].split(".A")[1].split(".B")[1].split(".W")[1].lower().split()
        else:
            summary = lst[idx].split(".W")[1].lower().split()
        currentFrequency = dict()
        for word in summary:
            parseWord(word, currentFrequency)
        accumulated.append(currentFrequency)
        idx += 1
    return accumulated

def tfidf(list):
    totalDocuments = len(list)
    documentFrequency = dict() # number of documents a word appears in
    for doc in list:
        for word in doc:
            documentFrequency[word] = documentFrequency.get(word, 0) + 1
    count = 0
    for doc in list:
        for word in doc:
            idf = np.log(totalDocuments / documentFrequency[word])
            doc[word] = doc[word] * idf

def cosineSimilarity(queryList, abstractList):
    results = []
    for i, query in enumerate(queryList):
        currSection = []
        for j, abstract in enumerate(abstractList):
            if i + 1  == 1 and j + 1 == 304:
                # print(query, abstract)
                score = similarity(query, abstract, False)
                print(score)
            else:
                score = similarity(query, abstract, False)
            currSection.append([i + 1, j + 1, score])
        results.append(currSection)
    return results

def similarity(query, abstract, bool):
    queryScores = []
    abstractScores = []
    for word in query:
        queryScore = query[word]
        queryScores.append(queryScore)
        abstractScore = abstract.get(word, 0)
        abstractScores.append(abstractScore)
        if bool:
            print(word, queryScore, abstractScore)
    queryArray = np.array(queryScores)
    abstractArray = np.array(abstractScores)
    top = np.sum(abstractArray * queryArray)
    bot = np.sqrt(np.sum(abstractArray * abstractArray) * np.sum(queryArray * queryArray))
    if bool:
        print(queryArray, abstractArray)
        print(top, bot)
    return top / bot if bot != 0 else 0

def sortHelper(start, end, similarityScores):
    for i in range(start, end):
        min_idx = i
        for j in range(i + 1, end):
            if similarityScores[min_idx][2] > similarityScores[j][2]:
                min_idx = j
        similarityScores[i], similarityScores[min_idx] = similarityScores[min_idx], similarityScores[i]

def insertionSort(arr, start, end):
    # print("Insertion Sort", start, end)
    for i in range(start + 1, end): 
        key = arr[i]
        j = i-1
        while j >= 0 and key[2] > arr[j][2]:
            print("Comparing:", key, "with:", arr[j])
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def selectionSort(arr):
    needSwap = True
    while needSwap:
        needSwap = False
        for i in range(len(arr) - 1):
            if arr[i][2] < arr[i + 1][2]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                needSwap = True

def sortBySimilarity(similarityScores):
    for section in similarityScores:
        selectionSort(section)

def writeScoreToOutput(similarityScores, file):
    for query in similarityScores:
        for (queryID, abstractID, score) in query:
            line = "{0} {1} {2}\n".format(queryID, abstractID, score)
            file.write(line)

def main():
    # First Step: read from query file
    queryFile = open("Cranfield_collection_HW/cran.qry", "r")
    queryList = readFromFile(queryFile, "query")
    queryFile.close()

    # Second Step: read from document
    abstractFile = open("Cranfield_collection_HW/cran.all.1400", "r")
    abstractList = readFromFile(abstractFile, "abstract")
    abstractFile.close()

    # print(queryList)
    print("Query Len:", len(queryList))

    # print(abstractList)
    print("Abstract Len:", len(abstractList))

    # Third Step: calculate TF-IDF score
    tfidf(queryList)
    tfidf(abstractList)

    # Fourth Step: calculate cosine similarity between each query and each abstract
    similarityScores = cosineSimilarity(queryList, abstractList)
    # insertionSort(similarityScores)
    sortBySimilarity(similarityScores)
    # print(similarityScores)

    # Fifth Step: write scores to output file
    outputFile = open("outputFinal.txt", "w")
    writeScoreToOutput(similarityScores, outputFile)
    outputFile.close()


if __name__ == '__main__':
    main()
