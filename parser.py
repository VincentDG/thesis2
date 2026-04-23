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

# t0 = time.perf_counter()
# print("Breakpoint A")


# t1 = time.perf_counter()
# print(f"Breakpoint B - {t1-t0:.2f}s")


# This section of the code deals with relative file paths
dirname = os.path.dirname(__file__)
var = 'G1'   # change this variable to match the dataset used
dataset_folder = {
    'A': "Sepsis Cases - Event Log_1_all",
    'B': "Road Traffic Fine Management Process_1_all",
    'D': "BPI Challenge 2017_1_all",
    'E': "BPI Challenge 2018_1_all",
    'G1': "BPI Challenge 2020_ Domestic Declarations_1_all",
    'G2': "BPI Challenge 2020_ International Declarations_1_all",
    'G3': "BPI Challenge 2020_ Prepaid Travel Costs_1_all",
    'G4': "BPI Challenge 2020_ Request For Payment_1_all",
    'G5': "BPI Challenge 2020_ Travel Permit Data_1_all"
}

dataset_filename = {
    'A': "Sepsis Cases - Event Log.xes.gz",
    'B': "Road_Traffic_Fine_Management_Process.xes.gz",
    'D': "BPI Challenge 2017.xes.gz",
    'E': "BPI Challenge 2018.xes.gz",
    'G1': "DomesticDeclarations.xes.gz",
    'G2': "InternationalDeclarations.xes.gz",
    'G3': "PrepaidTravelCost.xes.gz",
    'G4': "RequestForPayment.xes.gz",
    'G5': "PermitLog.xes.gz"
}

rel_path = os.path.join(dirname, 'Datasets', dataset_folder[var], dataset_filename[var])

# This section of the code decompresses datasets compressed with Gzip into XES files
# The previous code was optimized to skip file decompression to disk and just reads the contents of the .gz file.
with gzip.open(rel_path, 'rt', encoding='utf-8') as f:
    contents = f.read()

# This section of the code looks for trace logs and saves the contents of each trace into an array
# The change is an optimized version of the search algorithm that goes through all the traces in one pass and stops string copying.
traces = []
traces = re.findall(r"<trace>.*?</trace>", contents, re.DOTALL)
print("Number of traces before preprocessing: " + str(len(traces)))

# This section of the code looks through each trace to extract its name and saves it to an array
event_log = {
    "traces": {
        "metadata": [],
        "events": {
            "metadata": [],
            "contents": []
        }
    }
 }

def extract_attribute(text, key):
    """Fallback extractor for logs using ></tag> closing style."""
    pattern = f'key="{key}" value="([^"]*)"'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def get_trace_name(trace):
    # Try stable approach first
    x = re.search("string key=\"concept:name\" value=\"", trace)
    if x:
        x_end = x.end()
        name_end = re.search("\"/>", trace[x_end:])
        if name_end:
            return trace[x_end:x_end + name_end.start()]
    # Fallback for ></string> closing style
    return extract_attribute(trace, "concept:name")

def get_event_name(event):
    x = re.search("string key=\"concept:name\" value=\"", event)
    if x:
        x_end = x.end()
        name_end = re.search("\"/>", event[x_end:])
        if name_end:
            return event[x_end:x_end + name_end.start()]
    return extract_attribute(event, "concept:name")

def get_event_timestamp(event):
    x = re.search("date key=\"time:timestamp\" value=\"", event)
    if x:
        x_end = x.end()
        date_end = re.search("\"/>", event[x_end:])
        if date_end:
            return event[x_end:x_end + date_end.start()]
    return extract_attribute(event, "time:timestamp")

# This section of the code looks for events in each trace log and saves the contents of each event into an array of arrays
# Trace name extraction
for trace in traces:
    trace_name = get_trace_name(trace)
    if trace_name is None:
        continue
    event_log["traces"]["metadata"].append(trace_name)
    event_contents = re.findall(r"<event>.*?</event>", trace, re.DOTALL)
    event_log["traces"]["events"]["contents"].append(event_contents)

# This section of the code extracts the name and timestamp of each event and saves it as a pair in an array
for trace in event_log["traces"]["events"]["contents"]:
    events_metadata = []
    for event in trace:
        event_name = get_event_name(event)
        event_date = get_event_timestamp(event)
        if event_name is None or event_date is None:
            continue
        events_metadata.append([event_name, event_date])
    event_log["traces"]["events"]["metadata"].append(events_metadata)

# # DEBUG - check first trace's events
# if event_log["traces"]["events"]["metadata"]:
#     print("First trace events:", event_log["traces"]["events"]["metadata"][0])
# else:
#     print("No events parsed at all")

# After event extraction, before cycle detection
print("Trace count:", len(event_log["traces"]["metadata"]))
print("Event content count:", len(event_log["traces"]["events"]["contents"]))
print("Event metadata count:", len(event_log["traces"]["events"]["metadata"]))
print("First trace event count:", len(event_log["traces"]["events"]["contents"][0]))
print("First trace metadata count:", len(event_log["traces"]["events"]["metadata"][0]))

