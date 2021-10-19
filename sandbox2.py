# cran.all.1400 is the text document
# cran.qry is the query
# cranqrel is the answer key

import string 
import numpy as np
import re

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
    # invalidWhitespace = ['\n', '\t', '\r', '\f', '\v']
    # newWord = re.sub(r'[^\w\s]', '', word)
    # newWord = re.sub(r'[0-9\,.]+', '', newWord)
    newWord = re.sub(r'[^\w\s0-9\,.]*', '', word)
    if not(newWord.isnumeric() or newWord in invalidChars or newWord in closed_class_stop_words or newWord == ''):
        currentFrequency[newWord] = currentFrequency.get(newWord, 0) + 1

def create_qry_list(filename):
	ids = []
	queries_tf = []
	file = open(filename, 'r')
	file_text = file.read()
	data = file_text.split('.I ')
	for i in range(1, len(data)):
		strings = data[i].split('.W')
		id = int(strings[0])
		original_text = strings[1].lower().split()
		new_text = dict()
		for word in original_text:
			word = re.sub(r'[^\w\s]', '', word)
			word = re.sub(r'[0-9\,.]+', '', word)
			if word not in closed_class_stop_words and word != '':
				# check if word is in vector dict
				if word not in new_text:
					new_text[word] = 1
				else:
					new_text[word] += 1
		queries_tf.append(new_text)
		ids.append(id)
	return queries_tf

def create_abstract_list(filename):
	abstracts_tf = []
	abstract_ids = []
	file = open(filename, 'r')
	file_text = file.read()
	data = file_text.split('.I ')
	for i in range(1, len(data)):
		strings = data[i].split('.T')
		id = int(strings[0])
		abstract_ids.append(id)
		strings = strings[1].split('.A')
		title = strings[0]
		strings = strings[1].split('.B')
		bibliography = strings[0]
		strings = strings[1].split('.W')
		text = strings[1]
		original_text = text.split()
		new_text = dict()
		for word in original_text:
			word = re.sub(r'[^\w\s]', '', word)
			word = re.sub(r'[0-9\,.]+', '', word)
			if word not in closed_class_stop_words and word != '':
				# check if word is in vector dict
				if word not in new_text:
					new_text[word] = 1
				else:
					new_text[word] += 1
		abstracts_tf.append(new_text)
	return abstracts_tf

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

def calculate_tfidf(documents):
    num_documents_with_word = dict() # word: idf value
    for document in documents:
        for word in document:
            if word not in num_documents_with_word:
                num_documents_with_word[word] = 1
            else:
                num_documents_with_word[word] += 1
    total_num_documents = len(documents)
    count = 0
    for document in documents:
        for word in document:
            if word == "models":
                count += 1
            tf = document[word]
            idf = np.log(total_num_documents / num_documents_with_word[word])
            document[word] = tf * idf
    print(count)

def cosine_similarity(query, abstract, bool):
    query_vector = []
    abstract_vector = []
    for word in query:
        if bool:
            print(word, query[word], abstract.get(word, 0))
        query_vector.append(query[word])
        if word in abstract:
            abstract_vector.append(abstract[word])
        else:
            abstract_vector.append(0)
    abstract_vec = np.array(abstract_vector)
    query_vec = np.array(query_vector)
    # Calculate cosine similarity
    numerator = np.sum(abstract_vec * query_vec)
    denom1 = np.sum(abstract_vec * abstract_vec)
    denom2 = np.sum(query_vec * query_vec)
    if bool:
        print(query_vec, abstract_vec)
        print(numerator, np.sqrt(denom1 * denom2))
    if denom1 == 0 or denom2 == 0:
        return 0.0
    return numerator / np.sqrt(denom1 * denom2)

def cosineSimilarity(queryList, abstractList):
    results = []
    for i, query in enumerate(queryList):
        for j, abstract in enumerate(abstractList):
            
            
            if i + 1  == 1 and j + 1 == 304:
                # print(query, abstract)
                score = similarity(query, abstract, False)
                print(score)
            else:
                score = similarity(query, abstract, False)
            results.append([i + 1, j + 1, score])
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

def sortBySimilarity(similarityScores):
    # while not reached the end 
    #   find start and end indexes of current section
    #   sort on this section
    start = 0
    while start < len(similarityScores):
        # find end index of current section
        for end in range(start, len(similarityScores)):
            curr = similarityScores[end]
            if curr[2] != similarityScores[start][2]:
                break
        sortHelper(start, end, similarityScores)
        start = end 

def writeScoreToOutput(similarityScores, file):
    for (queryID, abstractID, score) in similarityScores:
        line = "{0} {1} {2}\n".format(queryID, abstractID, score)
        file.write(line)


def main():
    # First Step: read from query file
    queryFile = open("Cranfield_collection_HW/cran.qry", "r")
    queryList = readFromFile(queryFile, "query")
    queryFile.close()
    # queryList = create_qry_list("Cranfield_collection_HW/cran.qry")

    # Second Step: read from document
    abstractFile = open("Cranfield_collection_HW/cran.all.1400", "r")
    abstractList = readFromFile(abstractFile, "abstract")
    abstractFile.close()
    # abstractList = create_abstract_list("Cranfield_collection_HW/cran.all.1400")

    # print(queryList)
    # print(len(queryList))

    print(abstractList)
    print(len(abstractList))

    # Third Step: calculate TF-IDF score
    tfidf(queryList)
    tfidf(abstractList)

    # calculate_tfidf(queryList)
    # calculate_tfidf(abstractList)

    # Fourth Step: calculate cosine similarity between each query and each abstract
    # similarityScores = cosineSimilarity(queryList, abstractList)

    outputs = [] # query id, abstract id, cosine similarity
    for query_idx in range(len(queryList)):
        query_ouput = []
        query = queryList[query_idx]
        for abstract_idx in range(len(abstractList)):
            abstract = abstractList[abstract_idx]
            
            if query_idx + 1 == 1 and abstract_idx + 1 == 304: 
                # print(query, abstract)
                similarity = cosine_similarity(query, abstract, False)
                print(similarity)
                # print(abstract_ids)
            else:
                similarity = cosine_similarity(query, abstract, False)
        #     query_ouput.append([query_id, abstract_id, similarity])
        # outputs.append(query_ouput)


    # sortBySimilarity(similarityScores)
    # print(similarityScores)

    # Fifth Step: write scores to output file
    # outputFile = open("output.txt", "w")
    # writeScoreToOutput(similarityScores, outputFile)
    # outputFile.close()


if __name__ == '__main__':
    main()
