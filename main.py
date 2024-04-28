from sympy import *
from itertools import combinations
from resolution import pl_resolution

import sympy

# belief age index
belief_age = 0
knowledge_base = []

def expand(KB, alpha):
    global belief_age
    belief_age += 1
    KB.append((alpha, belief_age))
    return KB


def contract(KB, notAlpha):
    # Find all sets that do not imply alpha
    remainder_sets = [(belief, age) for belief, age in KB if not pl_resolution(belief, notAlpha)]
    print("Remainder sets")
    print(remainder_sets)

    # Sort the remainder_sets sets by belief age in ascending order
    remainder_sets.sort(key=lambda x: x[1], reverse=True)

    # Calculate the number of sets to include based on the percentage
    if len(remainder_sets) < 100:
        num_sets_to_include = len(remainder_sets)
    else :
        num_sets_to_include = int(len(remainder_sets) * 0.9)

    # Intersect the remainder_sets based on their priority (i.e., belief age)
    # Here we're using the fact that the sets are sorted by belief age to perform the intersection
    contracted_kb = remainder_sets[:num_sets_to_include]
    # Return the contracted knowledge base
    return contracted_kb


def revise(KB, alpha):  # levi identity
    combined_beliefs = And(*[belief for belief, _ in KB])
    if pl_resolution(combined_beliefs, alpha):
        return expand(KB, alpha)

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


# Add a new belief to the knowledge base

def include_belief(kb, new_belief):
    global knowledge_base
    global belief_age
    if knowledge_base:
        # Revise the combined belief with the new belief
        revised_kb = revise(kb, new_belief)
        knowledge_base.clear()
        knowledge_base = revised_kb
    else:
        global belief_age
        belief_age += 1
        knowledge_base.append((new_belief, belief_age))

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
    print("4) Exit the program")
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
            stop_agent = True
        else:
            print("Action not recognized")

# Start interacting with the agent
interact_with_agent()
