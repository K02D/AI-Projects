# English Sentence Parser

This is an AI that breaks down an English sentence into its grammatical components. It works by using a defined set of recursive rules called context-free grammar. 
A few examples: /n
S -> NP VP | S Conj S
This means that a sentence (S) can be either a noun phrase (NP) followed by a verb phrase (VP)
OR
a sentence followed by a conjunction (Conj) and a sentence.

PP -> P | P NP | V PP
This means a prepositional phrase (PP) can be either a preposition
OR
a preposition (P) followed by a noun phrase
OR 
a verb phrase followed by a prepositional phrase

To apply these recursive rules, however, the computer needs to know whether a given word is a noun, verb, preposition, etc.
Hence, we list all possible values of each part of speech that appear in the corpus of sentences in the "sentences" directory, like so:
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"

By having recursive rules like this for every part of speech and then telling the computer all possible values for adjectives, nouns, prepositions, etc, that might appear in the sentence it is attempting to parse, the AI can construct a tree representing the sentences's grammatical components.

Video demonstration: https://youtu.be/5UXi_EOtrIE
