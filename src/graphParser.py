import rdflib
g=rdflib.Graph()
g.parse("../taxonomy/tax.xml")


qres = g.query(
    """SELECT DISTINCT ?s
       WHERE {
          ?s ?p ?o1 .
          FILTER(NOT EXISTS {?s skos:broader ?o2}) 
       }""")

for row in qres:
    print("%s" % row)
