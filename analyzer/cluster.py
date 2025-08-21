import pandas as pd

def parse_cluster_from_jsonl(filename: str):
    '''Function to parse all TRD clusters from a JSONL file
    from passim. Each cluster is stored in a separate .csv file
    for further processing.'''
    df = pd.read_json(filename, lines=True)
    # DEBUG
    df.to_csv("full.csv")
    dicts_list = df.to_dict("records")
    df_src = pd.json_normalize(dicts_list, record_path="src", meta=["uid", "cluster"], record_prefix="src_")
    df_src.to_csv("src.csv")
    # We are merging both dataframes
    df_merged = pd.merge(df.drop(columns="src"), df_src, on=["uid", "cluster"], how="left")
    df_merged.to_csv("merged.csv")
    # We are just saving every cluster in a separate CSV file for now
    cluster_list = df_merged["cluster"].unique()
    grouped = df_merged.groupby("cluster")
    for grp in cluster_list:
        df_grouped = grouped.get_group(grp)
        df_grouped = df_grouped[["cluster", "uid", "begin", "end", "tafsir_id", "tafsir_title", "author_name", "author_place_of_death", "author_death_dce", "text", "src_uid", "src_begin", "src_end"]]
        df_grouped.to_csv(f"analyzer/output/{grp}.csv")
