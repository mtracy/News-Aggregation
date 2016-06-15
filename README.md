# News-Aggregation
A tool to aggregate news from rss feeds into a postgres database. 


# Setup

First pip install the requirements document

```
pip install -r requirements.txt
```

Then, change directories to the `/src` folder and run

```
python createDB.py yourDBusername yourDBpassword
```

obviously with filling in your appropriate credentials for your postgres database.

# Run
```
./runner.sh inputfile yourDBusername yourDBpassword
```

where `inputfile` is a pipe-delimited input file containing RSS feeds that you are listening to. There is an example file in the `/inputs` directory. The format of the input file is as follows

```
{RSS URL}|{Publishing Site (for example, NBC}|{Subject content of the RSS (e.g. "general news" or "technology"}|{the desired rate at which you want to check the RSS feed in seconds}
```

# Database Scheme

The database that is created has the following schema

```
(title, source, subject, taxonomy, pubtime, link, summary, media)
```

`title` is the title of the particular article in the RSS.

`source` is the source which this story was acquired from, which is obtained from the input file.

`subject` is the general subject that the RSS was classified as in the input file.

`taxonomy` is an array of values which classifies the story according to the taxonomy in `/taxonomy/tax.xml` which was obtained from [here](https://iptc.org/standards/media-topics/). It does so by determining the semantic similarity between the article's description, and the description of top level topics defined by the iptc taxonomy. Once this top level is determined, it progresses down the tree, adding additional child topics if the semantic similarity between the news article and the child is higher than that of the article and the parent. The semantic similarity is determined using a web api which is documented [here](http://swoogle.umbc.edu/SimService/api.html). 

`pubtime` is the time at which the article was published. 

`link` is the link to the article.

`summary` is the summary of the article (if it exists).

`media` contains a link to any media that may have been posted with the article.

 **When parsing an RSS, the script will stop when it either reaches the end of the RSS or it finds a title that already exists in the database.** It will, however, still try again when the refresh time resets.
