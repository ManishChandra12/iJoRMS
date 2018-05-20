import requests, ast
from xml.etree import ElementTree
from .InformationExtraction import getData
from ..models import JobApplicant



# userSkill = 'http://dbpedia.org/resource/Human_capital http://dbpedia.org/resource/Computer_virus http://dbpedia.org/resource/Spring_Framework http://dbpedia.org/resource/Virtuoso http://dbpedia.org/resource/Rugby_league_positions http://dbpedia.org/resource/Cascading_Style_Sheets http://dbpedia.org/resource/Agile_software_development http://dbpedia.org/resource/Technology http://dbpedia.org/resource/Web_application http://dbpedia.org/resource/JavaScript http://dbpedia.org/resource/MySQL http://dbpedia.org/resource/Model–view–controller http://dbpedia.org/resource/Sun_Microsystems http://dbpedia.org/resource/1984_Summer_Olympics http://dbpedia.org/resource/JavaServer_Pages http://dbpedia.org/resource/Cognition http://dbpedia.org/resource/Java_(programming_language'.split(' ')
#
#
# userWE = 'http://dbpedia.org/resource/University_of_Göttingen http://dbpedia.org/resource/Engineer http://dbpedia.org/resource/Software http://dbpedia.org/resource/Infosys http://dbpedia.org/resource/Internship http://dbpedia.org/resource/Academia http://dbpedia.org/resource/Computer_programming'.split(' ')
#
# userEducation = "education\nb.e.; in; computer; science\nanna; university; chennai".split('\n')
#
# userCertification = "".split('\n')
#
# jobSkill = 'Java, HTML, JavaScript, CSS, Spark framework, jQuery, React'.lower().split(',')
#
# jobWE = 'Java programming, Versioning control tools, Bamboo, RESTful, OSGi'.lower().split(',')
#
# jobEducation = "Master's in Computer Science".lower().split(',')
#
# jobCertification = "".lower().split(',')

def ranking(jobApplicant, applicant, job):
    # try:
        # userSkill = (applicant.skill_link).split(' ')
        # userWE = (applicant.work_experience_link).split(' ')
        # userEducation = (applicant.applicant_Edu).split('\n')
        # if(applicant.certification_link != None):
        #     userCertification = (applicant.certification_link).split('\n')
        # else:
        #     userCertification = [""]

    while(not applicant.applicant_Edu):
        continue
    jobSkill = (job.skills).lower().split(',')
    jobWE = (job.work_experience).lower().split(',')
    jobEducation = (job.degree).lower().split(',')
    if(job.certification):
        jobCertification = (job.certification).lower().split(',')
    else:
        jobCertification = [""]

    eduscore = matchEducation((applicant.applicant_Edu).split('\n'), jobEducation)
    print(eduscore)
    if(eduscore != -1):
        skillscore = matchSkill(applicant.skill_ontology, jobSkill, jobWE)
        print(skillscore)
        wescore = matchWE(applicant.work_experience_ontology, jobWE, jobSkill)
        print(wescore)
        certiscore = matchCertification(applicant.certification_link, jobCertification, jobSkill, jobWE)
        print(certiscore)
        jobApplicant.skillScore = (skillscore)
        jobApplicant.workExpScore = (wescore)
        jobApplicant.certificationScore = (certiscore)
        jobApplicant.educationScore = (eduscore)
    jobApplicant.save()
    allApplicants = JobApplicant.objects.filter(job=jobApplicant.job)
    sums = []
    for app in allApplicants:
        suma = 0
        suma += app.skillScore + app.workExpScore + app.educationScore + app.certificationScore
        sums.append(suma)
    print(sums)
    sorted_unique = sorted(set(sums), reverse=True)
    ordinal_map = {val: i for i, val in enumerate(sorted_unique, 1)}
    ordinals = [ordinal_map[val] for val in sums]
    print(ordinals)
    for ss in range(len(allApplicants)):
        allApplicants[ss].rank = ordinals[ss]
        allApplicants[ss].save()
    print("Out of Thread")
    return

    # except:
    #     print("Error Ranking")


