import gzip
import shutil
import os
import re
from checker import detect_exclusive_choices
from datetime import datetime as dt
import utilities
from itertools import permutations
from imports.app.posetsolver import PosetSolver
from imports.app.posetutils import PosetUtils
import json
import time

# This section of the code deals with relative file paths
dirname = os.path.dirname(__file__)
dataset_folder = "Sepsis Cases - Event Log_1_all"
dataset_filename = "Sepsis Cases - Event Log.xes.gz"
rel_path = os.path.join(dirname, 'Datasets', dataset_folder, dataset_filename)

# This section of the code decompresses datasets compressed with Gzip into XES files
with gzip.open(rel_path, 'rb') as f_in:
    with open(rel_path[:-3], 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# This section of the code opens the dataset
with open(rel_path[:-3], 'rb') as dataset:
    contents = dataset.read()
contents = str(contents)

# This section of the code looks for trace logs and saves the contents of each trace into an array
traces = []
i = 0
while re.search("<trace>", contents):
    x = re.search("<trace>", contents)
    y = re.search("</trace>", contents)
    start = x.start()
    i = y.end()
    traces.append(contents[start:i])
    contents = contents[i:]

# This section of the code looks through each trace to extract its name and saves it to an array
trace_metadata = []
for trace in traces:
    x = re.search("string key=\"concept:name\" value=\"", trace)
    x_end = x.end()
    name_end = re.search("\"/>", trace[x_end:])
    trace_name = trace[x_end:x_end + name_end.start()]
    trace_metadata.append(trace_name)

# This section of the code looks for events in each trace log and saves the contents of each event into an array of arrays
events = []
for trace in traces:
    i = 0
    event_log = []
    while re.search("<event>", trace):
        x = re.search("<event>", trace)
        y = re.search("</event>", trace)
        start = x.start()
        i = y.end()
        event_log.append(trace[start:i])
        trace = trace[i:]
    events.append(event_log)

# This section of the code extracts the name and timestamp of each event and saves it as a pair in an array
trace_events_metadata = []
for trace in events:
    events_metadata = []
    for event in trace:
        # extracting name
        x = re.search("string key=\"concept:name\" value=\"", event)
        x_end = x.end()
        name_end = re.search("\"/>", event[x_end:])
        event_name = event[x_end:x_end + name_end.start()]
        # extracting timestamp
        x = re.search("date key=\"time:timestamp\" value=\"", event)
        x_end = x.end()
        date_end = re.search("\"/>", event[x_end:])
        event_date = event[x_end:x_end + date_end.start()]
        metadata = [event_name, event_date]
        events_metadata.append(metadata)
    trace_events_metadata.append(events_metadata)

# This section of the code checks for duplicate events (looping)
# nl means No Loops
nl_traces = []
for trace in trace_events_metadata:
    seen = set()
    for event in trace:
        if event[0] not in seen:
            seen.add(event[0])
        else:
            break
    if len(seen) == len(trace):
        nl_traces.append(trace)

# This section of the code formats the timestamp into a manipulable object
# dt means datetime 
date_format = "%Y-%m-%dT%H:%M:%S.%f"
dt_traces = []
for trace in nl_traces:
    events = []
    for event in trace:
        date_object = dt.strptime(event[1][:-6], date_format) #make sure this works for other datasets
        new_event = [event[0], date_object]
        events.append(new_event)
    dt_traces.append(events)


# REMEMBER: check for concurrent events
# This section groups traces via the set of events they have
# grp means Grouped
event_sets = []
grp_traces = []
for trace in dt_traces:
    event_names = set()
    for event in trace:
        event_names.add(event[0])
    if event_names not in event_sets:
        event_sets.append(event_names)
        grp_traces.append([trace])
    else:
        for x in event_sets:
            if event_names == x:
                grp_traces[event_sets.index(x)].append(trace)

# This section of the code sorts the events of each trace in chronological order
# co means Chronologically Ordered
co_grp_traces = []
for grp in grp_traces:
    co_traces = []
    for trace in grp:
        co_events = sorted(trace, key = lambda event:event[1])
        co_traces.append(co_events)
    co_grp_traces.append(co_traces)

# This section populates the event dictionary
event_dict = {}
event_idx = 0
for group in co_grp_traces:
    for trace in group:
        for event in trace:
            if event[0] not in event_dict:
                event_dict[event[0]] = event_idx 
                event_idx += 1

# This section creates the linear orders from the co_grp_traces, event_dict and concurrency_list
grouped_linear_orders = []
for group in co_grp_traces:
    linear_orders = []
    for trace in group:
        linear_order = []
        for event in trace:
            event_number = event_dict[event[0]]
            linear_order.append(event_number)
        linear_orders.append(linear_order)    
    grouped_linear_orders.append(linear_orders)

# This section of the code checks for concurrent events
# Detect concurrency by checking if timestamp is equivalent
# New concurrency algorithm puts them in a blocks instead of pairwise

concurrency_list = []

for grp_no in range(len(co_grp_traces)):
    curr_grp = co_grp_traces[grp_no]
    for trace_no in range(len(curr_grp)):
        current_block = [0]
        trace = co_grp_traces[grp_no][trace_no]

        for i in range(1, len(trace)):
            if trace[i][1] == trace[i-1][1]:
                current_block.append(i)
            else:
                if len(current_block) > 1:
                    concurrency_list.append([grp_no, trace_no, current_block])
                current_block = [i]
        
        if len(current_block) > 1:
            concurrency_list.append([grp_no, trace_no, current_block])

# Map index from concurrency list to its actual event
c_no = 0
for concurrency in concurrency_list:
    grp_no, trace_no, indices = concurrency[0], concurrency[1], concurrency[2]
    linear_order = grouped_linear_orders[grp_no][trace_no]
    concurrent_events = []
    for c_index in indices:
        event_no = linear_order[c_index]
        concurrent_events.append(event_no)
    
    # Generate permutations
    p = list(permutations(concurrent_events))

    # Insert permutations to linear orders
    linear_extensions = []
    for permutation in p:
        new_order = linear_order.copy()
        for idx, val in zip(indices, permutation):
            new_order[idx] = val
        linear_extensions.append(new_order)
    
    grp = grouped_linear_orders[grp_no]

    # Insert to group
    for extension in linear_extensions:
        grp.append(extension)

    c_no += 1

# This section of the code is for solving each instance of the poset cover problem
hasse_diagram_list = []
grp_no = 0
for group in grouped_linear_orders:   
    upsilon = [tuple(order) for order in group]                 # Converted to tuple to support networkX
    result_linear_orders = PosetSolver.minimum_poset_cover(upsilon)
    result_posets = [
        PosetUtils.get_partial_order_of_convex(leg) for leg in result_linear_orders
    ]
 
    ## !!! potential error coming from here !!!
    ## This section of the code gets the Hasse diagram of each poset in the poset cover (simply to apply transitive reduction)
    hasse_posets = []
    for result in result_posets:
        hasse = PosetUtils.get_hasse_from_partial_order(result, group[0])  
        hasse_posets.append(hasse)
    
    # This section of the code verifies the correctness of the solutions
    # This is done by obtaining linear extensions from cover relations
    # Print linear extensions, and compare to stored set of linear extensions
    print("This is Poset Block: " + str(grp_no))
    utilities.check_solution_to_instance(upsilon, hasse_posets)
    grp_no += 1

    ## This section of the code appends the Hasse diagrams of each poset block to the master list
    hasse_diagram_list.append(hasse_posets)

# Outputting
groups = []
for group_idx, poset_block in enumerate(hasse_diagram_list):
    group = grouped_linear_orders[group_idx]

    trace_counts = {}
    for trace in group:
        key = str(tuple(trace))
        trace_counts[key] = trace_counts.get(key, 0) + 1
    
    poset_cover = []
    for hasse in poset_block:
        poset_cover.append({
            "nodes": list(hasse.nodes()),
            "edges": [list(e) for e in hasse.edges()]
        })
    
    groups.append({
        "event_set": list(set(e for trace in group for e in trace)),
        "trace_counts": trace_counts,
        "poset_cover": poset_cover
    })

# Invert event_dict for output (int -> name)
inverted_dict = {str(v): k for k, v in event_dict.items()}

output = {
    "event_dictionary": inverted_dict,
    "groups": groups
}

output_path = "output.json.gz"
with gzip.open(output_path, 'wt', encoding='utf-8') as f:
    json.dump(output, f)

print(f"Output written to {output_path}")