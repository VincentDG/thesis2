import gzip
import shutil
import os
import re

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
