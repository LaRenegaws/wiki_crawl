# Wikipedia Crawler to Philosophy

The wikipedia crawler clicks the first link in the main text and continues until it either reaches philsophy which is considered a success.
If it does not reach philosophy, then it is considered a failure.
Failures can occur when the articles loop, the first link is an internal redirect, or it does not redirect anywhere.

The wiki_db.json contains a small sample size of the success and failure outcomes along with the conversion rate.
The cache is used to improve performance when iterating through continuous cycles.

Install necessary dependencies to run the prorgam
$ pip install BeautifulSoup4
$ pip install lxml
$ pip install tinydb

