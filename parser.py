import gzip
import shutil
import os
import re
from checker import detect_exclusive_choices
from datetime import datetime as dt
import random

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

for trace in trace_events_metadata[0]:
    print(trace)
    
exclusive_pairs = detect_exclusive_choices(trace_events_metadata)
print("Exclusive choices:", exclusive_pairs)
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

# This section of the code checks for concurrent events
# Detect concurrency by checking if timestamp is equivalent
# If concurrency is detected between events, two linear orders are created
concurrency_list = []
for grp in grp_traces:
    for trace in grp:
        for x in range(len(trace)-1):
            for y in range(x+1, len(trace)):
                if trace[x][1] == trace[y][1]:
                    # Format: [grp_index, trace_index, event_index_1, event_index_2]
                    concurrency_list.append([grp_traces.index(grp), grp.index(trace), x, y])
