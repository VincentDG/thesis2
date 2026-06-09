# Poset Cover-Based Event Log Compressor

The poset cover-based event log compressor are scripts for performing poset cover based compression for event log (.XES) files.

## Prerequisites
- Please make sure you have **Python 3.12+** installed.

## Setup Instructions (as of 6/9/2026)
1. Clone the repository

    ```
    git clone https://github.com/VincentDG/event-log-poset-compression
    ```


2. Install dependencies
    ```
    python3.12 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. Select dataset by editing `parser.py`
    - If you have Datasets.zip, please extract it on the root folder and proceed to step 4.
    - Otherwise, create a folder named `Datasets` on the root folder.
    - Add the dataset folder and on dataset filename on the dictionary in `parser.py`.
<br>

4. Change `parser.py` parameters
    - On `parser.py`, change the value of `var` to the dataset to be compressed.
    - If you are importing a new dataset, please ensure that the variable indicated in `var` is in `dataset_folder` and `dataset_filename` exist and are the same.
        - Zipped datasets: Make sure that they have the extension `.xes.gz`.
        - Unzipped datasets: Make sure that their extension is `.xes`, please edit the `unzipped` variable in `parser.py` to include the `var` value of `dataset_folder` and `dataset_filename`.

5. Run `parser.py`

    ```
    python3.12 parser.py
    ```

6. Check for results for filesizes can be checked using File Explorer.
   - The modified XES file is located in `trimmed_input.xes.gz`.
   - The resulting compressed JSON file is located in `output.json.gz`.

7. Extract `trimmed_input.xes.gz` and `output.json.gz` to the root folder.
   
8. Run `evaluation.py`. <br>
   - Please ensure that `var` is the same as the one used in `parser.py`.
   - Here, the decompression time and correctness can be verified.

