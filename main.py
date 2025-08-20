import pandas as pd


def main():
    df = pd.read_json("passim-data.json", lines=True)
    # We are just saving every cluster in a separate CSV file for now
    cluster_list = df["cluster"].unique()
    grouped = df.groupby("cluster")
    for grp in cluster_list:
        df_grouped = grouped.get_group(grp)
        df_grouped = df_grouped[["cluster", "uid", "tafsir_id", "tafsir_title", "author_name", "author_place_of_death", "author_death_dce", "text"]]
        df_grouped.to_csv(f"output/{grp}.csv")


if __name__ == "__main__":
    main()
