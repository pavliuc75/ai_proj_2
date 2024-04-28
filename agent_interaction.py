from sympy import *
from belief_manager import include_belief, show_beliefs, reset_beliefs, knowledge_base
from agm_checks import *

# Function to capture the user's command
def user_command():
    print("\nYou can:")
    print("1) Add a belief")
    print("2) Show beliefs")
    print("3) Reset the belief base")
    print("4) Check against AGM postulates")
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
                include_belief(belief_expr)
            except SympifyError:
                print("Could not interpret the belief.")
        elif user_choice == "2":
            show_beliefs()
        elif user_choice == "3":
            reset_beliefs()
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
