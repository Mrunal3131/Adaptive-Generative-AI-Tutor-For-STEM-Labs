def evaluate(answer, correct):
    if answer == correct:
        return 10, "Excellent understanding!"
    else:
        return 4, "Revise the concept and try again."