# This section of the code checks for duplicate events (looping)
# nl means No Loops
nl_traces = []
trace_ids = []
for idx_trace, trace in enumerate(event_log["traces"]["events"]["metadata"]):
    seen = set()
    for event in trace:
        if event[0] not in seen:
            seen.add(event[0])
        else:
            break
    if len(seen) == len(trace):
        nl_traces.append(trace)
        trace_ids.append(event_log["traces"]["metadata"][idx_trace])

print("Number of traces after preprocessing:", len(nl_traces))


# This section of the code formats the timestamp into a manipulable object
# dt means datetime 
date_formats = [
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S"
]

def parse_timestamp(timestamp_str):
    # Remove timezone offset
    clean = re.sub(r'([+-]\d{2}:\d{2}|Z)$', '', timestamp_str)
    for fmt in date_formats:
        try:
            return dt.strptime(clean, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized timestamp format: {timestamp_str}")    

dt_traces = []
for trace in nl_traces:
    events = []
    for event in trace:
        date_object = parse_timestamp(event[1]) 
        new_event = [event[0], date_object]
        events.append(new_event)
    dt_traces.append(events)


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

print("Number of concurrencies:", len(concurrency_list))

# Map index from concurrency list to its actual event
c_no = 0
l = 0
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
        l += 1
    
    grp = grouped_linear_orders[grp_no]

    # Insert to group
    for extension in linear_extensions:
        grp.append(extension)

    c_no += 1

print("Number of generated permutations:", l)

# This section of the code is for solving each instance of the poset cover problem
THRESHOLD = 20 # to be decided

hasse_diagram_list = []
total_groups = len(grouped_linear_orders)
upsilon_sum = 0
for grp_idx, group in enumerate(grouped_linear_orders):
    t_start = time.perf_counter()

    upsilon = list(set([tuple(order) for order in group]))      # Optimization: deduplicates upsilon before passing it in.

    # t_solving_start = time.perf_counter()
    # print(f"Group {grp_idx + 1}/{total_groups} — {len(group)} traces, "
    #   f"{len(upsilon)} unique — solving...")
    

    # if len(upsilon) > THRESHOLD:
    #     print(f"Group {grp_idx + 1} skipped - too many unique traces")
    #     hasse_diagram_list.append([])
    #     continue

    result_linear_orders = PosetSolver.minimum_poset_cover(upsilon)
    
    # t_solving_end = time.perf_counter()
    # print(f"[{dt.now().strftime('%H:%M:%S')}] Group {grp_idx + 1}/{total_groups} — "
    #       f"solved in {t_solving_end - t_solving_start:.2f}s")
    
    result_posets = [
        PosetUtils.get_partial_order_of_convex(leg) for leg in result_linear_orders
    ]
 
    ## This section of the code gets the Hasse diagram of each poset in the poset cover (simply to apply transitive reduction)
    hasse_posets = []
    for result in result_posets:
        hasse = PosetUtils.get_hasse_from_partial_order(result, group[0])  
        hasse_posets.append(hasse)
    
    ## This section of the code appends the Hasse diagrams of each poset block to the master list
    hasse_diagram_list.append(hasse_posets)

    t_end = time.perf_counter()
    print(f"Group {grp_idx + 1}/{total_groups} — {len(group)} traces, "
          f"{len(hasse_posets)} posets — {t_end - t_start:.2f}s")

    upsilon_sum += len(upsilon)

print("Summation of Upsilon: ", upsilon_sum)

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

print("Group length:", len(groups))
print("Number of linear orders: " + str(lo_count)) # obtained by summating the len of upsilon for all groups

output_path = "output.json.gz"
with gzip.open(output_path, 'wt', encoding='utf-8') as f:
    json.dump(output, f)

print(f"Output written to {output_path}")

# This part of the code iterates through the original array of traces, and trimming traces whose IDs are not in trace_ids
# which is the set of traces representable as posets
trimmed_input = []
trace_ids_set = set(trace_ids)
for trace in traces:
    trace_name = extract_attribute(trace, "concept:name")
    if trace_name in trace_ids_set:
        trimmed_input.append(trace)

# Changed output of dataset to a .xes file.
### This part of the code extracts everything before the first trace (<trace>)
###first_trace = re.search("<trace>", contents)
###log_header = contents[:first_trace.start()]

### This part of the code extracts everything after the last trace (</trace>)
###last_trace_end = contents.rfind("</trace>")
###log_footer = contents[last_trace_end + len("</trace>"):]

# Reconstructing the trimmed XES
trimmed_xes = "".join(trimmed_input)
trimmed_xes_path = "trimmed_input.xes.gz"
with gzip.open(trimmed_xes_path, 'wt', encoding='utf-8') as f:
    f.write(trimmed_xes)

print(f"Trimmed dataset written to {trimmed_xes_path}")