import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print("sum: ", sum(ranks.values()))
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print("sum: ", sum(ranks.values()))


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # If no links on current page then probability equal for all sites
    if not corpus[page]:
        p = 1 / len(corpus.keys())
        return dict.fromkeys(corpus, p)

    distribution = dict()

    # Number of links on the current page
    no_of_links = len(corpus[page])

    # Probability of going to any page
    p_random = (1 - damping_factor) / len(corpus.keys())

    # Add probability of pages linked from current page
    for pg in corpus[page]:
        distribution[pg] = damping_factor / no_of_links + p_random

    # Add probability of pages not linked from current page
    for pg in corpus.keys():
        if pg not in distribution.keys():
            distribution[pg] = p_random

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Get names of pages
    pages = list(corpus.keys())

    # Stores how many times each page has been visited during sampling
    page_count = dict.fromkeys(corpus, 0)

    # Generate first sample
    first = random.choice(pages)

    page_count[first] += 1

    # Generate probability distribution for first sample
    probabilities = transition_model(corpus, first, damping_factor)

    for i in range(n-1):
        choices = []
        weights = []

        # Get pages and corresponding probabilities
        for page in probabilities.keys():
            choices.append(page)
            weights.append(probabilities[page])

        # Choose next sample given the probabilities as weights
        sample = np.random.choice(choices, p=weights)

        # Update to keep track of how many times a page has been visited
        page_count[sample] += 1

        # Generate probability distribution for next sample
        probabilities = transition_model(corpus, sample, damping_factor)

    # Convert counts into probabilities
    for page in page_count:
        page_count[page] /= n

    return page_count


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Number of pages
    N = len(corpus.keys())

    # Assign each page an equal rank
    page_ranks = dict.fromkeys(corpus, 1 / N)

    # Store updated ranks separately
    new_ranks = dict()

    # Interpret a page having no links as having links to every page
    for key in corpus:
        if not corpus[key]:
            corpus[key] = set(corpus.keys())

    while True:

        # Stores changes to page rank
        changes = []

        for page in page_ranks:

            # Get all pages that link to the current page along with their link counts
            links = links_to_page(corpus, page)

            # Stores probability of getting to the current page from a link
            val = 0

            # Sum probabilities of getting to the current page from another page
            for link in links:

                # Probability is the page rank divided by the number of links
                val += page_ranks[link] / links[link]

            # Calculate new rank
            new_rank = (1 - damping_factor) / N + damping_factor * val

            # Add difference to changes
            changes.append(abs(page_ranks[page] - new_rank))

            # Add new page rank
            new_ranks[page] = new_rank

        # Update page ranks
        for page in page_ranks:
            page_ranks[page] = new_ranks[page]

        # If all changes are less than 0.001 then return page ranks
        if all([x < 0.001 for x in changes]):
            return page_ranks


def links_to_page(corpus, page):
    """
    Return all pages that link to the given page.

    Return a dictionary where keys are the page names
    of pages that link to the given page and values
    are the number of links on that page.
    """
    pages = dict()
    for key in corpus:
        if page in corpus[key]:
            pages[key] = len(corpus[key])
    return pages


if __name__ == "__main__":
    main()