def matchEducation(userEducation, jobEducation):
    degree = {0: '', 1: 'associate', 2: 'bachelor', 3: 'master', 4: 'phd'}
    highestDegree = 0
    jobDegree = -1
    # print(userEducation)
    for i in userEducation:
        if (i.startswith('b') and highestDegree < 2):
            # url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + i.split(';')[0]
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + i.split(';')[0]
            print("trying")
            response = requests.get(url)
            print("got it")
            tree = ElementTree.fromstring(response.content)
            if(len(tree) != 0):
                q1 = "SELECT ?description WHERE { " + "<" + tree[0][1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"
                data = getData(q1)['results']['bindings']
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        if pp.__contains__("degree"):
                            highestDegree = 2
        elif (i.startswith('m') and highestDegree < 3):
            # url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + i.split(';')[0]
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + i.split(';')[0]
            response = requests.get(url)
            tree = ElementTree.fromstring(response.content)
            if(len(tree) != 0):
                q1 = "SELECT ?description WHERE { " + "<" + tree[0][
                    1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"
                data = getData(q1)['results']['bindings']
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        if pp.__contains__("degree"):
                            highestDegree = 3
        elif (i.startswith('a') and highestDegree < 1):
            # url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + i.split(';')[0]
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + i.split(';')[0]
            response = requests.get(url)
            tree = ElementTree.fromstring(response.content)
            if(len(tree) != 0):
                q1 = "SELECT ?description WHERE { " + "<" + tree[0][
                    1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"
                data = getData(q1)['results']['bindings']
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        if pp.__contains__("degree"):
                            highestDegree = 1
        elif (i.startswith('p') or i == 'doctor' or i == 'doctorate') and highestDegree < 4:
            # url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + i.split(';')[0]
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + i.split(';')[0]
            response = requests.get(url)
            tree = ElementTree.fromstring(response.content)
            if(len(tree) != 0):
                q1 = "SELECT ?description WHERE { " + "<" + tree[0][
                    1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"
                data = getData(q1)['results']['bindings']
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        if pp.__contains__("degree"):
                            highestDegree = 4

    for jj in jobEducation:
        if (jj[0] == 'a' and jobDegree < 1):
            jobDegree = 1
        elif (jj[0] == 'b' and jobDegree < 2):
            jobDegree = 2
        elif (jj[0] == 'm' and jobDegree < 3):
            jobDegree = 3
        elif (jj[0] == 'p' or i == 'doctor' or i == 'doctorate') and jobDegree < 4:
            jobDegree = 4
    # print(jobDegree)
    # print(highestDegree)
    if(highestDegree < jobDegree):
        return -1
    else:
        return 1



def matchSkill(userSkillOntology, jobSkill, jobWE):
    score = 0
    ontology = ast.literal_eval(userSkillOntology)
    for j in jobSkill:
        # mm = j.split(' ')
        # for t in mm:
        for k in ontology:
            if (j in k['label']):
                score += 1
                break
            else:
                p = ''
                for nt in k['parent']:
                    p += nt + ' '
                if(j in p):
                    score += 0.5
                    break

    for j in jobWE:
        # mm = j.split(' ')
        # for t in mm:
        for k in ontology:
            if (j in k['label']):
                score += 0.25
                break
            else:
                p = ''
                for nt in k['parent']:
                    p += nt + ' '
                if(j in p):
                    score += 0.125
                    break
    return score


def matchWE(userWEOntology, jobWE, jobSkill):
    ontology = ast.literal_eval(userWEOntology)
    score = 0
    for j in jobWE:
        # mm = j.split(' ')
        # for t in mm:
        for k in ontology:
            if (j == k['label']):
                score += 1
                break
            else:
                p = ''
                for nt in k['parent']:
                    p += nt + ' '
                if(j in p):
                    score += 0.5
                    break

    for j in jobSkill:
        # mm = j.split(' ')
        # for t in mm:
        for k in ontology:
            if (j == k['label']):
                score += 1.5
                break
            else:
                p=''
                for nt in k['parent']:
                    p += nt + ' '
                if(j in p):
                    score += 1.25
                    break
    return score


def matchCertification(userCertificationLink, jobCertification, jobSkill, jobWE):
    score =0
    for i in jobCertification:
        # url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + i
        url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + i
        response = requests.get(url)
        tree = ElementTree.fromstring(response.content)
        if(len(tree) != 0):
            for j in userCertificationLink:
                if(j == tree[0][1].text):
                    score += 2

    for j in userCertificationLink:
        q1 = "SELECT ?description WHERE { " + "<" + j + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"
        data = getData(q1)['results']['bindings']
        if (len(data) != 0):
            if (data[0].keys().__contains__('description')):
                pp = data[0]['description']['value'].lower()
                for sk in jobSkill:
                    if pp.__contains__(sk):
                        score += 0.25
                for we in jobWE:
                    if pp.__contains__(we):
                        score += 0.25

    return score
