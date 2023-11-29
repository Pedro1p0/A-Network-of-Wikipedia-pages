from operator import itemgetter
import networkx as nx
import wikipedia
import matplotlib.pyplot as plt

# https://en.wikipedia.org/wiki/Complex_network
SEEDS = ["Complex network", "Graph theory", "Network science", "Social network"]
STOPS = ("International Standard Serial Number",
         "International Standard Book Number",
         "National Diet Library",
         "International Standard Name Identifier",
         "International Standard Book Number (Identifier)",
         "Pubmed Identifier",
         "Pubmed Central",
         "Digital Object Identifier",
         "Arxiv",
         "Proc Natl Acad Sci Usa",
         "Bibcode",
         "Library Of Congress Control Number",
         "Jstor",
         "Doi (Identifier)",
         "Isbn (Identifier)",
         "Pmid (Identifier)",
         "Arxiv (Identifier)",
         "Bibcode (Identifier)")

todo_lst = [(0, seed) for seed in SEEDS]  # The seeds are in layer 0
todo_set = set(SEEDS)  # The seeds themselves
done_set = set()  # Nothing is done yet

g = nx.DiGraph()

while todo_lst:
    layer, page = todo_lst[0]

    # Remove the name page of the current page from the todo_lst,
    # and add it to the set of processed pages.
    # If the script encounters this page again, it will skip over it.
    del todo_lst[0]
    done_set.add(page)

    # Show progress
    print(layer, page)

    # Attempt to download the selected page.
    try:
        wiki = wikipedia.page(page)
    except:
        print("Could not load", page)
        continue

    if layer < 2:  # Limit the search to the second layer
        for link in wiki.links:
            link = link.title()
            if link not in STOPS and not link.startswith("List Of"):
                if link not in todo_set and link not in done_set:
                    todo_lst.append((layer + 1, link))
                    todo_set.add(link)
                g.add_edge(page, link)

print("{} nodes, {} edges".format(len(g), nx.number_of_edges(g)))
