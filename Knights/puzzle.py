""""
All knowledge bases are as logically unsimplified as possible to provide the most
direct translation of the information in the puzzle, as instructed in the specification.
"""

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Encoding puzzle rules: A is either a knight or a knave (XOR)
    Or(And(AKnight, Not(AKnave)), And(Not(AKnight), AKnave)),

    # If A is a knight then A is both a knight and a knave
    Biconditional(AKnight, And(AKnight, AKnave)),

    # If A is a knave then A is not both a knight a knave
    Biconditional(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Encoding puzzle rules: A and B are either a knight or a knave (XOR)
    Or(And(AKnight, Not(AKnave)), And(Not(AKnight), AKnave)),
    Or(And(BKnight, Not(BKnave)), And(Not(BKnight), BKnave)),

    # If A is a knight then A and B both knaves
    Biconditional(AKnight, And(AKnave, BKnave)),

    # If A is a knave then A and B not both knaves
    Biconditional(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Encoding puzzle rules: A and B are either a knight or a knave (XOR)
    Or(And(AKnight, Not(AKnave)), And(Not(AKnight), AKnave)),
    Or(And(BKnight, Not(BKnave)), And(Not(BKnight), BKnave)),

    # If A is a knight then both knaves or both knights
    Biconditional(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),

    # If A is a knave then not both knaves or knights
    Biconditional(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),

    # If B is a knight then one knight one knave (XOR)
    Biconditional(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),

    # If B is a knave then not one knight one knave (not XOR)
    Biconditional(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Encoding puzzle rules: A, B and C are either a knight or a knave (XOR)
    Or(And(AKnight, Not(AKnave)), And(Not(AKnight), AKnave)),
    Or(And(BKnight, Not(BKnave)), And(Not(BKnight), BKnave)),
    Or(And(CKnight, Not(CKnave)), And(Not(CKnight), CKnave)),

    Biconditional(BKnight,
                  # If B is a knight then A said "I am a knave"
                  And(Or(Biconditional(AKnave, Not(AKnave)),
                         Biconditional(AKnight, AKnave)),
                         
                      # If B is a knight then C is a knave
                      CKnave)),

    Biconditional(BKnave,
                  # If B is a knave then A said "I am a knight"
                  And(Or(Biconditional(AKnave, Not(AKnight)),
                         Biconditional(AKnight, AKnight)),
                         
                      # If B is a knave then C is a knight
                      Not(CKnave))),

    # If C is a knight then A is a knight
    Biconditional(CKnight, AKnight),

    # If C is a knave then A is not a knight
    Biconditional(CKnave, Not(AKnight))

    # A can't say "I am a knave" since this paradoxical. Thus, B logically can't be a knight
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
