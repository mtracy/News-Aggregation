import rdflib
from rdflib import Literal
from rdflib.namespace import SKOS

from requests import get

sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"

def sss(s1, s2, type='relation', corpus='webbase'):
    try:
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return 0.0


def getParentTopic(string):
	g=rdflib.Graph()
	g.parse("../taxonomy/tax.xml")


	qres = g.query(
		"""SELECT DISTINCT ?s ?def
			WHERE {
				?s ?p ?o1 .
				FILTER(NOT EXISTS {?s skos:broader ?o2}) 
				?s skos:definition ?def .
		   }""")

	maxtopic = -1
	maxdef = -1
	maxsim = -1
	similarity = -1
	for (subject, definition) in qres:
		similarity = sss(string, definition)
		if similarity > maxsim:
			maxsim = similarity
			maxtopic = subject
			maxdef = definition
		
	return maxtopic, maxdef
		#for s,p,o in g.triples( (subject,  SKOS.narrower, None) ):
		#	print "%s contains %s"%(s,o)

s1="the city of Paris is on high alert, with floodwaters on the River Seine due to peak in the coming hours and heavy rain continuing to sweep across Europe"
s2="The study, reporting and prediction of meteorological phenomena."
#sim = sss(s1, s2)
#print(sim)

sub, definition = getParentTopic(s1)

print(definition)

