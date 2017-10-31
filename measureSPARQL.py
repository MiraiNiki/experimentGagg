import requests
import time

query = (
    "PREFIX foaf: <http://xmlns.com/foaf/0.1/> " +
    "PREFIX spb: <http://localhost/vocabulary/bench/> " +
    "PREFIX dc: <http://purl.org/dc/elements/1.1/> " +
    "PREFIX : <http://example.org/> CONSTRUCT { " +
    "_:b2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> :Coauthorship . " +
    "_:b2 :author ?auth1 . " +
    "_:b2 :author ?auth2 . " +
    "_:b2 <http://example.org/count> ?prop_count . " +
    "} WHERE { " +
    "SELECT ?auth1  ?auth2 (COUNT(DISTINCT ?s) AS ?prop_count)" +
    "WHERE{ " +
    "?s dc:creator ?b0;  a spb:Inproceedings; dc:creator ?b1 ."
    + "?b0 foaf:name ?name1 ."
    + "?b1 foaf:name ?name2 ."
    + "BIND (IRI(STR(?name1)) AS ?auth1) "
    + "BIND (IRI(STR(?name2)) AS ?auth2)" +
    "FILTER (?name1 < ?name2) " +
    "} GROUP BY ?auth1 ?auth2" +
    "}"
)


# request response to fuseki server
# input: url, query
def requestResponseToFusekiServer(url, query):
    response = requests.post(url, data={'query': query})
    return response



# use your endpoint at local
url = 'http://localhost:3030/sp2b-1Mt/query'
# get together ??

t1 = time.time()
response = requestResponseToFusekiServer(url, query)
t2 = time.time()

elapsed_time = t2 - t1
print(f"経過時間：{elapsed_time}")
