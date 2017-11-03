import requests
import time

query = (
    "PREFIX foaf: <http://xmlns.com/foaf/0.1/> " +
    "PREFIX spb: <http://localhost/vocabulary/bench/> " +
    "PREFIX dc: <http://purl.org/dc/elements/1.1/> " +
    "PREFIX dct:<http://purl.org/dc/terms/> " +
    "PREFIX : <http://example.org/> CONSTRUCT { " +
    "_:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> :Citation . " +
    "_:b2 :from ?b0 ."
    + "?b0 foaf:name ?name1 ." +
    "_:b2 :to ?b1 . " +
    "?b1 foaf:name ?name2 ." +
    "_:b2 <http://example.org/count> ?prop_count . " +
    "} WHERE { " +
    "SELECT ?b0 ?name1 ?b1 ?name2 (COUNT(*) AS ?prop_count)" +
    "WHERE{ " +
    "?p1 dc:creator ?b0;  a spb:Inproceedings; dct:references ?refs . " +
    "?b0 foaf:name ?name1 . " +
    "?p2 dc:creator ?b1;  a spb:Inproceedings . " +
    "?b1 foaf:name ?name2 . " +
    "?refs ?p ?p2 . " +
    "} GROUP BY ?b0 ?b1 ?name1 ?name2" +
    "}"
)

# request response to fuseki server
# input: url, query


def requestResponseToFusekiServer(url, query):
    response = requests.post(url, data={'query': query})
    return response.content


# use your endpoint at local
url = 'http://localhost:3030/sp2b-500kt/query'
# get together ??

t1 = time.time()
response = requestResponseToFusekiServer(url, query)
t2 = time.time()

elapsed_time = t2 - t1
print(f"経過時間：{elapsed_time}")
