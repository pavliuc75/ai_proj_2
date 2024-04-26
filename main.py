from sympy import *
from itertools import combinations

class BeliefBase:
    def __init__(self):
        self.beliefs = set()

    def add_belief(self, belief):
        self.beliefs.add(belief)

    def remove_belief(self, belief):
        self.beliefs.discard(belief)

    def display_beliefs(self):
        print("Belief Base:")
        for belief in self.beliefs:
            print("-", belief)

    def logical_entailment(self, statement):
        for belief in self.beliefs:
            if self._resolve(belief, statement):
                return True
        return False


    def _resolve(self, belief, statement):
    # Check if statement is entailed by belief using resolution-based reasoning
        combined_cnf = And(to_cnf(belief), to_cnf(Not(statement)))
        print("Combined CNF:", combined_cnf)  # Print the combined CNF for debugging purposes
        result = combined_cnf == False
        print("Result:", result)  # Print the result for debugging purposes
        return result


    def contract(self, statement):
        print("Beliefs before contraction:", self.beliefs)
        if statement in self.beliefs:
            self.beliefs.remove(statement)
            print("Removed:", statement)
        if Not(statement) in self.beliefs:
            self.beliefs.remove(Not(statement))
            print("Removed:", Not(statement))
        print("Beliefs after contraction:", self.beliefs)# Remove the negation of the statement as well

    def expand(self, statement):
        self.beliefs.add(statement)

    def check_AGMP_postulates(self, belief, action):
        # AGM Success Postulate: If φ is already believed, it remains believed after revision.
        if action == 'revision':
            if belief in self.beliefs:
                return True
        # AGM Inclusion Postulate: If φ is believed after revision, it was either believed before or has been added.
        elif action == 'revision' or action == 'expansion':
            if belief in self.beliefs:
                return True
            else:
                return False
        # AGM Vacuity Postulate: If φ is not believed after contraction, it was not believed before.
        elif action == 'contraction':
            if belief not in self.beliefs:
                return True
            else:
                return False
        # AGM Consistency Postulate: After a revision, the new belief set is consistent if the new belief φ is consistent.
        elif action == 'revision':
            new_beliefs = self.beliefs.copy()
            new_beliefs.add(belief)
            combined_cnf = And(*[to_cnf(b) for b in new_beliefs])
            return combined_cnf != False
        # AGM Extensionality Postulate: Two belief sets remain identical after revision with logically equivalent sentences.
        elif action == 'revision':
            for b in self.beliefs:
                if Equivalent(b, belief) not in self.beliefs:
                    return False
            return True
        else:
            return False



def pl_resolution(KB, alpha):
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
                new_disjuncts = (_ci | _cj) - {i, j}
                resolvents.add(Or(*new_disjuncts) if new_disjuncts else False)
    return resolvents


def expand(KB, alpha):
    return And(KB, alpha)


def contract(KB, alpha):
    if Not(alpha) in KB.beliefs:
        KB.remove_belief(alpha)
        KB.remove_belief(Not(alpha))
    return KB


def revise(KB, alpha):
    if pl_resolution(KB, alpha):
        KB.contract(alpha)
        KB.contract(Not(alpha))
    return KB


a = symbols('a')
b = symbols('b')
c = symbols('c')

# Set up an initial list for storing beliefs
knowledge_base = BeliefBase()

def include_belief(knowledge_base, new_belief):
    if new_belief is not None:
        # Check if the belief or its negation is already present
        if new_belief in knowledge_base.beliefs:
            print("Belief already present:", new_belief)
            return
        if Not(new_belief) in knowledge_base.beliefs:
            print("Negation of belief already present:", Not(new_belief))
            # Remove the conflicting belief
            knowledge_base.beliefs.remove(Not(new_belief))

        # Add the new belief to the knowledge base
        knowledge_base.add_belief(new_belief)



# Show all beliefs in the knowledge base
def show_beliefs(knowledge_base):
    print("\nKnowledge Base Contains:")
    knowledge_base.display_beliefs()


# Remove all beliefs from the knowledge base
def reset_beliefs(knowledge_base):
    print("\nResetting the knowledge base")
    knowledge_base.beliefs.clear()

# Check logical entailment of a belief
def check_entailment(knowledge_base, belief):
    result = knowledge_base.logical_entailment(belief)
    print(f"The belief '{belief}' is entailed by the knowledge base: {result}")

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
# Interpret and convert user input to a symbolic expression
def interpret_belief(input_belief):
    belief_expr = sympify(str(input_belief))
    return belief_expr



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
            reset_beliefs(knowledge_base)
        elif user_choice == "4":
            belief_input = input("Enter the belief to check entailment: ")
            belief_expr = interpret_belief(belief_input)
            check_entailment(knowledge_base, belief_expr)
        elif user_choice == "5":
            stop_agent = True
        else:
            print("Action not recognized")

# Start interacting with the agent
interact_with_agent()
