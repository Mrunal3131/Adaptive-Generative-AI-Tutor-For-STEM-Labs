def get_hint(level, experiment):
    hints = {
        "Ohm's Law": [
            "Think about relation between voltage and current.",
            "V = I × R",
            "Increase voltage and observe current."
        ],
        "Osmosis": [
            "Water moves from high concentration to low.",
            "Semi permeable membrane is required.",
            "Compare inside and outside solution."
        ]
    }
    return hints.get(experiment, ["Try again"])[level]
