# Question Answering (QA) AI

This is an AI that answers inputted questions by retrieving relevant sentences from a corpus of texts (it works only assuming that the corpus has some sentence that answers the user's question). 

The AI first finds which document is the most relevant to the query using a metric called *tf-idf* and then finds the most relevant sentence by using the metrics *idf*, *matching word measure* and *query term density*. 

**term frequency (tf)**: number of times a term appears in a document

**inverse document frequency (idf)**: measure of how rare a word is across documents

**tf-idf**: measure of the importance of a word in a document, calculated by multiplying term frequency (tf) by inverse document frequency (idf)
If a word is used more often and the word is rarer over the entire corpus, it is likely to be more relevant or important to the current document. 

**matching word measure**: sum of IDF values for any word in the query that also appears in the sentence
The rarer the word and the more words there are in common, the greater the sum. 
**query term density**: proportion of words in the sentence that are also words in the query

Video demonstration: https://youtu.be/-B8ZuXwRUnw
