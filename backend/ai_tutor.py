def introduce_experiment(subject, experiment, class_group):
    if class_group == "Group_1":
        level = "simple"
    else:
        level = "advanced"

    intro = f"""
    Welcome to the virtual lab!

    Today we will perform the experiment: {experiment}.
    Subject: {subject}

    I will guide you step-by-step and help you if you make mistakes.
    Let's begin!
    """

    return intro.strip()


def explain_concept(subject, experiment, class_group):
    if experiment == "Ohm's Law":
        if class_group == "Group_1":
            return (
                "Ohm's Law explains the relationship between voltage, current, "
                "and resistance. When voltage increases, current also increases."
            )
        else:
            return (
                "Ohm's Law states that current is directly proportional to voltage "
                "when resistance remains constant, mathematically represented as V = IR."
            )

    return "Concept explanation will be provided during the experiment."
