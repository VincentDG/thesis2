from collections import defaultdict
from itertools import combinations

def detect_exclusive_choices(event_log, threshold = 1.0):
    """
    Detect pairs of events that are in exclusive choice.

    Args:
        event_log: list of traces (each trace is a list of event names)
        threshold: fraction of traces that must obey exclusivity to count as choice (1.0 = strict)

    Returns:
        exclusive_pairs: set of tuples (event1, event2) that are in exclusive choice
    """

    # 1. Count co-occurrences
    co_occurrence = defaultdict(lambda: defaultdict(int))
    event_counts = defaultdict(int)
    num_traces = len(event_log)

    for trace in event_log:
        unique_events = set(event[0] for event in trace)
        for e in unique_events:
            event_counts[e] += 1
        for e1, e2 in combinations(unique_events, 2):
            co_occurrence[e1][e2] += 1
            co_occurrence[e2][e1] += 1
    
    # 2. Detect exclusive pairs
    exclusive_pairs = set()
    for e1, e2 in combinations(event_counts.keys(), 2):
        co_count = co_occurrence[e1].get(e2, 0)
        # Fraction of traces where both occur
        fraction = co_count / num_traces
        if fraction <= (1 - threshold):
            exclusive_pairs.add((e1, e2))

    return exclusive_pairs

