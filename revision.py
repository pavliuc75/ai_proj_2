from resolution import pl_resolution
from sympy import *


def revise(KB, alpha):  # levi identity
    combined_beliefs = And(*[belief for belief, _ in KB])
    if pl_resolution(combined_beliefs, alpha):
        return expand(KB, alpha)

    contracted_kb = contract(KB, Not(alpha))
    expanded_kb = expand(contracted_kb, alpha)

    return expanded_kb


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
    else:
        num_sets_to_include = int(len(remainder_sets) * 0.9)

    # Intersect the remainder_sets based on their priority (i.e., belief age)
    # Here we're using the fact that the sets are sorted by belief age to perform the intersection
    contracted_kb = remainder_sets[:num_sets_to_include]
    # Return the contracted knowledge base
    return contracted_kb
