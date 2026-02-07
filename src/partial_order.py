class PartialOrder:
    def __init__(self):
        self.nodes = set()
        self.edges = set()
    
    def add_event(self, event):
        self.nodes.add(event)

    def add_order(self, a, b):
        self.edges.add((a, b))

def trace_to_po(trace):
    po = PartialOrder()
    for e in trace:
        po.add_event(e)
    
    for i in range(len(trace)):
        for j in range(i+1, len(trace)):
            po.add_order(trace[i], trace[j])
    
    return po
