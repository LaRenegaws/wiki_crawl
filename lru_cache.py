import datetime

class Cache:
  """
  Basic LRU cache that is made using a dictionary
  The value stores a date field that is used to maintain the elements in the cache
  Date field is used to compare expire an element in the cache
  Persisted field is a boolean that determines whether it can be deleted
  """

  def __init__(self, size):
    self.cache_size_limit = size
    self.__cache = {}


  def update(self, key, value=None, persisted=False):
    """
    if inputs are key and value then adds the key and value to the cache
    if inputs are only key, then only updates the access date for the element in the cache
    """

    if value == None:
      if not self.exists(key):
        raise LookupError("The element does not exist in the cache")

      self.__cache[key]["date"] = datetime.datetime.utcnow()

    else:
      date = datetime.datetime.utcnow()

      if self.size() == self.cache_size_limit:
        self.delete_oldest_entry()

      self.__cache[key] = { "date": date, "value": value, "persisted": persisted }


  def delete_oldest_entry(self):
    # Deletes the dictionary element that was the last element to be updated
    oldest = datetime.datetime.utcnow()
    oldest_key = None

    for key in self.__cache:
      if self.__cache[key]["date"] < oldest and not self.__cache[key]["persisted"]:
        oldest = self.__cache[key]["date"]
        oldest_key = key

    del self.__cache[oldest_key]


  def find(self, key):
    # Returns the value that is associated with the key
    # Otherwise returns False
    if not self.exists(key):
      # raise LookupError("The element does not exist in the cache")
      return False
    else:
      return self.__cache[key]["value"]


  def size(self):
    return len(self.__cache)


  def exists(self, key):
    # Returns a boolean whether the key exists in the cache
    return key in self.__cache


class WikiCache(Cache):
  """
  For the purpose of the wiki_crawl,
  the key represents the article title
  and the value is the number of links until philosophy

  There is a pattern of certain wiki links appearing frequently prior
  to reaching Philosophy. As a result, I will initiallly seed the cache
  with the most common links that I've noticed to improve performance.
  The seeded entries would then not be expirable in the cache
  """

  def __init__(self, size=100):
    Cache.__init__(self, size)
    self.seed_wiki_cache()


  def seed_wiki_cache(self):
    common_links = {
      "Critical thinking - Wikipedia": 6,
      "Polity - Wikipedia": 4,
      "Geometry - Wikipedia": 4,
      "Fact - Wikipedia": 5,
      "Mathematics - Wikipedia": 3,
      "Ontology - Wikipedia": 2,
      "Premise - Wikipedia": 3,
      "Logic - Wikipedia": 2,
      "Quantity - Wikipedia": 2,
      "Argument - Wikipedia": 1,
      "Property (philosophy) - Wikipedia": 1,
      "Psychology - Wikipedia": 12
    }

    for key in common_links:
      self.update(key, common_links[key], True)
