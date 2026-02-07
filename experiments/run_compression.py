from src.log_loader import load_log_from_list
from src.poset_mining import mine_candidate_posets
from src.dictionary import build_dictionary
from src.encoder import encode_traces, encode_to_json


toy_log = [
    ["A", "B", "C"],
    ["A", "C", "B"]
]

event_log = load_log_from_list(toy_log)
candidate_posets = mine_candidate_posets(event_log)
dictionary, reverse_dictionary = build_dictionary(candidate_posets)

encoded_traces = encode_traces(toy_log, dictionary)

print(dictionary.items())
# print(encoded_traces)

# encode_to_json(dictionary, encoded_traces, "data/compressed/toy_log.json")