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
print(events[0])