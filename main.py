from sympy import *
from itertools import combinations


def pl_resolution(kb, alpha): # same as in book figure 7.13
    combined_cnf = And(to_cnf(kb), to_cnf(Not(alpha)))

    clauses = set(combined_cnf.args)
    new_clauses = set()

    while True:
        pairs = list(combinations(clauses, 2))
        for (Ci, Cj) in pairs:
            resolvents = pl_resolve(Ci, Cj)
            if resolvents == {False}:  # contradiction
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


a = symbols('a')
b = symbols('b')

expression1 = (a >> b) & a
expression2 = b

print(pl_resolution(expression1, expression2))
