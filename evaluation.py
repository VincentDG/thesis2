import json
import gzip
import os
import time
import networkx as nx

OUTPUT_PATH = "output.json.gz"

dirname = os.path.dirname(__file__)
dataset_folder = "Sepsis Cases - Event Log_1_all"
dataset_filename = "Sepsis Cases - Event Log.xes.gz"
rel_path = os.path.join(dirname, 'Datasets', dataset_folder, dataset_filename)

ORIGINAL_PATH = rel_path 

# --- Size ---
def measure_size(original_path, compressed_path):
    original_bits = os.path.getsize(original_path) * 8
    compressed_bits = os.path.getsize(compressed_path) * 8

    bpb = compressed_bits / original_bits
    compression_factor = original_bits / compressed_bits
    space_saving = (1 - bpb) * 100

    print(f"Original:           {original_bits} bits")
    print(f"Compressed:         {compressed_bits} bits")
    print(f"BPB:                {bpb:.6f}")
    print(f"Compression factor: {compression_factor:.4f}")
    print(f"Space saving:       {space_saving:.2f}%")

# --- Speed ---
def measure_speed(original_path, compressed_path):
    original_mb = os.path.getsize(original_path) / (1024 * 1024)
    compressed_mb = os.path.getsize(compressed_path) / (1024 * 1024)

    # Read and decompress output.json.gz, measure throughput
    start = time.perf_counter()
    with gzip.open(compressed_path, 'rt', encoding='utf-8') as f:
        json.load(f)
    end = time.perf_counter()

    elapsed = end - start
    throughput = compressed_mb / elapsed

    print(f"Decompression time: {elapsed:.4f} seconds")
    print(f"Throughput:         {throughput:.4f} MB/s")

# --- Correctness ---
def measure_correctness(compressed_path):
    with gzip.open(compressed_path, 'rt', encoding='utf-8') as f:
        data = json.load(f)

    all_correct = True
    for grp_idx, group in enumerate(data["groups"]):
        # Reconstruct original traces from trace_counts
        original_traces = set()
        for trace_str in group["trace_counts"].keys():
            original_traces.add(trace_str)

        # Reconstruct linear extensions from poset cover
        generated_traces = set()
        for poset in group["poset_cover"]:
            G = nx.DiGraph()
            G.add_nodes_from(poset["nodes"])
            G.add_edges_from([tuple(e) for e in poset["edges"]])
            for sorting in nx.all_topological_sorts(G):
                generated_traces.add(str(tuple(sorting)))

        if original_traces == generated_traces:
            print(f"Group {grp_idx}: Correct")
        else:
            print(f"Group {grp_idx}: MISMATCH")
            print(f"  Original:  {original_traces}")
            print(f"  Generated: {generated_traces}")
            all_correct = False

    if all_correct:
        print("\nAll groups correct!")
    else:
        print("\nSome groups have mismatches.")

    return all_correct

def check_event_sets(compressed_path):
    with gzip.open(compressed_path, 'rt', encoding='utf-8') as f:
        data = json.load(f)
    
    all_correct = True
    for grp_idx, group in enumerate(data["groups"]):
        event_set = set(tuple(group["event_set"]))
        le_str = list(group["trace_counts"].keys())[0][1:-1].split(", ")
        le_set = set(tuple([int(x) for x in le_str]))

        if event_set == le_set:
            print(f"Group {grp_idx}: Correct")
        else:
            print(f"Group {grp_idx}: MISMATCH")
            print(f"  Event set:  {event_set}")
            print(f"  Extension: {le_set}")
            all_correct = False
    if all_correct:
        print("\nAll groups correct!")
    else:
        print("\nSome groups have mismatches.")

# --- Run all ---
if __name__ == "__main__":
    print("=== SIZE ===")
    measure_size(ORIGINAL_PATH, OUTPUT_PATH)
    print("\n=== SPEED ===")
    measure_speed(ORIGINAL_PATH, OUTPUT_PATH)
    print("\n=== CORRECTNESS ===")
    measure_correctness(OUTPUT_PATH)