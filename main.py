from sympy import *
from itertools import combinations

import sympy


#todo implementation of contraction of belief base (based on a priority order on formulas in the belief base);
# , belief agent console version,
# Define the closure postulate function
def closure(B, alpha, psi = None):
    """Closure postulate: B ∗ alpha = Cn(B ∗ alpha)"""
    return to_cnf(B + [alpha]) == to_cnf(B) + [alpha]

# Define the success postulate function
def success(B, alpha, psi = None):
    """Success postulate: If alpha /∈ Cn(∅), then alpha /∈ Cn(B ∗ alpha)"""
    return Not(alpha) not in to_cnf([])

# Define the inclusion postulate function
def inclusion(B, alpha, psi = None):
    """Inclusion postulate: B ∗ alpha ⊆ B"""
    return B + [alpha] == B

# Define the vacuity postulate function
def vacuity(B, alpha, psi = None):
    """Vacuity postulate: If alpha /∈ Cn(B), then B ∗ alpha = B"""
    return alpha not in to_cnf(B)

# Define the consistency postulate function
def consistency(B, alpha, psi = None):
    """Consistency postulate: B ∗ alpha is consistent if alpha is consistent"""
    return not to_cnf(B + [alpha]).equals(set())

# Define the extensionality postulate function
def extensionality(B, alpha, psi):
    """Extensionality postulate: If (alpha ↔ psi) ∈ Cn(∅), then B ∗ alpha = B ∗ psi"""
    return to_cnf(B + [alpha]) == to_cnf(B + [psi])

# Define the superexpansion postulate function
def superexpansion(B, alpha, psi):
    """Superexpansion postulate: B ∗ (alpha ∧ psi) ⊆ (B ∗ alpha) + psi"""
    return to_cnf(B + [alpha & psi]).issubset(to_cnf(B + [alpha]) + [psi])

# Define the subexpansion postulate function
def subexpansion(B, alpha, psi):
    """Subexpansion postulate: If ¬psi /∈ B ∗ alpha, then (B ∗ alpha) + psi ⊆ B ∗ (alpha ∧ psi)"""
    return Not(psi) not in to_cnf(B + [alpha]) or to_cnf(to_cnf(B + [alpha]) + [psi]).issubset(to_cnf(B + [alpha & psi]))

# Define a function to check if all postulates are satisfied
def satisfies_all_postulates(B, alpha, psi=None):
    """Check if the revised belief base satisfies all AGM postulates"""
    postulates = [closure, success, inclusion, vacuity, consistency, extensionality, superexpansion, subexpansion]
    for postulate in postulates:
        if not postulate(B, alpha, psi):
            return False, postulate.__doc__.split(":")[0].strip()  # Return the failed postulate
    return True, None  # All postulates are satisfied

# Example usage


def pl_resolution(KB, alpha):  # same as in book figure 7.13
    KB = sympify(KB)
    alpha = sympify(alpha)
    combined_cnf = And(sympy.to_cnf(KB), sympy.to_cnf(Not(alpha)))

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

# Set up an initial list for storing beliefs
knowledge_base = []

# Add a new belief to the knowledge base
def include_belief(knowledge_base, new_belief):
    if knowledge_base:
        # Combine all beliefs in the knowledge base into a single belief
        combined_belief = And(*knowledge_base)
        # Revise the combined belief with the new belief
        revised_belief = revise(combined_belief, new_belief)
        # Clear the knowledge base and add the revised belief to it
        knowledge_base.clear()
        knowledge_base.append(revised_belief)
    else:
        knowledge_base.append(new_belief)

# Show all beliefs in the knowledge base
def show_beliefs(knowledge_base):
    print("\nKnowledge Base Contains:")
    print(knowledge_base)


# Remove all beliefs from the knowledge base
def reset_beleifs(knowledge_base):
    print("\nResetting the knowledge base")
    knowledge_base.clear()

# Function to capture the user's command
def user_command():
    print("\nYou can:")
    print("1) Add a belief")
    print("2) Show beliefs")
    print("3) Reset the belief base")
    print("4) Check entailment of a belief")
    print("5) Exit the program")
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
        if user_choice == "1":
            print("-----------------------")
            belief_input = input("Enter the new belief: ")

            try:
                belief_expr = interpret_belief(belief_input)
                include_belief(knowledge_base, belief_expr)
            except SympifyError:
                print("Could not interpret the belief.")
        elif user_choice == "2":
            show_beliefs(knowledge_base)
        elif user_choice == "3":
            reset_beleifs(knowledge_base)
        elif user_choice == "4":
            alpha = input("Enter alpha: ")
            psi = input("Enter psi: ")
            result, failed_postulate = satisfies_all_postulates(knowledge_base, alpha, psi)
            if result:
                print("\nRevised belief base:", knowledge_base)
            else:
                print("\nRevision rejected: Failed postulate:", failed_postulate)
        
        elif user_choice == "5":
            stop_agent = True
        else:
            print("Action not recognized")

# Start interacting with the agent
interact_with_agent()
