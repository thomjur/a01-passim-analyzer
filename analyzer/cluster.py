import pandas as pd


def parse_cluster_from_jsonl(filename: str):
    '''Function to parse all TRD clusters from a JSONL file
    from passim. Each cluster is stored in a separate .csv file
    for further processing.'''
    df = pd.read_json(filename, lines=True)
    # WARNING: We get huge conversion errors between INT and FLOAT later on when handling the
    # pd.merge with a left join; to handle this, we save two dataframes: one with all source entries (and empty src fields)
    # and the another one with references to previous texts
    # First, we save the dataframe with source texts
    df_sources = df.loc[~df["src"].astype(bool),:]
    df_sources.to_csv("analyzer/output/sources.csv")
    # Next, we continue with the rest of the data
    df = df.loc[df["src"].astype(bool),:]
    # First creating an intermediary JSON Array (maybe this is not even necessary)
    dicts_list = df.to_dict("records")
    # We flatten the records in the src field and take uid+cluster as a unique id to the row
    df_src = pd.json_normalize(dicts_list, record_path="src", meta=["uid", "cluster"], record_prefix="src_")
    # We are merging both dataframes on uid+cluster
    # For each reference from a target to a source text, there should be a single row now
    df_merged = pd.merge(df.drop(columns="src"), df_src, on=["uid", "cluster"], how="inner")
    print(df_merged.info())
    # We are saving every cluster in a separate CSV file for now
    cluster_list = df_merged["cluster"].unique()
    grouped = df_merged.groupby("cluster")
    for grp in cluster_list:
        df_grouped = grouped.get_group(grp)
        df_grouped = df_grouped[["cluster", "uid", "begin", "end", "tafsir_id", "tafsir_title", "author_name", "author_place_of_death", "author_death_dce", "text", "src_uid", "src_begin", "src_end"]]
        # We need to cast uids to int otherwise we get comparison errors later
        df_grouped["src_uid"] = df_grouped["src_uid"].fillna(-1).astype(int)        
        df_grouped.to_csv(f"analyzer/output/{grp}.csv")


def parse_pairwise_from_jsonl(filename: str):
    '''Retrieving pairwise alignments created with passim --pairwise from JSONL.'''
    df = pd.read_json(filename, lines=True)
    df_filtered = df[["uid", "uid2", "s1", "s2"]]
    df_filtered.to_csv("analyzer/output/pairwise.csv")
