from SPARQLWrapper import SPARQLWrapper, JSON

def getData(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()

def main():
    q1 = """PREFIX dbpedia0: <http://dbpedia.org/page/Programmer> SELECT ?description WHERE { dbo:abstract ?description. }"""
    data = getData(q1)
    print(data)

main()


# PREFIX db: <http://dbpedia.org/resource/>
# SELECT  ?o
# WHERE { db:Programmer dbo:abstract ?o
# filter(langMatches(lang(?o),"EN"))
# }
# #
#
# function _set_html_from_dbpedia_description(selector, search_for) {
#   $.ajax({
#     url: "http://lookup.dbpedia.org/api/search/KeywordSearch",
#     data: {
#       "QueryString" : search_for,
#       "MaxHits" : 1,},
#     dataType: 'json',
#     success: function( response ) {
#       if ( response.results[0] ) {
#         $( selector ).html(response.results[0].description + " <i>[Source: Wikipedia]</i>");
#       };
#     },
#     timeout: 2500,
#   });
# }

# import requests
# from xml.etree import ElementTree
# url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=system%20analyst"
# # url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString=jjjjjj"
# response = requests.get(url)
# tree = ElementTree.fromstring(response.content)
# print(tree[0][1].text)