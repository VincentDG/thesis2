from src.partial_order import trace_to_po

def mine_candidate_posets(event_log):
    """
    Input: EventLog (list of traces)
    Output: list of PartialOrder objects
    """
    candidate_posets = []
    
    for trace in event_log:
        po = trace_to_po(trace)
        candidate_posets.append(po)

    return candidate_posets