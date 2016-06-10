import rdflib
from rdflib import Literal
from rdflib.namespace import SKOS

from nltk.corpus import stopwords
from requests import get

sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
g=rdflib.Graph()
g.parse("../taxonomy/tax.xml")
cachedStopWords = stopwords.words("english")

def stripwords(string):
	return ' '.join([word for word in string.split() if word not in cachedStopWords])

def sss(s1, s2, type='relation', corpus='webbase'):
    try:
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return 0.0


def getParentTopic(string):

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
			maxdef = stripwords(definition)
	#print(maxsim)
	#print(maxtopic)
	return maxtopic, maxsim
		#for s,p,o in g.triples( (subject,  SKOS.narrower, None) ):
		#	print "%s contains %s"%(s,o)

def highestSimChild(parent, sentence, simfloor):

	maxtopic = -1
	maxdef = -1
	maxsim = -1
	similarity = -1
	for s,p,o in g.triples( (parent,  SKOS.narrower, None) ):
		definition=g.value(subject=o, predicate=SKOS.definition, object=None) 
		similarity = sss(sentence, definition)
		if similarity > maxsim:
			maxsim = similarity
			maxtopic = o
			maxdef = stripwords(definition)
	#print(maxsim)	
	if maxsim <= simfloor:
		maxsim = -1
		maxtopic = -1
	#print(maxtopic)
	return maxtopic, maxsim



def getPath(sentence):
	path = []
	sub, score = getParentTopic(sentence)
	path.append(sub)
	newsub, newscore = highestSimChild(sub, sentence, score)
	while newsub != -1:
		path.append(newsub)
		newsub, newscore = highestSimChild(sub, sentence, newscore)
	return path
	

