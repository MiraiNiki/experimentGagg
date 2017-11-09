import requests
import time

query = (
    "PREFIX foaf: <http://xmlns.com/foaf/0.1/> " +
    "PREFIX spb: <http://localhost/vocabulary/bench/> " +
    "PREFIX dc: <http://purl.org/dc/elements/1.1/> " +
    "PREFIX dct:<http://purl.org/dc/terms/> " +
    "PREFIX : <http://example.org/> "
    + "SELECT ?paper1 ?name1 ?name2 \n"
    + "WHERE {\n"
    + "?paper1 dc:creator ?author1;  a spb:Inproceedings ; dc:creator ?author2 .\n"
    + "?author1 foaf:name ?name1 . \n"
    # dimensions_y
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
        # non-directed_graph
        rel2 = {"from": node.index(d2), "to": node.index(d1)}
        if d1 != d2:
            if rel not in edge:
                if rel2 not in edge:
                    edge.append(rel)
                    mrel = {
                        "index": edge.index(rel),
                        "o": data['paper1']['value']}
                else:
                    mrel = {
                        "index": edge.index(rel2),
                        "o": data['paper1']['value']}
            else:
                mrel = {"index": edge.index(rel), "o": data['paper1']['value']}
            if mrel not in measureEdge:
                measureEdge.append(mrel)
        # measure
        m1 = {"index": node.index(d1), "m": data['paper1']['value']}
        if m1 not in measure:
            measure.append(m1)
        m2 = {"index": node.index(d2), "m": data['paper1']['value']}
        if m2 not in measure:
            measure.append(m2)


def printResult(dicList):
    for dic in dicList:
        for k, v in dic.items():
            print(k, v, end=" , ")
        print()


def testGroupedGraph():
    print("node :")
    print(node)
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
t2 = time.time()
elapsed_time = t2 - t1

print(f"経過時間：{elapsed_time}")
if response['results'] != []:
    getResultArray(response)
    t2 = time.time()
    elapsed_time = t2 - t1

    print(f"経過時間：{elapsed_time}")
    #testGroupedGraph()
