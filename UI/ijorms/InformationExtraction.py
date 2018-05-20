import nltk
import requests
from xml.etree import ElementTree
import sys
from SPARQLWrapper import SPARQLWrapper, JSON


def getData(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()

# def extractSkills(skills):
#     IEskills = []
#     news = []
#     for i in skills:
#         IEskill = []
#         new = []
#         p = nltk.pos_tag(i)
#         for j in range(len(p)):
#             if p[j][1] == 'NN' or p[j][1] == 'NNS' or p[j][1] == 'NNP' or p[j][1] == 'NNPS':
#                 IEskill.append(p[j][0])
#                 if j < len(p) - 2 and (
#                                 p[j + 1][1] == 'NN' or p[j + 1][1] == 'NNS' or p[j + 1][1] == 'NNP' or p[j + 1][
#                     1] == 'NNPS') and (
#                                 p[j + 2][1] == 'NN' or p[j + 2][1] == 'NNS' or p[j + 2][1] == 'NNP' or p[j + 2][
#                     1] == 'NNPS'):
#                     new.append(p[j][0] + ' ' + p[j + 1][0] + ' ' + p[j + 2][0])
#                 if j < len(p) - 1 and (
#                                 p[j + 1][1] == 'NN' or p[j + 1][1] == 'NNS' or p[j + 1][1] == 'NNP' or p[j + 1][
#                     1] == 'NNPS'):
#                     new.append(p[j][0] + ' ' + p[j + 1][0])
#         IEskills.append(IEskill)
#         news.append(new)
#     IEskills += news
#     # print(IEskills)
#     #
#     # finals = []
#     # for j in IEskills:
#     #     final = []
#     #     for k in j:
#     #         if (ont.__contains__(k)):
#     #             final.append(k)
#     #     finals.append(final)
#     # print(finals)
#     seed = ["programming", "language", "interface", "library", "operating system"]
#     finals = []
#     done = False
#     for i in IEskills:
#         final = []
#         for j in i:
#             url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + j
#             response = requests.get(url)
#             tree = ElementTree.fromstring(response.content)
#             for iii in range(len(tree)):
#                 # print(j, tree[i][2].text)
#                 if(tree[iii][2].text != None):
#                     pp = (tree[iii][2].text).lower()
#                     for se in seed:
#                         if pp.__contains__(se):
#                             final.append(j)
#                             done = True
#                             break
#                     if (done == True):
#                         done = False
#                         break
#         # if (len(final) != 0):
#         finals.append(final)
#     for ii in range(len(news)):
#         for dup in finals[ii + len(news)]:
#             if finals[ii].__contains__(dup.split(' ')[0]):
#                 ind = finals[ii].index(dup.split(' ')[0])
#                 if len(dup.split(' ')) == 3 and ind < len(finals[ii]) - 2 and finals[ii][ind + 1] == dup.split(' ')[
#                     1] and finals[ii][ind + 2] == dup.split(' ')[2]:
#                     finals[ii].pop(ind)
#                     finals[ii].pop(ind)
#                     finals[ii].pop(ind)
#                     finals[ii].insert(ind, dup)
#                     finals[ii + len(news)].pop(finals[ii + len(news)].index(dup) + 1)
#                     finals[ii + len(news)].pop(finals[ii + len(news)].index(dup) + 1)
#                 elif ind < len(finals[ii]) - 1 and finals[ii][ind + 1] == dup.split(' ')[1]:
#                     finals[ii].pop(ind)
#                     finals[ii].pop(ind)
#                     finals[ii].insert(ind, dup)
#                 else:
#                     finals[ii].pop(ind)
#                     finals[ii].insert(ind, dup)
#     finalest = finals[0:len(news)]
#     IEs = []
#     for i in finalest:
#         if len(i) != 0:
#             IEs.append(i)
#     # print(finalest)
#     return IEs
#     # print(finals)
#
# def extractWorkExperience(workExperience):
#     IEWorkExperiences = []
#     news = []
#     for i in workExperience:
#         IEWorkExperience = []
#         new = []
#         p = nltk.pos_tag(i)
#         # print(p)
#         for j in range(len(p)):
#             if p[j][1] == 'NN' or p[j][1] == 'NNS' or p[j][1] == 'NNP' or p[j][1] == 'NNPS':
#                 IEWorkExperience.append(p[j][0])
#                 if j < len(p) - 2 and (
#                                 p[j + 1][1] == 'NN' or p[j + 1][1] == 'NNS' or p[j + 1][1] == 'NNP' or p[j + 1][
#                     1] == 'NNPS') and (
#                                 p[j + 2][1] == 'NN' or p[j + 2][1] == 'NNS' or p[j + 2][1] == 'NNP' or p[j + 2][
#                     1] == 'NNPS'):
#                     new.append(p[j][0] + ' ' + p[j + 1][0] + ' ' + p[j + 2][0])
#                 if j < len(p) - 1 and (
#                                 p[j + 1][1] == 'NN' or p[j + 1][1] == 'NNS' or p[j + 1][1] == 'NNP' or p[j + 1][
#                     1] == 'NNPS'):
#                     new.append(p[j][0] + ' ' + p[j + 1][0])
#         IEWorkExperiences.append(IEWorkExperience)
#         # if (len(new) != 0):
#         news.append(new)
#     IEWorkExperiences += (news)
#     # print(IEWorkExperiences)
#     # print(IEWorkExperiences)
#
#     seed = ["programming", "language", "interface", "library", "operating system", "professional", "profession"]
#     finals = []
#     done = False
#     for i in IEWorkExperiences:
#         final = []
#         for j in i:
#             url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + j
#             response = requests.get(url)
#             tree = ElementTree.fromstring(response.content)
#             for iii in range(len(tree)):
#                 # print(j, tree[i][1].text)
#                 if (tree[iii][2].text != None):
#                     pp = (tree[iii][2].text).lower()
#                     for se in seed:
#                         if pp.__contains__(se):
#                             final.append(j)
#                             done = True
#                             break
#                     if (done == True):
#                         done = False
#                         break
#         # if (len(final) != 0):
#         finals.append(final)
#     for ii in range(len(news)):
#         for dup in finals[ii + len(news)]:
#             if finals[ii].__contains__(dup.split(' ')[0]):
#                 ind = finals[ii].index(dup.split(' ')[0])
#                 if len(dup.split(' ')) == 3 and ind < len(finals[ii]) - 2 and finals[ii][ind + 1] == dup.split(' ')[
#                     1] and finals[ii][ind + 2] == dup.split(' ')[2]:
#                     finals[ii].pop(ind)
#                     finals[ii].pop(ind)
#                     finals[ii].pop(ind)
#                     finals[ii].insert(ind, dup)
#                     finals[ii + len(news)].pop(finals[ii + len(news)].index(dup) + 1)
#                     finals[ii + len(news)].pop(finals[ii + len(news)].index(dup) + 1)
#                 elif ind < len(finals[ii]) - 1 and finals[ii][ind + 1] == dup.split(' ')[1]:
#                     finals[ii].pop(ind)
#                     finals[ii].pop(ind)
#                     finals[ii].insert(ind, dup)
#                 else:
#                     finals[ii].pop(ind)
#                     finals[ii].insert(ind, dup)
#     finalest = finals[0:len(news)]
#     IEw = []
#     for i in finalest:
#         if len(i) != 0:
#             IEw.append(i)
#     # print(finalest)
#     return IEw
#
# def extractEducation(education):
#     seed = ["degree", "university"]
#     finals = []
#     done = False
#     for i in education:
#         new = []
#         p = nltk.pos_tag(i)
#         for j in range(len(p)):
#             if (p[j][1] != 'CD'):
#                 new.append(p[j][0])
#         # strng = ''
#         # for j in new:
#         #     strng += j + ' '
#         # print(strng.strip())
#         for strng in new:
#             url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + strng
#             response = requests.get(url)
#             tree = ElementTree.fromstring(response.content)
#             for k in range(len(tree)):
#                 # print(j, tree[k][1].text)
#                 if (tree[k][2].text != None):
#                     pp = tree[k][2].text.lower()
#                     for se in seed:
#                         if pp.__contains__(se):
#                             finals.append(i)
#                             done = True
#                             break
#                     if (done == True):
#                         break
#             if (done == True):
#                 done = False
#                 break
#     return finals
#
# def extractCertification(certification):
#     seed = ["certification"]
#     finals = []
#     done = False
#     for i in certification:
#         new = []
#         p = nltk.pos_tag(i)
#         for j in range(len(p)):
#             if (p[j][1] != 'CD'):
#                 new.append(p[j][0])
#         strng = ''
#         for j in new:
#             strng += j + ' '
#         url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + strng.strip()
#         response = requests.get(url)
#         tree = ElementTree.fromstring(response.content)
#         for k in range(len(tree)):
#             # print(j, tree[k][1].text)
#             if (tree[k][2].text != None):
#                 pp = tree[k][2].text.lower()
#                 for se in seed:
#                     if pp.__contains__(se):
#                         finals.append(i)
#                         done = True
#                         break
#                 if (done == True):
#                     done = False
#                     break
#     return finals




def extractSkills(skills):
    IEskills = []
    news = []
    for i in skills:
        IEskill = []
        new = []
        # skills ma chai [['token1', 'token2, .........],[...........]]
        # p ms chai harek token ko tagged garera rakhinchha, tuple ma rakhinchha
        # NNx vaneko nouns, JJ vaneko adjective, CD vaneko number
        # tyo tala ko if j<len(p).... vanne wala part ma chai two or more NNx sangai aaako chha ki chhaina vanera hereko
        # for eg. Software Developer, tesko token haru chai DBpedia ma pathauna news vanne ma rakheko
        p = nltk.pos_tag(i)
        for j in range(len(p)):
            if p[j][1] == 'NN' or p[j][1] == 'NNS' or p[j][1] == 'NNP' or p[j][1] == 'NNPS' or p[j][1] == 'JJ':
                IEskill.append(p[j][0])
                if j < len(p) - 2 and (p[j + 1][1] == 'NN' or p[j + 1][1] == 'NNS' or p[j + 1][1] == 'NNP' or p[j + 1][1] == 'NNPS') and (p[j + 2][1] == 'NN' or p[j + 2][1] == 'NNS' or p[j + 2][1] == 'NNP' or p[j + 2][1] == 'NNPS'):
                    new.append(p[j][0] + ' ' + p[j + 1][0] + ' ' + p[j + 2][0])
                if j < len(p) - 1 and (p[j + 1][1] == 'NN' or p[j + 1][1] == 'NNS' or p[j + 1][1] == 'NNP' or p[j + 1][1] == 'NNPS'):
                    new.append(p[j][0] + ' ' + p[j + 1][0])
        IEskills.append(IEskill)
        news.append(new)
    IEskills += news
    #
    # finals = []
    # for j in IEskills:
    #     final = []
    #     for k in j:
    #         if (ont.__contains__(k)):
    #             final.append(k)
    #     finals.append(final)
    # print(finals)
    seed = ["software", "programming", "language", "network", "security", "computer", "framework", "interface", "library", "operating system", "skill"]
    finals = []
    links = []
    done = False
    for i in IEskills:
        final = []
        for j in i:
            # url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + j
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + j
            response = requests.get(url)
            tree = ElementTree.fromstring(response.content)
            for iii in range(len(tree)):
                # print(j, tree[iii][1].text)
                q1 = "SELECT ?description WHERE { " + "<" + tree[iii][1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"

                data = getData(q1)['results']['bindings']   #json ma reply aauchha, tesma results vitra ko bindings ko value leko
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        for se in seed:
                            if pp.__contains__(se):
                                final.append(j)
                                print(j)
                                links.append(tree[iii][1].text)
                                done = True
                                break
                if (done == True):
                    done = False
                    break
        # if (len(final) != 0):
        finals.append(final)  #finals ma chai IESkills bata nachaine lai hataidiyo, eg software, developer chhitta chhuttai vako lai hatayera
        ## software developer ek sath vakako lai rakheko
    for ii in range(len(news)):
        for dup in finals[ii+len(news)]:
            if finals[ii].__contains__(dup.split(' ')[0]):
                ind = finals[ii].index(dup.split(' ')[0])
                if len(dup.split(' ')) == 3 and ind < len(finals[ii])-2 and finals[ii][ind+1] == dup.split(' ')[1] and finals[ii][ind+2] == dup.split(' ')[2]:
                    finals[ii].pop(ind)
                    finals[ii].pop(ind)
                    finals[ii].pop(ind)
                    finals[ii].insert(ind, dup)
                    finals[ii+len(news)].pop(finals[ii+len(news)].index(dup)+1)
                    finals[ii + len(news)].pop(finals[ii + len(news)].index(dup) + 1)
                elif ind < len(finals[ii])-1 and finals[ii][ind+1] == dup.split(' ')[1]:
                    finals[ii].pop(ind)
                    finals[ii].pop(ind)
                    finals[ii].insert(ind, dup)
                else:
                    finals[ii].pop(ind)
                    finals[ii].insert(ind, dup)
    finalest = finals[0:len(news)]
    IEs = []
    for i in finalest:
        if len(i) != 0:
            temp = list(set(i))
            IEs.append(temp)
    # print(finalest)

    ontologySkill = []
    for i in list(set(links)):
        one = {'parent': []}
        q1 = "SELECT ?label ?parent WHERE {" + "<" + i + ">" + " rdfs:label ?label. " + "<" + i + ">" + "dct:subject ?parent. filter langMatches(lang(?label), 'EN')}"
        data1 = getData(q1)['results']['bindings']
        if (len(data1) != 0):
            one['label'] = data1[0]['label']['value'].lower()
            for result in data1:
                # print(result['label']['value'], result['parent']['value'])
                q2 = "SELECT ?label WHERE {" + "<" + result['parent'][
                    'value'] + ">" + " rdfs:label ?label. filter langMatches(lang(?label), 'EN')}"
                data2 = getData(q2)['results']['bindings']
                one['parent'].append(data2[0]['label']['value'].lower())
                # print(data2[0]['label']['value'])
        else:
            one['label'] = i.split('/')[-1]
        print (one)
        ontologySkill.append(one)
    return IEs, ontologySkill  # IEs ma lastfinal skills haru chha, arko chai ontology ho
    ## ontology ma chia list vitra dictionary ho, key ma (label, parent) value ma details ma baschha
    # print(finals)


def extractWorkExperience(workExperience):
    IEWorkExperiences = []
    news = []
    for i in workExperience:
        IEWorkExperience = []
        new = []
        p = nltk.pos_tag(i)
        # print(p)
        for j in range(len(p)):
            if p[j][1] == 'NN' or p[j][1] == 'NNS' or p[j][1] == 'NNP' or p[j][1] == 'NNPS' or p[j][1] == 'JJ':
                IEWorkExperience.append(p[j][0])
                if j<len(p)-2 and (p[j+1][1] == 'NN' or p[j+1][1] == 'NNS' or p[j+1][1] == 'NNP' or p[j+1][1] == 'NNPS') and (p[j+2][1] == 'NN' or p[j+2][1] == 'NNS' or p[j+2][1] == 'NNP' or p[j+2][1] == 'NNPS'):
                    new.append(p[j][0] + ' ' + p[j+1][0] + ' ' + p[j+2][0])
                if j<len(p)-1 and (p[j+1][1] == 'NN' or p[j+1][1] == 'NNS' or p[j+1][1] == 'NNP' or p[j+1][1] == 'NNPS'):
                    new.append(p[j][0] + ' ' + p[j+1][0])
        IEWorkExperiences.append(IEWorkExperience)
        # if (len(new) != 0):
        news.append(new)
    IEWorkExperiences += (news)
    # print(IEWorkExperiences)
    # print(IEWorkExperiences)

    seed = ["software", "programming", "language", "network", "security", "computer", "framework", "interface", "library", "operating system", "professional", "profession"]
    finals = []
    links = []
    done = False
    for i in IEWorkExperiences:
        final = []
        for j in i:
            # url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + j
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + j
            response = requests.get(url)
            tree = ElementTree.fromstring(response.content)
            for iii in range(len(tree)):
                # print(j, tree[iii][1].text)
                q1 = "SELECT ?description WHERE { " + "<" + tree[iii][1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"

                data = getData(q1)['results']['bindings']
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        for se in seed:
                            if pp.__contains__(se):
                                final.append(j)
                                print(j)
                                links.append(tree[iii][1].text)
                                done = True
                                break
                if (done == True):
                    done = False
                    break
        # if (len(final) != 0):
        finals.append(final)
    for ii in range(len(news)):
        for dup in finals[ii+len(news)]:
            if finals[ii].__contains__(dup.split(' ')[0]):
                ind = finals[ii].index(dup.split(' ')[0])
                if len(dup.split(' ')) == 3 and ind < len(finals[ii])-2 and finals[ii][ind+1] == dup.split(' ')[1] and finals[ii][ind+2] == dup.split(' ')[2]:
                    finals[ii].pop(ind)
                    finals[ii].pop(ind)
                    finals[ii].pop(ind)
                    finals[ii].insert(ind, dup)
                    finals[ii+len(news)].pop(finals[ii+len(news)].index(dup)+1)
                    finals[ii + len(news)].pop(finals[ii + len(news)].index(dup) + 1)
                elif ind < len(finals[ii])-1 and finals[ii][ind+1] == dup.split(' ')[1]:
                    finals[ii].pop(ind)
                    finals[ii].pop(ind)
                    finals[ii].insert(ind, dup)
                else:
                    finals[ii].pop(ind)
                    finals[ii].insert(ind, dup)
    finalest = finals[0:len(news)]
    IEw = []
    for i in finalest:
        if len(i) != 0:
            temp = list(set(i))
            IEw.append(temp)
    # print(finalest)

    ontologyWE = []
    for i in list(set(links)):
        one = {'parent': []}
        q1 = "SELECT ?label ?parent WHERE {" + "<" + i + ">" + " rdfs:label ?label. " + "<" + i + ">" + "dct:subject ?parent. filter langMatches(lang(?label), 'EN')}"
        data1 = getData(q1)['results']['bindings']
        if (len(data1) != 0):
            one['label'] = data1[0]['label']['value'].lower()
            for result in data1:
                # print(result['label']['value'], result['parent']['value'])
                q2 = "SELECT ?label WHERE {" + "<" + result['parent'][
                    'value'] + ">" + " rdfs:label ?label. filter langMatches(lang(?label), 'EN')}"
                data2 = getData(q2)['results']['bindings']
                one['parent'].append(data2[0]['label']['value'].lower())
                # print(data2[0]['label']['value'])
        else:
            one['label'] = i.split('/')[-1]
        print (one)
        ontologyWE.append(one)

    return IEw, ontologyWE

def extractEducation(education):
    seed = ["degree", "university"]
    finals = []
    done = False
    for i in education:
        new = []
        p = nltk.pos_tag(i)
        for j in range(len(p)):
            if(p[j][1] != 'CD'):
                new.append(p[j][0])
        # strng = ''
        # for j in new:
        #     strng += j + ' '
        # print(strng.strip())
        for strng in new:
            # url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + strng
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + strng
            response = requests.get(url)
            tree = ElementTree.fromstring(response.content)
            for k in range(len(tree)):
                # print(j, tree[k][1].text)
                q1 = "SELECT ?description WHERE { " + "<" + tree[k][
                    1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"

                data = getData(q1)['results']['bindings']
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        for se in seed:
                            if pp.__contains__(se):
                                finals.append(i)
                                done = True
                                break
                if (done == True):
                    break
            if (done == True):
                done = False
                break
    return finals

def extractCertification(certification):
    seed = ["certification"]
    finals = []
    links = []
    done = False
    for i in certification:
        new = []
        p = nltk.pos_tag(i)
        for j in range(len(p)):
            if (p[j][1] != 'CD'):
                new.append(p[j][0])
        strng = ''
        for j in new:
            strng += j + ' '
        # url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=" + strng.strip()
        url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + strng.strip()
        response = requests.get(url)
        tree = ElementTree.fromstring(response.content)
        for k in range(len(tree)):
            # print(j, tree[k][1].text)
            q1 = "SELECT ?description WHERE { " + "<" + tree[k][
                1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"

            data = getData(q1)['results']['bindings']
            if (len(data) != 0):
                if (data[0].keys().__contains__('description')):
                    pp = data[0]['description']['value'].lower()
                    for se in seed:
                        if pp.__contains__(se):
                            finals.append(i)
                            links.append(tree[k][1].text)
                            done = True
                            break
            if (done == True):
                done = False
                break
    return finals, links