import json
from src.dictionary import trace_signature

def encode_traces(event_log, dictionary):
    """
    Input:
        - event_log: EventLog (list of traces)
        - dictionary: { signature -> id }
    
    Output:
        - encoded_traces: list of list[int]
          Each trace is represented as a list of dictionary IDs
    """
    encoded_traces = []

    for trace in event_log:
        # Baseline assumption
        # One trace == one poset
        signature = trace_signature(trace)

        if signature not in dictionary:
            raise ValueError("Trace signature not found in dictionary")
        
        encoded_traces.append([dictionary[signature]])

    return encoded_traces


def encode_to_json(dictionary, encoded_traces, path):
    json_dict = {
        "dictionary": {},
        "traces": encoded_traces
    }

    for po, pid in dictionary.items():
        json_dict["dictionary"][pid] = {
            "nodes": list(po.nodes),
            "edges": list([a, b] for a, b in po.edges)
        }
    
    with open(path, "w") as f:
        json.dump(json_dict, f, indent=2)