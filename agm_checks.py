from sympy import *


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

