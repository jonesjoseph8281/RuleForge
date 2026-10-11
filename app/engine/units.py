# Utility for unit conversions if needed in the future
def to_mm(val: float, unit: str) -> float:
    if unit.lower() == 'm':
        return val * 1000
    if unit.lower() == 'cm':
        return val * 10
    return val

def to_ms(val: float, unit: str) -> float:
    return val
