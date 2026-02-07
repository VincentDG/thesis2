from pm4py.objects.log.importer.xes import importer as xes_importer

Trace = list[str]
EventLog = list[Trace]

def load_log_from_list(log):
    """
    Input: List of traces (each trace is a list of event labels)
    Output: EventLog
    """
    assert isinstance(log, list)
    return log

# ignore this for now
def load_xes(path):
    log = xes_importer.apply(path)
    return [[event["concept:name"] for event in trace] for trace in log]
