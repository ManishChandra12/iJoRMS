from .Dataset import getAsList
import csv
import math


def sentenceClassifierNB(trainingSet, testSet):   #Naive Bayes classifier
    hashtable, lengths = naiveBayesTrain(trainingSet)
    predictions, prob = getPredictions(hashtable, lengths, testSet)
    return predictions, prob
    # print(sorted(hashtable.items(), key = operator.itemgetter(1), reverse = True))


def naiveBayesTrain(trainingSet):
    hashtable, lengths = generateHash(trainingSet)
    return hashtable, lengths


def generateHash(trainingSet):     #generate hash table of probabilities
    education, certification, workExperience, skill =  getAsList(trainingSet)
    vocabEducation = list(set(education))
    vocabCertification = list(set(certification))
    vocabWorkExperience = list(set(workExperience))
    vocabSkill = list(set(skill))
    total = len(vocabCertification) + len(vocabSkill) + len(vocabWorkExperience) + len(vocabEducation)  #cardinality of vocabulary set

    hashTable = {}    #hashtable of probabilities generated below with add-1 laplace smoothing
    for i in vocabCertification:
        hashTable[tuple([i,'certification'])] = (sum(1 for p in certification if p == i) + 1) / (len(certification)+(total))
    for i in vocabEducation:
        hashTable[tuple([i,'education'])] = (sum(1 for p in education if p == i)+1) / (len(education)+(total))
    for i in vocabSkill:
        hashTable[tuple([i,'skill'])] = (sum(1 for p in skill if p == i)+1) / (len(skill)+(total))
    for i in vocabWorkExperience:
        hashTable[tuple([i,'workExperience'])] = (sum(1 for p in workExperience if p == i)+1) / (len(workExperience)+(total))

    hashTable['certification'] = 0.25    #considering equiprobable class
    hashTable['education'] = 0.25
    hashTable['skill'] = 0.25
    hashTable['workExperience'] = 0.25
    lengths = {'certification': len(certification), 'education': len(education), 'skill': len(skill), 'workExperience': len(workExperience), 'total': total}  #number of words in each class

    # lenDataset = len(certification)+len(education)+len(skill)+len(workExperience) #Yields lesser accuracy than equiprobable assumption
    # probCertification = len(certification) / lenDataset
    # probEducation = len(education) / lenDataset
    # probSkill = len(skill) / lenDataset
    # probWorkExperience = len(workExperience) / lenDataset
    # hashTable['certification'] = probCertification
    # hashTable['education'] = probEducation
    # hashTable['skill'] = probSkill
    # hashTable['workExperience'] = probWorkExperience
    # storeModel(hashTable)
    # storeLengths(lengths)
    return hashTable, lengths

# def storeLengths(lengths):
#     with open('Lengths.csv','w') as out:
#         writer = csv.writer(out)
#         for entry in lengths:
#             writer.writerow([entry, lengths[entry]])
#     out.close()

# def storeModel(hashTable):
#     with open ('NaiveBayesModel.csv','w') as out:
#         writer = csv.writer(out)
#         for entry in hashTable:
#             writer.writerow([entry, hashTable[entry]])


def getPredictions(hashtable, lengths, testSet):     #get predictions for all the sentences
    predictions = {}
    prob = {}
    predictionsCertification = []
    probCertification = []
    predictionsEducation = []
    probEducation = []
    predictionsSkill = []
    probSkill = []
    predictionsWorkExperience = []
    probWorkExperience = []

    for i in testSet['certification']:
        if(len(i) != 0):
            result, probab = predict(hashtable, lengths, i)
            predictionsCertification.append(result)
            probCertification.append(probab)
    predictions['certification'] = predictionsCertification
    prob['certification'] = probCertification

    for i in testSet['education']:
        if(len(i) != 0):
            result, probab = predict(hashtable, lengths, i)
            predictionsEducation.append(result)
            probEducation.append(probab)
    predictions['education'] = predictionsEducation
    prob['education'] = probEducation

    for i in testSet['skill']:
        if(len(i) != 0):
            result, probab = predict(hashtable, lengths, i)
            predictionsSkill.append(result)
            probSkill.append(probab)
            if result == 'workExperience':
                print(i)
    predictions['skill'] = predictionsSkill
    prob['skill'] = probSkill


    for i in testSet['workExperience']:
        if(len(i) != 0):
            result, probab = predict(hashtable, lengths, i)
            predictionsWorkExperience.append(result)
            probWorkExperience.append(probab)
    predictions['workExperience'] = predictionsWorkExperience
    prob['workExperience'] = probWorkExperience

    return predictions, prob


def predict(hashtable, lengths, inVector):      #prediction for one sentence
    probabilities = calculateClassProbabilities(hashtable, lengths, inVector)
    # if (len(set(list(probabilities.values()))) == 1):
    #     return 'Other', 0
    if(probabilities['certification']-(math.log10(hashtable['certification'])) == probabilities['education']-(math.log10(hashtable['education'])) and probabilities['certification']-(math.log10(hashtable['certification'])) == probabilities['skill']-(math.log10(hashtable['skill'])) and probabilities['certification']-(math.log10(hashtable['certification'])) == probabilities['workExperience']-(math.log10(hashtable['workExperience']))):
        return 'Other', 0

    bestLabel, bestProb = None, -1
    for classValue, probability in list(probabilities.items()):
        if (bestLabel is None or probability > bestProb):
            bestProb = probability
            bestLabel = classValue


    return bestLabel, bestProb


def calculateClassProbabilities(hashtable, lengths, inVector):  #calculation of probabilities that the sentence belongs to each of the four classes
    probabilities = {}
    for cls in ['certification', 'education', 'skill', 'workExperience']:
        probabilities[cls] = (math.log10(hashtable[cls]))
        for i in inVector:
            if((i, cls) in hashtable.keys()):
                probabilities[cls] += (math.log10(hashtable[(i, cls)]))
            else:   #handling unknown words, i.e., those that are not seen in training set
                # probabilities[cls] *= (1 / (lengths[cls] + lengths['total'] + 1))
                probabilities[cls] += (math.log10((1 / (lengths['total'] + 1))))
    return probabilities