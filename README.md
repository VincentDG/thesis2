# thesis2 (tempname)

**thesis2 (tempname)** is a system that takes an event log and outputs a compressed file using poset covers which can be decompressed.

# MVP Pipeline
The minimum viable product for this project is achieved through the following pipeline:

```
Event Log
↓
Trace → Partial Orders
↓
Candidate Posets
↓
Dictionary Construction
↓
Trace Encoding
↓
Compressed File
↓
Decompression
```

# Project Structure
The structure of the project is as follows:
```
poset_compression/
|
├── data/
|    ├── raw_logs/
|    ├── compressed/
|    ├└── decompressed/
|
├── src/
|    ├── log_loader.py
|    ├── partial_order.py
|    ├── poset_mining.py
|    ├── dictionary.py
|    ├── encoder.py
|    ├── decoder.py
|    └── evaluation.py
|
├── experiments/
|    ├── run_compression.py
|    └── benchmarks.py
|
├── tests/
|    └── test_small_logs.py
|
└── README.md
```
