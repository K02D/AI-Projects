# Degrees of separation

This is a program that determines how many "degrees of separation" apart two actors are.

The degree of separation is the minimum number of movies needed to connect two actors. For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

To frame it as a search problem, the states are people and actions are movies (since they take us from one person to another).

The program works by using breadth-first search, which is essentially when an algorithm takes one step in every possible direction before taking a second step in any one direction. 

Video demonstration: https://youtu.be/TXew1A7H1xY
