from nim import train, play

ai = train(10000)
while True:
    play(ai)
    if input("Press enter to play again"):
        break
