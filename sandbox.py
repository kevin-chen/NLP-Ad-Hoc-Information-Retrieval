# cran.all.1400 is the text document
# cran.qry is the query
# cranqrel is the answer key

# Second Step: read from document

import string 

def parseQueryLine(splits):
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
        if word.isnumeric() or word in invalidChars or word in closed_class_stop_words:
            splits.remove(word)
    return splits

def readFromQuery(queryFile):
    currentQueryList = []
    accumulatedQueries = []

    line = queryFile.readline()
    isReadingQuery = False
    
    while line != None:
        splits = line.strip().split(" ")
        if splits[0] == ".W": # start of new query
            isReadingQuery = True
        elif (splits[0] == ".I" or splits[0] == "") and len(currentQueryList) != 0:
            isReadingQuery = False
            accumulatedQueries.append(currentQueryList)
            currentQueryList = []
            if splits[0] == "":
                break
        elif isReadingQuery:
            # loop through array of strings and return list of valid query words
            validWords = parseQueryLine(splits)
            currentQueryList.extend(validWords)
        line = queryFile.readline()
    
    return accumulatedQueries

def main():
    # First Step: read from query file
    queryFile = open("Cranfield_collection_HW/cran.qry")
    print(len(readFromQuery(queryFile)))
    queryFile.close()


if __name__ == '__main__':
    main()
