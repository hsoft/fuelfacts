def unsource(facts):
    """Simplifies `facts` dict by replacing the value/source dict with just the value.

    It doesn't actually changes the dict, but return a deep copy.
    """
    if not isinstance(facts, dict):
        return facts
    elif {'value', 'source'}.issubset(set(facts.keys())):
        return facts['value']
    else:
        return {k: unsource(v) for k, v in facts.items()}

