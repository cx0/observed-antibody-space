### Query Observed Antibody Space database

This is a toy repo to assess various options to build a performant database to query Observed Antibody Space (OAS) sequence database.

#### Option 1: DuckDB

```bash
# Download a random subset of unpaired sequences available on OAS
# wget batch download script (N=15083 unpaired sequences)
mkdir oas_subset
cd oas_subset/
sort -R bulk_download.sh | head -n150 | bash -

# extract and append metadata for downstream uniform processing
python expand_csv.py

# combine compressed csv files and write to a parquet file using DuckDB
python load_duckdb.py
```

```bash
# example query: retrieve unique aligned amino acid sequences by specific chain and species
./duckdb
D SELECT DISTINCT (sequence_alignment_aa), Species, "Chain" FROM 'oas_subset_db/ab_seq.parquet' AS tbl
> WHERE tbl.Species = 'human' AND tbl."Chain" = 'Heavy'
> GROUP BY sequence_alignment_aa, Species, "Chain"
> LIMIT 5;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬─────────┬─────────┐
│                                                     sequence_alignment_aa                                                     │ Species │  Chain  │
│                                                            varchar                                                            │ varchar │ varchar │
├───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼─────────┼─────────┤
│ VQLVESGGGVVQPGRSLRLSCAASGFTFSSYAMHWVRQAPGKGLEWVAVISYDGSNKYYADSVKGRFTISRDNSKNTLYLQMNSLRVEDTAVYYCAKSPGKDHGGNSGGFDIWGQGTMVTVSS   │ human   │ Heavy   │
│ QVHLVESGGGLVKPGGSLRLSCATSGFSFKDYYMNWVRQTPGKGLEWVSHISSSGTIKYYADSVKGRFTVSRDNAKKSLYLEMTSLRVDDTAVYYCARESTPWGGDYVGYGLDVWGRGTKVAVSS │ human   │ Heavy   │
│ EVQLVESGGGLVQPGGSLRLSCAASGFRFSNYWMSWVRQAPGKGLEWVANIKQDGNEKYSVDSVKGRFTISRDNAKNSLYLQMNSLRVEDTAVYYCAKSWHSGSLYDAFHIWGQGTMVTVS     │ human   │ Heavy   │
│ QVQLVESGGGVVQPGRSLRLSCAASGFTFSSYAMDWVRQAPGKGLEWVAVISYEGSNKYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCARVSGGNDYGDYAGAFDIWGQGTMVTVSS │ human   │ Heavy   │
│ VQLVESGGGLVQPGRSLRLSCAASGFTFDDYAMHWVRQAPGKGLEWVSGITWNSGSIGYADSVKGRFTISRDNAKNSLYLQMNSLRTEDTALYYCAKGLGWELLTHDAFDIWGQGTMVTVSS    │ human   │ Heavy   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴─────────┴─────────┘
D
```
