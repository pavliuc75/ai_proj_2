from sympy import *
from itertools import combinations


#todo implementation of contraction of belief base (based on a priority order on formulas in the belief base);
# , belief agent console version,
# check agains agm postulates

def pl_resolution(KB, alpha):  # same as in book figure 7.13
    combined_cnf = And(to_cnf(KB), to_cnf(Not(alpha)))

    clauses = set(combined_cnf.args)
    new_clauses = set()

    while True:
        pairs = list(combinations(clauses, 2))
        for (Ci, Cj) in pairs:
            resolvents = pl_resolve(Ci, Cj)
            if resolvents == {False}:  # contradiction (KB entails alpha)
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
                new_disjuncts = (_ci | _cj) - {i, j}  # modus ponens
                resolvents.add(Or(*new_disjuncts) if new_disjuncts else False)
    return resolvents


def expand(KB, alpha):
    return And(KB, alpha)


def contract(KB, alpha):
    return KB
    # todo


def revise(KB, alpha):  # levi identity
    if pl_resolution(KB, alpha):  # tautology check
        return KB

    contracted_kb = contract(KB, Not(alpha))
    expanded_kb = expand(contracted_kb, alpha)

    return expanded_kb


a = symbols('a')
b = symbols('b')
c = symbols('c')

expression1 = (a >> b) & a
expression2 = c

# print(revise(expression1, expression2))

# ------------ ADRIAN ---------------#
# Set up an initial list for storing beliefs
knowledge_base = []

# Add a new belief to the knowledge base
def include_belief(knowledge_base, new_belief):
    updated_base = revise(And(*knowledge_base), new_belief) if knowledge_base else new_belief
    knowledge_base.append(to_cnf(updated_base))

# Show all beliefs in the knowledge base
def show_beliefs(knowledge_base):
    print("Knowledge Base Contains:")
    for belief in knowledge_base:
        print(belief)


# Remove all beliefs from the knowledge base
def reset_beleifs(knowledge_base):
    knowledge_base.clear()

# Function to capture the user's command
def user_command():
    print("You can:")
    print("1) add - Add a belief")
    print("2) show - Show beliefs")
    print("3) reset - Reset the belief base")
    print("4) exit - Exit the program")
    return input("Please choose an action: ").strip().lower()

# Interpret and convert user input to a symbolic expression
def interpret_belief(input_belief):
    # This needs to be expanded based on how complex the input can be
    return sympify(input_belief)

# Loop to interact with the belief revision agent
def interact_with_agent():
    stop_agent = False
    while not stop_agent:
        user_choice = user_command()
        if user_choice == "add":
            belief_input = input("Enter the new belief: ")
            try:
                belief_expr = interpret_belief(belief_input)
                include_belief(knowledge_base, belief_expr)
            except SympifyError:
                print("Could not interpret the belief.")
        elif user_choice == "show":
            show_beliefs(knowledge_base)
        elif user_choice == "reset":
            reset_beleifs(knowledge_base)
        elif user_choice == "exit":
            stop_agent = True
        else:
            print("Action not recognized")

# Start interacting with the agent
interact_with_agent()
