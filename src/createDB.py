import psycopg2
import sys
import json
import sys



username = sys.argv[1]
pword = sys.argv[2]

try:
    conn=psycopg2.connect(database='news', user=username, host='localhost', password=pword) 
except Exception as e:
    print("I am unable to connect to the database.")
    print(e)

cur = conn.cursor()

try:
	cur.execute("DROP TABLE stories;")
	print("dropped existing stories table")
except:
	print("There was no existing stories table to drop")

conn.commit()

try:
	cur.execute("CREATE TABLE stories (id serial PRIMARY KEY, info xml);")
	print("created table stories")
except Exception as e:
	print("Could not create table stories")
	print(e)

conn.commit()

