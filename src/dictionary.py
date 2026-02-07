def po_signature(po):
    return (frozenset(po.nodes), frozenset(po.edges))

def build_dictionary(candidate_posets):
    dictionary = {}
    reverse_dictionary = {}

    for po in candidate_posets:
        sig = po.signature()
        if sig not in dictionary:
            idx = len(dictionary)
            dictionary[sig] = idx
            reverse_dictionary[idx] = po
    
    return dictionary, reverse_dictionary

def trace_signature(trace):
    """
    Converts a trace into a comparable signature.
    For now, this assumes total order.
    """
    nodes = set(trace)
    edges = set()

    for i in range(len(trace)):
        for j in range(i + 1, len(trace)):
            edges.add((trace[i], trace[j]))
    
    return (frozenset(nodes), frozenset(edges))

