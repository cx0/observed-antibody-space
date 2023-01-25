import os
import json
import pandas as pd

# append metadata as columns
def append_metadata(path_ab_file):
    cols = ",".join(pd.read_csv(path_ab_file, nrows=0).columns)
    data = pd.read_csv(path_ab_file, header=0, skiprows=1)
    num_rows = data.shape[0]

    # json normalize the dict containing metadata
    x = pd.json_normalize(json.loads(cols))

    # keep relevant attributes (available via OAS search)
    # "Metadata: Run, Species, BSource, BType, Disease, Vaccine, Subject, Chain, Isotype"
    x = x[
        [
            "Run",
            "Species",
            "BSource",
            "BType",
            "Disease",
            "Vaccine",
            "Subject",
            "Chain",
            "Isotype",
        ]
    ]

    # expand data as to include metadata and return merged dataframe
    x = pd.concat([x] * num_rows, ignore_index=True)

    # relevant columns from data
    # "Per-entry: sequence_alignment_aa, germline_alignment_aa, v_call, d_call, j_call, ANARCI_status"
    rel_cols = [
        "sequence_alignment_aa",
        "germline_alignment_aa",
        "v_call",
        "d_call",
        "j_call",
        "ANARCI_status",
    ]

    return pd.concat([data[rel_cols], x], axis=1)


# gzip compressed sample files (n=150; ~1% of unpaired sequences)
data_dir = "oas_subset/"

# output directory for the expanded data
output_dir = "oas_subset_expanded/"

for ab_file in os.listdir(data_dir):
    if os.path.isfile(output_dir + ab_file):
        pass
    else:
        y = append_metadata(data_dir + ab_file)
        y.to_csv(output_dir + ab_file, index=False, compression="gzip")
        # optional: write to parquet (dependency: pyarrow)
