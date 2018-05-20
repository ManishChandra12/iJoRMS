import csv
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import re

# def getData(query):
#     sparql = SPARQLWrapper("http://dbpedia.org/sparql")
#     sparql.setReturnFormat(JSON)
#
#     sparql.setQuery(query)  # the previous query as a literal string
#
#     return sparql.query().convert()

def createCSV():
             # q1="""PREFIX db: <http://dbpedia.org/resource/> SELECT ?p ?o WHERE { db:United_States ?p ?o }"""
            # q1 = """PREFIX dbpedia0: <http://dbpedia.org/ontology/> SELECT ?body ?label WHERE { ?body a dbpedia0:ProgrammingLanguage. ?body rdfs:label ?label. }"""
    # q1 = """PREFIX dbpedia0: <http://dbpedia.org/ontology/> PREFIX dbpedia2: <http://dbpedia.org/property/> SELECT ?label ?parent WHERE { ?body a dbpedia0:ProgrammingLanguage. ?body rdfs:label ?label. ?body dbpedia2:paradigm ?parent. } ORDER BY ?body"""
    # data = getData(q1)['results']['bindings']
    # print (len(data))
    # data1 = []
    # for i in data:
    #     if (i['label']['xml:lang'] == 'en'):
    #         data1.append(i)

    # newRowsList = []
    # with open('skillsWiki.csv', 'r') as inp:
    #     skillSet = csv.reader(inp, delimiter=',')
    #
    #     for row in skillSet:
    #         newRow = [row[0][2:-1], row[1].replace('_',' ')]
    #         newRowsList.append(newRow)
    #         # (skillSet[i][0].replace("b'", ''))
    #         # (skillSet[i][-1].replace("'", ''))
    # inp.close()
    #
    # with open('skillsWiki.csv', 'w') as out:
    #     writer = csv.writer(out)
    #     writer.writerows(newRowsList)
    # out.close()

    # newRowsList = []
    # with open('skillsWiki.csv', 'r') as inp:
    #     skillSet = csv.reader(inp, delimiter=',')
    #
    #     for row in skillSet:
    #         newRow = [re.sub(r'\([^)]*\)', '', row[0]), row[1].replace('_',' ')]
    #         newRowsList.append(newRow)
    #         # (skillSet[i][0].replace("b'", ''))
    #         # (skillSet[i][-1].replace("'", ''))
    # inp.close()
    #
    # with open('skillsWiki.csv', 'w') as out:
    #     writer = csv.writer(out)
    #     writer.writerows(newRowsList)

    newRowsList = []
    with open('skillsWiki.csv', 'r') as inp:
        skillSet = csv.reader(inp, delimiter=',')

        for row in skillSet:
            newRow = [row[0].strip(), row[1].strip()]
            newRowsList.append(newRow)
            # (skillSet[i][0].replace("b'", ''))
            # (skillSet[i][-1].replace("'", ''))
    inp.close()

    with open('skillsWiki.csv', 'w') as out:
        writer = csv.writer(out)
        writer.writerows(newRowsList)

createCSV()

# dict_keys(['bindings', 'distinct', 'ordered'])