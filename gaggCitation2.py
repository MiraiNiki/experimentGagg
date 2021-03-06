import requests
import time

query = (
    "PREFIX foaf: <http://xmlns.com/foaf/0.1/> " +
    "PREFIX spb: <http://localhost/vocabulary/bench/> " +
    "PREFIX dc: <http://purl.org/dc/elements/1.1/> " +
    "PREFIX dct:<http://purl.org/dc/terms/> " +
    "PREFIX : <http://example.org/> "
    + "SELECT ?paper1 ?paper2 ?name1 ?name2 \n"
    + "WHERE {\n"
    # relation
    + "?refs ?p ?paper2 .\n"
    # dimensions_x
    + "?paper1 dc:creator ?author1;  a spb:Inproceedings ; dct:references ?refs .\n"
    + "?author1 foaf:name ?name1 . \n"
    # dimensions_y
    + "?paper2 dc:creator ?author2;  a spb:Inproceedings . \n"
    + "?author2 foaf:name ?name2 . \n"

    + "}\n"
)

edge = []
measureEdge = []
node = []
measure = []

# request response to fuseki server
# input: url, query


def requestResponseToFusekiServer(url, query):
    response = requests.post(url, data={'query': query})
    return response.json()

# get result array
# return s p o
def getResultArray(response):
    responseSparqlArray = response['results']['bindings']
    for data in responseSparqlArray:
        # dimension
        d1 = data["name1"]['value']
        if d1 not in node:
            node.append(d1)
        d2 = data["name2"]['value']
        if d2 not in node:
            node.append(d2)
        # relation
        rel = {"from": node.index(d1), "to": node.index(d2)}
        if rel not in edge:
            edge.append(rel)
        # measure
        m1 = {"index": node.index(d1), "m": data['paper1']['value']}
        if m1 not in measure:
            measure.append(m1)
        m2 = {"index": node.index(d2), "m": data['paper2']['value']}
        if m2 not in measure:
            measure.append(m2)
        mrel = {"index": edge.index(rel), "o": data['paper1']['value']}
        measureEdge.append(mrel)


def printResult(dicList):
    for dic in dicList:
        for k, v in dic.items():
            print(k, v, end=" , ")
        print()


def testGroupedGraph():
    print("node :")
    printResult(node)
    print("measure :")
    measure.sort(key=lambda x: x['index'])
    printResult(measure)
    edge.sort(key=lambda x: x['from'])
    print("edge :")
    printResult(edge)
    measureEdge.sort(key=lambda x: x['index'])
    print("measureEdge :")
    printResult(measureEdge)


# use your endpoint at local
url = 'http://localhost:3030/sp2b-500kt/query'
# get together ??
t1 = time.time()
response = requestResponseToFusekiServer(url, query)
if response['results'] != []:
    getResultArray(response)
    t2 = time.time()
    elapsed_time = t2 - t1

    print(f"経過時間：{elapsed_time}")


    # testGroupedGraph()
