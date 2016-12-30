import urllib
from bs4 import BeautifulSoup # library for pulling data out of HTML and XML files

base_url = "https://en.wikipedia.org"

def remove_brackets(text):
  # assuming that wiki text only has valid parenthesis
  # strips text within parenthesis  
  # it leaves parenthesis in place for anything within "<" and ">" tags

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

      if parenth_tracker > 0:
        output += " "

      else: 
        output += sym

    else:
      output += sym

  return output

def find_link(main):
  # iterates through only the paragraphs in the main body to find the first url, which avoids italicized links
  # The link should be in the first paragraph in the main body, but can't be certain of this so iterate through them all
  for p in main.find_all("p", recursive=False):

    p_less_brackets = BeautifulSoup(remove_brackets(p), "lxml")
    
    for url in p_less_brackets.find_all("a", href=True):

      # self-directed links on wikipedia have "#" in the href
      if "#" in url.get("href"):
        if "#" != str(url.get("href")[0]):
          
          raise AttributeError("Not an external link")
          break

      # Ignores citations they begin with '#' on Wikipedia 
      # Only finds url links that are outside parenthesis
      # Ignores the Help:IPA for pronunciation
      if url and "#" not in url.get("href") and "Help:IPA" not in url.get("href"): 
        
        link =  base_url + url.get("href")
        return link

def path_length():
  
  counter = 0 # track number of path links
  title = ''

  # used to check against looping articles
  prev_title = ''
  prev_prev_title = ''
  link = "https://en.wikipedia.org/wiki/Special:Random"


  while title != 'Philosophy - Wikipedia':

    try: 
      html = urllib.urlopen(link).read()
      soup = BeautifulSoup(html, "lxml")
      main_body = soup.find(id="mw-content-text")
      counter += 1

      prev_prev_title = prev_title
      prev_title = title
      title = soup.title.string

      # Checks against looping articles 
      if prev_prev_title == title:
        raise AttributeError("Articles in a loop")
      print title

      link = find_link(main_body)

    except AttributeError as err: 
      print err.args
      break

  return counter

if __name__ == "__main__":
  length = 0
  length = path_length()
  print length
