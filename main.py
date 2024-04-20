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

print(revise(expression1, expression2))
