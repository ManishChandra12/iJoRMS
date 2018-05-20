
def performanceMeasure(prediction):
    truePositive = {}
    falseNegative = {}
    falsePositive = {}
    trueNegative = {}

    truePositive['education'] = prediction['education'].count('education')
    falseNegative['education'] = len(prediction['education']) - truePositive['education']
    falsePositive['education'] = prediction['certification'].count('education') + prediction['skill'].count('education') + prediction['workExperience'].count('education')
    trueNegative['education'] = (len(prediction['certification']) + len(prediction['skill']) + len(prediction['workExperience'])) - falsePositive['education']

    truePositive['certification'] = prediction['certification'].count('certification')
    falseNegative['certification'] = len(prediction['certification']) - truePositive['certification']
    falsePositive['certification'] = prediction['education'].count('certification') + prediction['skill'].count('certification') + prediction['workExperience'].count('certification')
    trueNegative['certification'] = (len(prediction['education']) + len(prediction['skill']) + len(prediction['workExperience'])) - falsePositive['certification']

    truePositive['skill'] = prediction['skill'].count('skill')
    falseNegative['skill'] = len(prediction['skill']) - truePositive['skill']
    falsePositive['skill'] = prediction['education'].count('skill') + prediction['certification'].count('skill') + prediction['workExperience'].count('skill')
    trueNegative['skill'] = (len(prediction['education']) + len(prediction['certification']) + len(prediction['workExperience'])) - falsePositive['skill']

    truePositive['workExperience'] = prediction['workExperience'].count('workExperience')
    falseNegative['workExperience'] = len(prediction['workExperience']) - truePositive['workExperience']
    falsePositive['workExperience'] = prediction['education'].count('workExperience') + prediction['certification'].count('workExperience') + prediction['skill'].count('workExperience')
    trueNegative['workExperience'] = (len(prediction['education']) + len(prediction['certification']) + len(prediction['skill'])) - falsePositive['workExperience']


    accuracyEducation = (truePositive['education'] + trueNegative['education']) / (truePositive['education'] + trueNegative['education'] + falsePositive['education'] + falseNegative['education'])
    accuracyCertification = (truePositive['certification'] + trueNegative['certification']) / (truePositive['certification'] + trueNegative['certification'] + falsePositive['certification'] + falseNegative['certification'])
    accuracySkill = (truePositive['skill'] + trueNegative['skill']) / (truePositive['skill'] + trueNegative['skill'] + falsePositive['skill'] + falseNegative['skill'])
    accuracyWorkExperience = (truePositive['workExperience'] + trueNegative['workExperience']) / (truePositive['workExperience'] + trueNegative['workExperience'] + falsePositive['workExperience'] + falseNegative['workExperience'])

    precisionEducation = (truePositive['education']) / (truePositive['education'] + falsePositive['education'])
    precisionCertification = (truePositive['certification']) / (truePositive['certification'] + falsePositive['certification'])
    precisionSkill = (truePositive['skill']) / (truePositive['skill'] + falsePositive['skill'])
    precisionWorkExperience = (truePositive['workExperience']) / (truePositive['workExperience'] + falsePositive['workExperience'])

    recallEducation = (truePositive['education']) / (truePositive['education'] + falseNegative['education'])
    recallCertification = (truePositive['certification']) / (truePositive['certification'] + falseNegative['certification'])
    recallSkill = (truePositive['skill']) / (truePositive['skill'] + falseNegative['skill'])
    recallWorkExperience = (truePositive['workExperience']) / (truePositive['workExperience'] + falseNegative['workExperience'])

    fmeasureEducation = (2 * precisionEducation * recallEducation) / (precisionEducation + recallEducation)
    fmeasureCertification = (2 * precisionCertification * recallCertification) / (precisionCertification + recallCertification)
    fmeasureSkill = (2 * precisionSkill * recallSkill) / (precisionSkill + recallSkill)
    fmeasureWorkExperience = (2 * precisionWorkExperience * recallWorkExperience) / (precisionWorkExperience + recallWorkExperience)

    return truePositive, trueNegative, falsePositive, falseNegative, accuracyCertification, accuracyEducation, accuracySkill, accuracyWorkExperience, fmeasureCertification, fmeasureEducation, fmeasureSkill, fmeasureWorkExperience