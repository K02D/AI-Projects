# English Sentence Parser

This is an AI that breaks down an English sentence into its grammatical components. It works by using a defined set of recursive rules called context-free grammar. 
A few examples: 

S -> NP VP | S Conj S

This means that a sentence (S) can be either a noun phrase (NP) followed by a verb phrase (VP) <ins>OR</ins> a sentence followed by a conjunction (Conj) and a sentence.

PP -> P | P NP | V PP

This means a prepositional phrase (PP) can be either a preposition <ins>OR</ins> a preposition (P) followed by a noun phrase <ins>OR</ins> a verb phrase followed by a prepositional phrase

<br/>

In this manner, verb phrases, noun phrases and a few othere syntactic units are defined (to see all the definitions you can check the code).

To apply these recursive rules, however, the computer needs to know whether a given word in the English language is a noun, verb, preposition, etc.
Hence, we list all possible instances of each part of speech that appear in the corpus of sentences in the "sentences" directory, like so:

Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"

N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"

By having recursive rules like this for every part of speech and then telling the computer all the possible instances of adjectives, nouns, prepositions, etc, that might appear in the sentence it is attempting to parse, the AI can construct trees representing the different ways you break up a sentence into its constituents without violating any of the pre-written grammatical rules.

Video demonstration: https://youtu.be/5UXi_EOtrIE
