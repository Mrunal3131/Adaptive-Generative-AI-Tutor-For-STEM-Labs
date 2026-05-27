def simulate_ohms_law(voltage, resistance=10):
    if voltage < 0:
        return {
            "error": "Voltage cannot be negative"
        }

    current = voltage / resistance
    brightness = min(current * 10, 100)  # brightness in %

    return {
        "voltage": voltage,
        "resistance": resistance,
        "current": round(current, 2),
        "brightness": round(brightness, 2)
    }
