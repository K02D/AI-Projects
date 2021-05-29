import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains.copy():
            for value in self.domains[variable].copy():
                if variable.length != len(value):
                    self.domains[variable].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Get overlap between words. self.crossword.overlaps[x, y] returns a tuple (i, j) which denotes that the 
        # ith character of word x overlaps with the jth character of word y
        overlap = self.crossword.overlaps[x, y]
        
        revised = False
        
        # If words don't overlap then no possible conflict
        if not overlap:
            return revised
        
        domain_x = self.domains[x].copy()
        domain_y = self.domains[y].copy()
        
        for val_x in domain_x:
            consistent = False
            for val_y in domain_y:
                # if any overlap agrees and words are distinct then the x value has a possible value in the domain of y
                if val_x[overlap[0]] == val_y[overlap[1]] and val_x != val_y:
                    consistent = True
                    revised = True
                    break
                
            # If no overlap agrees for all y values then remove x value from x's domain
            if not consistent:
                self.domains[x].remove(val_x)
                
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If no parameter passed in then begin with all arcs in the problem
        if not arcs:
            # Use a set so duplicate arcs are eliminated
            queue = set()
            
            # For each variable add all its neighbors
            for var in self.crossword.variables:
                for neighbor in self.crossword.neighbors(var):
                    queue.add((var, neighbor))
                    
            queue = list(queue)
        else:
            queue = arcs
            
        # Iterate until queue is not empty
        while queue:
            # Dequeue
            arc = queue[0]
            del queue[0]
            
            # If domain changed add neighboring arcs to ensure arc consistency
            if self.revise(arc[0], arc[1]):
                
                # If domain empty then variable has no possible value and there is no solution 
                if not self.domains[arc[0]]:
                    return False
                
                # Add neighboring arcs except the one already checked to the queue so they get checked for arc consistency again
                for neighbor in self.crossword.neighbors(arc[0]) - {arc[1]}:
                    queue.append((neighbor, arc[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # If any variable in assignment not present in the set of all crossword variables return False
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        # Check if all values are distinct using set()
        if sorted(list(assignment.values())) != sorted(list(set(assignment.values()))):
            return False

        checked = set()
        
        for variable, value, in assignment.items():
            
            # Check if value is of the correct length
            if variable.length != len(value):
                return False
            
            # Check if there's any conflict between neighboring variables (whether any overlap doesn't agree)
            for neighbor in self.crossword.neighbors(variable):
                if (variable, neighbor) not in checked and neighbor in assignment.keys():
                    overlap = self.crossword.overlaps[variable, neighbor]
                    if value[overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False
                    checked.add((variable, neighbor))
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Keys are values in the domain of var and values are the number of neighbors ruled out 
        domain_with_constraints = dict()
        
        unassigned_neighbors = self.crossword.neighbors(var) - set(assignment.keys())
        
        for value in self.domains[var]:
            ruled_out = 0
            
            for neighbor in unassigned_neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                
                # Number ruled out is the number of neighbors' domain values that can't overlap with the variable's value
                for neighbor_val in self.domains[neighbor]:
                    if value[overlap[0]] != neighbor_val[overlap[1]]:
                        ruled_out += 1
            domain_with_constraints[value] = ruled_out
        
        # Sort domain by ascending number of neighbors ruled out
        return sorted(domain_with_constraints, key=domain_with_constraints.get)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = self.crossword.variables - set(assignment.keys())
        criteria = []
        
        for variable in unassigned:
            domain_length = len(self.domains[variable])
            neighbor_no = 1/len(self.crossword.neighbors(variable))
            criteria.append((variable, domain_length, neighbor_no))
        
        # Sort by priority:-
        # First priority: ascending number of remaining values in the domain
        # Second priority: descending number of neighbors
        criteria.sort(key=lambda criteria: (criteria[1], criteria[2]))
        
        return criteria[0][0]
            
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        # If assignment complete return assignment
        if len(assignment.keys()) == len(self.crossword.variables):
            return assignment
            
        # Select unassigned variable
        var = self.select_unassigned_variable(assignment)
        
        for value in self.domains[var].copy():
            # Make assignment
            new_assignment = assignment.copy()
            new_assignment[var] = value
            
            # If assignment is consistent then reduce domain and call backtrack again with the new assignment added
            if self.consistent(new_assignment):
            
                self.domains[var] = {value}
                result = self.backtrack(new_assignment)
                
                # If result returns a value then assignment complete
                if result:
                    return result

        return None
        

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
