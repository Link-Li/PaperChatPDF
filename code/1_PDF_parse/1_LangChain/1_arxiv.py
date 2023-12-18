# -*- coding: utf-8 -*-
"""
@Time        : 2023/12/17 18:40
@Author      : noahzhenli
@Email       : 
@Description : 
"""



import arxiv

# # Construct the default API client.
# client = arxiv.Client()
#
# # Search for the 10 most recent articles matching the keyword "quantum."
# search = arxiv.Search(
#   query = "llama",
#   max_results = 10,
#   sort_by = arxiv.SortCriterion.SubmittedDate
# )
#
# results = client.results(search)
# # print(len(results))
#
# # `results` is a generator; you can iterate over its elements one by one...
# for r in client.results(search):
#   print(r.title)
# # ...or exhaust it into a list. Careful: this is slow for large results sets.
# all_results = list(results)
# print([r.title for r in all_results])
#
# # For advanced query syntax documentation, see the arXiv API User Manual:
# # https://arxiv.org/help/api/user-manual#query_details
# search = arxiv.Search(query = "au:del_maestro AND ti:checkerboard")
# first_result = next(client.results(search))
# print(first_result)

# # Search for the paper with ID "1605.08386v1"
# search_by_id = arxiv.Search(id_list=["1605.08386v1"])
# # Reuse client to fetch the paper, then print its title.
# first_result = next(client.results(search_by_id))
# print(first_result.title)










import arxiv

big_slow_client = arxiv.Client(
  page_size = 1000,
  delay_seconds = 10.0,
  num_retries = 5
)

# Prints 1000 titles before needing to make another request.
for index, result in enumerate(big_slow_client.results(arxiv.Search(query="quantum"))):
  print(index, ": ", result.title)


