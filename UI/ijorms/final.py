# from jnius import autoclass # Import the Java classes we are going to need
import tika
tika.initVM()
from tika import parser
# from nltk.tag import StanfordNERTagger
import copy
from ast import literal_eval
from .Dataset import *
from .NaiveBayes import sentenceClassifierNB, generateHash, predict
from .TfIdf import tfidf, calculateIdfWeight, calculateTfWeight
from .PerformanceMeasure import performanceMeasure
from .InformationExtraction import extractSkills, extractWorkExperience, extractEducation, extractCertification
from .ontology import creatOntology, getValues
from .bagging import sentenceClassifierBag, calculateBagPerformanceMeasure


def classifiers():
    data = readDataset()
    splitRatio = 0.1
    splittedDataset = tenChunks(copy.deepcopy(data), splitRatio)

    totalTruePositiveNB = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalTrueNegativeNB = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalFalsePositiveNB = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalFalseNegativeNB = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}

    totalFmeasureNBCertification = 0
    totalFmeasureNBEducation = 0
    totalFmeasureNBSkill = 0
    totalFmeasureNBWorkExperience = 0

    totalAccuracyNBCertification = 0
    totalAccuracyNBEducation = 0
    totalAccuracyNBSkill = 0
    totalAccuracyNBWorkExperience = 0

    totalTruePositiveTfIdf = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalTrueNegativeTfIdf = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalFalsePositiveTfIdf = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalFalseNegativeTfIdf = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}

    totalFmeasureTfIdfCertification = 0
    totalFmeasureTfIdfEducation = 0
    totalFmeasureTfIdfSkill = 0
    totalFmeasureTfIdfWorkExperience = 0

    totalAccuracyTfIdfCertification = 0
    totalAccuracyTfIdfEducation = 0
    totalAccuracyTfIdfSkill = 0
    totalAccuracyTfIdfWorkExperience = 0

    # totalFmeasureBagCertification = 0
    # totalFmeasureBagEducation = 0
    # totalFmeasureBagSkill = 0
    # totalFmeasureBagWorkExperience = 0

    for r in range(10):
        trainingSet = {'education': [], 'workExperience': [], 'skill': [], 'certification': []}
        testSet = splittedDataset[r]
        for j in list(set(range(0, 9)) - {r}):
            trainingSet['education'].extend(splittedDataset[j]['education'])
            trainingSet['workExperience'].extend(splittedDataset[j]['workExperience'])
            trainingSet['skill'].extend(splittedDataset[j]['skill'])
            trainingSet['certification'].extend(splittedDataset[j]['certification'])

        NBPrediction, NBProbability = sentenceClassifierNB(copy.deepcopy(trainingSet), copy.deepcopy(testSet))
        truePositiveNB, trueNegativeNB, falsePositiveNB, falseNegativeNB, accuracyNBCertification, accuracyNBEducation, accuracyNBSkill, accuracyNBWorkExperience, fmeasureNBCertification, fmeasureNBEducation, fmeasureNBSkill, fmeasureNBWorkExperience = performanceMeasure(NBPrediction)

        for i in ['certification', 'education', 'skill', 'workExperience']:
            totalTruePositiveNB[i] += truePositiveNB[i]
            totalTrueNegativeNB[i] += trueNegativeNB[i]
            totalFalsePositiveNB[i] += falsePositiveNB[i]
            totalFalseNegativeNB[i] += falseNegativeNB[i]

        totalFmeasureNBCertification += fmeasureNBCertification
        totalFmeasureNBEducation += fmeasureNBEducation
        totalFmeasureNBSkill += fmeasureNBSkill
        totalFmeasureNBWorkExperience += fmeasureNBWorkExperience
        totalAccuracyNBCertification += accuracyNBCertification
        totalAccuracyNBEducation += accuracyNBEducation
        totalAccuracyNBSkill += accuracyNBSkill
        totalAccuracyNBWorkExperience += accuracyNBWorkExperience

        TfIdfPrediction, TfIdfWeight = tfidf(copy.deepcopy(trainingSet), copy.deepcopy(testSet))
        truePositiveTfIdf, trueNegativeTfIdf, falsePositiveTfIdf, falseNegativeTfIdf, accuracyTfIdfCertification, accuracyTfIdfEducation, accuracyTfIdfSkill, accuracyTfIdfWorkExperience, fmeasureTfIdfCertification, fmeasureTfIdfEducation, fmeasureTfIdfSkill, fmeasureTfIdfWorkExperience = performanceMeasure(TfIdfPrediction)

        for i in ['certification', 'education', 'skill', 'workExperience']:
            totalTruePositiveTfIdf[i] += truePositiveTfIdf[i]
            totalTrueNegativeTfIdf[i] += trueNegativeTfIdf[i]
            totalFalsePositiveTfIdf[i] += falsePositiveTfIdf[i]
            totalFalseNegativeTfIdf[i] += falseNegativeTfIdf[i]

        totalFmeasureTfIdfCertification += fmeasureTfIdfCertification
        totalFmeasureTfIdfEducation += fmeasureTfIdfEducation
        totalFmeasureTfIdfSkill += fmeasureTfIdfSkill
        totalFmeasureTfIdfWorkExperience += fmeasureTfIdfWorkExperience
        totalAccuracyTfIdfCertification += accuracyTfIdfCertification
        totalAccuracyTfIdfEducation += accuracyTfIdfEducation
        totalAccuracyTfIdfSkill += accuracyTfIdfSkill
        totalAccuracyTfIdfWorkExperience += accuracyTfIdfWorkExperience

        # BagPrediction, BagProbability = sentenceClassifierBag(copy.deepcopy(trainingSet), copy.deepcopy(testSet))
        # fmeasureBagCertification, fmeasureBagEducation, fmeasureBagSkill, fmeasureBagWorkExperience = calculateBagPerformanceMeasure(BagPrediction)
        # totalFmeasureBagCertification += fmeasureBagCertification
        # totalFmeasureBagEducation += fmeasureBagEducation
        # totalFmeasureBagSkill += fmeasureBagSkill
        # totalFmeasureBagWorkExperience += fmeasureBagWorkExperience

    finalFmeasureNBCertification = totalFmeasureNBCertification * 0.1
    finalFmeasureNBEducation = totalFmeasureNBEducation * 0.1
    finalFmeasureNBSkill = totalFmeasureNBSkill * 0.1
    finalFmeasureNBWorkExperience = totalFmeasureNBWorkExperience * 0.1

    finalAccuracyNBCertification = totalAccuracyNBCertification * 0.1
    finalAccuracyNBEducation = totalAccuracyNBEducation * 0.1
    finalAccuracyNBSkill = totalAccuracyNBSkill * 0.1
    finalAccuracyNBWorkExperience = totalAccuracyNBWorkExperience * 0.1

    finalFmeasureTfIdfCertification = totalFmeasureTfIdfCertification * 0.1
    finalFmeasureTfIdfEducation = totalFmeasureTfIdfEducation * 0.1
    finalFmeasureTfIdfSkill = totalFmeasureTfIdfSkill * 0.1
    finalFmeasureTfIdfWorkExperience = totalFmeasureTfIdfWorkExperience * 0.1

    finalAccuracyTfIdfCertification = totalAccuracyTfIdfCertification * 0.1
    finalAccuracyTfIdfEducation = totalAccuracyTfIdfEducation * 0.1
    finalAccuracyTfIdfSkill = totalAccuracyTfIdfSkill * 0.1
    finalAccuracyTfIdfWorkExperience = totalAccuracyTfIdfWorkExperience * 0.1
    # print('')
    # finalFmeasureBagCertification = totalFmeasureBagCertification * 0.1
    # finalFmeasureBagEducation = totalFmeasureBagEducation * 0.1
    # finalFmeasureBagSkill = totalFmeasureBagSkill * 0.1
    # finalFmeasureBagWorkExperience = totalFmeasureBagWorkExperience * 0.1


