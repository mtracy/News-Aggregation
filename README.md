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

Then, you can run
```
./runner.sh inputfile yourDBusername yourDBpassword
```

where `inputfile` is a pipe-delimited input file containing RSS feeds that you are listening to. There is an example file in the `/inputs` directory. The format of the input file is as follows

```
{RSS URL}|{Publishing Site (for example, NBC}|{Subject content of the RSS (e.g. "general news" or "technology"}|{the desired rate at which you want to check the RSS feed in seconds}
```
