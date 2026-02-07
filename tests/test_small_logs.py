from src.log_loader import load_log_from_list
from src.partial_order import trace_to_po

def test_simple_trace():
    toy_log = [
        ["A", "B", "C"],
        ["A", "C", "B"],
        ["A", "B", "C"]
    ]

    log = load_log_from_list(toy_log)
    pos = trace_to_po(log[0])
    
    assert ("A", "B") in pos.edges