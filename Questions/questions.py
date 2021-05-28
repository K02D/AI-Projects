import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)

def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    print("Loading data...")
    info = dict()
    for doc in os.listdir(directory):
        with open(os.path.join(directory, doc), encoding="utf8", mode="r") as f:
            info[doc] = f.read()
    return info


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document)
    words_out = []
    for w in words:
        # Exclude stop words and punctuation
        if w in nltk.corpus.stopwords.words("english") or w in string.punctuation:
            continue
        words_out.append(w.lower())
    return words_out


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_idf = dict()
    n = len(documents.keys())
    for doc in documents:
        for word in documents[doc]:
            # Compute inverse document frequency, a measure of rarity, for each word
            appears_in = 1
            for d in documents:
                if d != doc and word in documents[d]:
                    appears_in += 1
            word_idf[word] = math.log(n / appears_in)
    return word_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    pairs = []
    for f in files:
        tf_idf = 0
        for word in query:
            if word in files[f]:
                tf_idf += files[f].count(word) * idfs[word]
        pairs.append((f, tf_idf))
    return [file[0] for file in sorted(pairs, key=lambda k: k[1], reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    data = []
    for s in sentences:
        measure = 0
        in_sentence = 0
        for word in query:
            if word in sentences[s] and word not in nltk.corpus.stopwords.words("english"):
                in_sentence += 1
                measure += idfs[word]
        qtd = in_sentence / len(sentences[s])
        data.append((s, measure, qtd,))
    return [sentence[0] for sentence in sorted(data, key=lambda k: (k[1], k[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
