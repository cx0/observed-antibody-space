import duckdb

# combine compressed files and write to a parquet file
con = duckdb.connect(database=":memory:")

con.execute("PRAGMA threads=10;")

query_str = """
    CREATE OR REPLACE TABLE ab_seq
    AS SELECT * FROM read_csv_auto("oas_subset_expanded/*.csv.gz", delim=",", header=True);
"""

result = con.execute(query_str).fetchall()

print(result)
# [(9296476,)]

con.execute(
    "EXPORT DATABASE 'oas_subset_db' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000);"
)

con.close()
