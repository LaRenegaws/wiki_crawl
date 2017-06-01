# Wikipedia Crawler to Philosophy

It has been noted that clicking the first link on any wikipedia article will allow it to reach the philosophy wikipedia article.
This tests that assumption.
The wikipedia crawler clicks the first link in the main text and continues until it either reaches philsophy which is considered a success.
If it does not reach philosophy, then it is considered a failure.
Failures can occur when the articles loop, the first link is an internal redirect, or it does not redirect anywhere.

The wiki_db.json contains a small sample size of the success and failure outcomes along with the conversion rate.
The cache is used to improve performance when iterating through continuous cycles.

Install necessary dependencies to run the program
```
$ pip install BeautifulSoup4
```
```
$ pip install lxml
```
```
$ pip install tinydb
```

Resolved issues related to parsing external web links on wikipedia :

 - internal redirects within the same page, which include "#" appended to the url
 - help ipa for pronouciation
 - first link that is in the main article. Ignore other notifications, alerts, notes unrelated to the main ariticle
 - avoid links that are within parenthesis