def NaiveBayesModel():
    data = readDataset()
    generateHash(data)


def TFModel():
    data = readDataset()
    calculateTfWeight(data)
    calculateIdfWeight(data)


def getText(filename):       # get plain text using Apache Tika
    # Tika = autoclass('org.apache.tika.Tika')
    # Metadata = autoclass('org.apache.tika.metadata.Metadata')
    # FileInputStream = autoclass('java.io.FileInputStream')

    # tika = Tika()
    # meta = Metadata()
    # text = tika.parseToString(FileInputStream(filename), meta)
    parsed = parser.from_file(filename)
    text = parsed["content"]
    return text


def preprocess(content):   #preprocess the test resume to get tokens
    c = content.lower()
    c = c.replace('.\n', '\n')
    for punc in [',',':','|','/',';','-','–','—','(',')']:
        c = c.replace(punc,' ')
    c = c.split('\n')
    c = list(filter(lambda x: x != '', c))
    tokens = []
    for i in c:
        token = i.split(' ')
        token = list(filter(lambda x: x != '', token))
        tokens.append(token)

    # for j in range(len(tokens)):
    #     tokens[j] = [w for w in tokens[j] if w not in stopwords.words('english')]
    return tokens            #improve the preprocessing: remove () maybe...


def loadAll():
    hashTable = {}
    lengths = {}
    Idf = {}
    tfCertification = {}
    tfEducation = {}
    tfSkill = {}
    tfWorkExperience = {}
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'NaiveBayesModel.csv'), 'r') as inp:
        reader = list(csv.reader(inp))
        # i[0] kina gareko vanda csv file ma skill, workexp, etc ko chhutai rakheko chha, aru ko vane tuple ma rakehko
        # chha, like so '(keyword, class)', prob_value ani hashtable ma rakhne ho
        for i in reader:
            if (i[0] == 'skill' or i[0] == 'workExperience' or i[0] == 'education' or i[0] == 'certification'):
                hashTable[i[0]] = float(i[1])
            else:
                hashTable[literal_eval(i[0])] = float(i[1]) #literal eval le chai tuple mai rakhidinchha

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Lengths.csv'), 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            lengths[i[0]] = float(i[1])

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'IDFModel.csv'), 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            Idf[i[0]] = float(i[1])

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'TFCertificationModel.csv'), 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            tfCertification[i[0]] = float(i[1])

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'TFEducationModel.csv'), 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            tfEducation[i[0]] = float(i[1])

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'TFSkillModel.csv'), 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            tfSkill[i[0]] = float(i[1])

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'TFExperienceModel.csv'), 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            tfWorkExperience[i[0]] = float(i[1])

    return hashTable, lengths, Idf, tfCertification, tfEducation, tfSkill, tfWorkExperience


