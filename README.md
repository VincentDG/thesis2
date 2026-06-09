# Poset Cover-Based Event Log Compressor

The poset cover-based event log compressor are scripts for performing poset cover based compression for event log (.XES) files.

## Prerequisites
1. Please make sure you have **Python 3.12+** installed.

## Setup Instructions (as of 6/9/2026)
1. Clone the repository

```git clone https://github.com/VincentDG/event-log-poset-compression```

2. Install dependencies

```pip install -r requirements.txt```

3. Select dataset by editing `parser.py`
- If you have Datasets.zip, please extract it on the root folder and proceed to step 4.
- Otherwise, create a folder named `Datasets` on the root folder.
- Add the dataset folder and on dataset filename on the dictionary in `parser.py`.

4. Change parser parameters
- On `parser.py` change the value of `var` to the dataset to be compressed. Please ensure that the variable indicated in `var` is in `dataset_folder` and `dataset_filename` exist and are the same. 

5. Run `parser.py`

```python3.12 parser.py```

6. Check for results for filesizes can be checked using File Explorer.

7. Run `evaluation.py`
Note: `evaluation.py` is outdated, only the decompression time is the metric used in the final paper.

