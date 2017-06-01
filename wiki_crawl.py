import urllib
from bs4 import BeautifulSoup # library for pulling data out of HTML and XML files
from tinydb import TinyDB, Query
import lru_cache

base_url = "https://en.wikipedia.org"
wiki_db = TinyDB('wiki_db.json')
Wiki = Query()

def remove_brackets(text):
  """
  params: takes in a string with the assumption that the text only has valid parenthesis

  We need to avoid links within parenthesis so this strips text within parenthesis
  it leaves parenthesis in place for anything within "<" and ">" tags

  return: input string but stripped of text within parenthesis outside of "<" ">" tags
  """

  text = str(text)
  parenth_tracker = 0
  in_tag = False
  output = ""

  for sym in text:

    if parenth_tracker == 0:
      if sym == "<":
        in_tag = True

      if sym == ">":
        in_tag = False

    if not in_tag:
      if sym == "(":
        parenth_tracker += 1

      if sym == ")":
        parenth_tracker -= 1

      elif parenth_tracker == 0:
        output += sym # character concactenation

    elif in_tag:
      output += sym

  return output


def find_link(main):
  """
  params: html

  iterates through only the paragraphs in the main body to find the first url, which avoids italicized links
  The link should be in the first paragraph in the main body, but can't be certain of this so iterate through them all

  returns: first link in the html
  """

  # Paragraphs related directly to the main wikipedia article (aren't italicized, header notes etc) are under <p> tag
  for p in main.find_all("p", recursive=False):

    p_less_brackets = BeautifulSoup(remove_brackets(p), "lxml")

    for url in p_less_brackets.find_all("a", href=True):

      # self-directed links on wikipedia have "#" in the href appended to the current link
      if "#" in url.get("href") and "#" != str(url.get("href")[0]):
        raise AttributeError("Not an external link")
        break

      # Ignores citations they begin with '#' on Wikipedia
      # Only finds url links that are outside parenthesis
      # Ignores the Help:IPA for pronunciation
      if url and "#" not in url.get("href") and "Help:IPA" not in url.get("href"):
        link =  base_url + url.get("href")
        return link


def crawl(link, cache=None):
  counter = -1 # track number of path links
  starting_title = ""
  title = ""

  # keeps track of existing wiki articles that have shown up during the crawl
  # used to check against looping articles
  visited_wiki_paths = {}

  # link = "https://en.wikipedia.org/wiki/Continent"

  while title != 'Philosophy - Wikipedia':

    try:
      html = urllib.urlopen(link).read()
      soup = BeautifulSoup(html, "lxml")
      # html id for the main content body for wikipedia
      main_body = soup.find(id="mw-content-text")
      counter += 1

      title = soup.title.string

      # Return a cached value of the path length if wiki title exists in cache
      if cache:
        if counter == 0:
          starting_title = title

        if cache.exists(title):
          if cache.find(title) == "Articles in a loop":
            raise AttributeError("Articles in a loop")

          else:
            counter += cache.find(title)
            break

      # Checks against looping articles
      if title in visited_wiki_paths:
        if cache:
          cache.update(starting_title, "Articles in a loop")

        raise AttributeError("Articles in a loop")

      else:
        # append the title to a list of visited titles
        visited_wiki_paths[title] = True

      print title

      link = find_link(main_body)

    except AttributeError as err:
      print err.args
      update_wiki_db("failure")
      break

  # Update the cache with the number of links that it took to reach philosophy
  if cache and cache.find(starting_title) != "Articles in a loop":
    cache.update(starting_title, counter)

  del visited_wiki_paths # clear memory after each loop

  print str(counter) + "\n"
  update_wiki_db("success")


def initialize_crawl(input):
  link = "https://en.wikipedia.org/wiki/Special:Random"

  if input == "s":
    command = raw_input("Enter wikipedia link, or r for random link: ")

    if command != "r":
      link = command
    crawl(link)

  elif input == "c":
    # initialize cache to improve performance with continuous crawl
    link_path_cache = lru_cache.WikiCache()
    while True:
      crawl(link, link_path_cache)

  else:
    raise ValueError("Invalid user input")


"""
TinyDB initialization and update function
"""

def initialize_db():

  if not wiki_db.search(Wiki.result.exists()):
    wiki_db.insert({'result': 'success', 'count': 0})
    wiki_db.insert({'result': 'failure', 'count': 0})
    wiki_db.insert({'result': 'conversion_rate', 'count': 0})


def update_wiki_db(result):
  """
  Updates the failure or success counts
  Updates the conversion rate of reaching Philosophy
  """

  curr_count = wiki_db.search(Wiki.result == result)[0]["count"]
  # print curr_count
  wiki_db.update({'count': curr_count+1}, Wiki.result == result)

  success_count = wiki_db.search(Wiki.result == "success")[0]["count"]
  failure_count = wiki_db.search(Wiki.result == "failure")[0]["count"]
  conversion_rate = float(success_count) / (success_count + failure_count)

  wiki_db.update({'count': conversion_rate}, Wiki.result == "conversion_rate")


if __name__ == "__main__":
  command = raw_input("Do you want to perform a continuous loop or single iteration(c = continous, s = single): ")

  initialize_crawl(command)
  initialize_db()
