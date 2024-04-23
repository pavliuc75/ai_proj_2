from sympy import *
from itertools import combinations
#---------------------Andrei-------------------------#
#AGM postulates check
class BeliefBase:
    def __init__(self, beliefs):
        self.beliefs = beliefs

    def add_belief(self, new_belief):
        if new_belief not in self.beliefs:
            self.beliefs.append(new_belief)

    def revise(self, new_beliefs):
        for new_belief in new_beliefs:
            self.beliefs = [belief for belief in self.beliefs if not pl_resolution(belief, Not(new_belief))]

    def contraction(self, belief_to_remove):
        self.beliefs = [belief for belief in self.beliefs if belief != belief_to_remove]

    def expansion(self, new_beliefs):
        for new_belief in new_beliefs:
            self.add_belief(new_belief)

    def entails(self, belief):
        return any(pl_resolution(b, belief) for b in self.beliefs)
#------------------end ------------------------#
def pl_resolution(KB, alpha):  
    combined_cnf = And(to_cnf(KB), to_cnf(Not(alpha)))
    clauses = set(combined_cnf.args)
    new_clauses = set()

    while True:
        pairs = list(combinations(clauses, 2))
        for (Ci, Cj) in pairs:
            resolvents = pl_resolve(Ci, Cj)
            if resolvents == {False}:  
                return True
            new_clauses |= resolvents

        if new_clauses.issubset(clauses):
            return False

        clauses |= new_clauses

def pl_resolve(ci, cj):
    _ci = set(ci.args if isinstance(ci, Or) else [ci])
    _cj = set(cj.args if isinstance(cj, Or) else [cj])

    resolvents = set()
    for i in _ci:
        for j in _cj:
            if i == Not(j) or Not(i) == j:
                new_disjuncts = (_ci | _cj) - {i, j}  
                resolvents.add(Or(*new_disjuncts) if new_disjuncts else False)
    return resolvents

def expand(KB, alpha):
    return And(KB, alpha)

def contract(KB, alpha):
    return KB

def revise(KB, alpha):  
    if pl_resolution(KB, alpha):  
        return KB

    contracted_kb = contract(KB, Not(alpha))
    expanded_kb = expand(contracted_kb, alpha)

    return expanded_kb

a, b, c = symbols('a b c')

# ------------ ADRIAN ---------------#
# Set up an initial list for storing beliefs
knowledge_base = []
belief_base = BeliefBase(knowledge_base)

# Add a new belief to the knowledge base
def add_belief(knowledge_base, new_belief):
    if knowledge_base:
        knowledge_base = revise(knowledge_base, new_belief)
    else:
        knowledge_base = new_belief

# Show all beliefs in the knowledge base
def show_beliefs(knowledge_base):
    print("Knowledge Base Contains:")
    print(knowledge_base)

# Remove all beliefs from the knowledge base
def reset_beliefs(knowledge_base):
    knowledge_base.clear()

# Function to capture the user's command
def user_command():
    print("You can:")
    print("1) Add a belief")
    print("2) Show beliefs")
    print("3) Reset the belief base")
    print("4) Check entailment for a symbol")
    print("5) Exit the program")
    return input("Please choose an action: ").strip().lower()

# Interpret and convert user input to a symbolic expression
def interpret_belief(input_belief):
    return sympify(input_belief)

# Loop to interact with the belief revision agent
def interact_with_agent():
    stop_agent = False
    while not stop_agent:
        user_choice = user_command()
        if user_choice == "1":
            print("-----------------------")
            belief_input = input("Enter the new belief: ")

            try:
                belief_expr = interpret_belief(belief_input)
                add_belief(knowledge_base, belief_expr)
            except SympifyError:
                print("Could not interpret the belief.")
        elif user_choice == "2":
            show_beliefs(knowledge_base)
        elif user_choice == "3":
            reset_beliefs(knowledge_base)
        elif user_choice == "4":
            symbol = input("Enter the symbol to check: ")
            try:
                symbol_expr = Symbol(symbol)
                print(f"Does the knowledge base entail {symbol}? {belief_base.entails(symbol_expr)}")
            except SympifyError:
                print("Could not interpret the symbol.")  
        elif user_choice == "5":
            stop_agent = True
        else:
            print("Action not recognized")

# Start interacting with the agent
interact_with_agent()