def main(filename):
    train = False
    if train:
        NaiveBayesModel()
        TFModel()
        classifiers()

    content = getText(filename)
    tokens = preprocess(content)
    # hash table ma chai featture/class ko probability rakhya chha
    # length vaneko chai kun class ma kati ota item item tesko detail
    # Idf vaneko harek vocab ko idf value store garchha
    # tcertification certification vanne class ma vocab ko tf value
    hashTable, lengths, Idf, tfCertification, tfEducation, tfSkill, tfWorkExperience = loadAll()
    result = {'Other':[], 'certification': [], 'education': [], 'skill': [], 'workExperience': []}
    for i in tokens:
        label, prob = predict(hashTable, lengths, i)
        result[label].append(i)
        #label, prob le chai resume ko harek paragraph lai classify gareko chha
    # ontology = creatOntology()
    # ont = getValues(ontology)
    IEskills, ontologySkill = extractSkills(result['skill'])  ##information extract garda gardai ontology pani banai rako chha
    print(IEskills)
    IEWorkExperience, ontologyWorkExperience = extractWorkExperience(result['workExperience'])
    print(IEWorkExperience)
    IEeducation = extractEducation(result['education'])
    print(IEeducation)
    IEcertification, linksCertification = extractCertification(result['certification'])
    print(IEcertification)
    return IEskills, ontologySkill, IEWorkExperience, ontologyWorkExperience, IEeducation, IEcertification, linksCertification


if __name__ == '__main__':
    main()