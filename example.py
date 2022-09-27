from googlesearch import search

# query string to search on Google
query = "As you are by Harry Styles"

# number of top search results to fetch
numResults = 3

google_search_results = list(search(query, stop=numResults, pause=1))

print("Here's a list of the top {} search results on Google:\n".format(numResults))
print(google_search_results)