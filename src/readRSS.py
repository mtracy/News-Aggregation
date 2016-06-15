import psycopg2
import sys
import json
import sys
import feedparser
import time
import graphParser

username = sys.argv[1]
pword = sys.argv[2]
url = sys.argv[3]
publisher = sys.argv[4]
subject = sys.argv[5]
refresh = float(sys.argv[6])

def checkDB(title):
    cur.execute("SELECT * FROM stories WHERE title = %s;", (title,))
    results = cur.fetchall()
    if len(results) > 0:
        return 1
    return 0

try:
    conn=psycopg2.connect(database='news', user=username, host='localhost', password=pword) 
except Exception as e:
    print("I am unable to connect to the database.")
    print(e)

cur = conn.cursor()
print("connection to DB established")
feed = feedparser.parse(url)
if(feed.bozo == 1):
    print("the url does not contain a well formed RSS")
    sys.exit(-1)

print(feed.feed.title)

while(1):

    for post in feed.entries:
        title = post.title
        if checkDB(title) == 1:
            #print("skipping " + title)
            break
        else:
	    #string = title + ", " + post.published + ", " + post.links[0].href + ", " + post.summary + ", " + post.media_content[0]['url']
            #print(string)
            print("insterting " + title) 
            try:
                media = post.media_content[0]['url']
            except Exception as e:
                media = ""
	    
	    summary = post.summary.split("<")[0]
	    if len(summary) > 0:
            	path = graphParser.getPath(summary)
	    else:
	        path = graphParser.getPath(title)
	    print(summary)
	    print(path)
	    print("--------")
            cur.execute("INSERT INTO stories (title, source, subject, taxonomy, pubtime, link, summary, media) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (title, publisher, subject, path, post.published, post.links[0].href, summary, media))

    	    conn.commit()

    time.sleep(refresh)
