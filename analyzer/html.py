import re
import pandas as pd
import dominate
from dominate.tags import *
import os
from dominate.util import text


def create_html_tr_doc_viewer(filepath: str, suffix: str = ""):
    '''Creating a simple HTML document showing documents and text reuse
    of a specific text-reuse cluster. Note: The data must be available as CSV file
    under the given path.'''
    doc = dominate.document(title="A01 Text-Reuse Document Viewer")
    with doc.head:
        link(rel='stylesheet', href='css/styles.css')

    # Storing every unique subchapter in this list
    SC_DICT = dict()
    # Storing tuples of already visited text combinations
    VISITED_LIST = list()

    # Loading data
    df = pd.read_csv(filepath)
    # Loading source csv
    df_sources = pd.read_csv("analyzer/output/sources.csv")
    # Loading pairwise alignment data
    df_pairwise = pd.read_csv("analyzer/output/pairwise.csv")
    if not os.path.exists(filepath):
        print(f"Could not create HTML file. The CSV does not exist under the path: {filepath}")
    with doc:
        with div(id="main-container"):
            current_cluster = df.at[0,"cluster"]
            h1(f"A01 Text Reuse Document Viewer (Cluster: {current_cluster})")
            # First, we get the source text
            source_data = df_sources[df_sources["cluster"] == current_cluster].reset_index()
            if source_data.at[0,'uid'] not in SC_DICT:
                SC_DICT[source_data.at[0,'uid']] = {
                    'text': source_data.at[0,'text'],
                    'start_idx': source_data.at[0,'begin']
                }
            with div(id="source-text"):
                h2(f"{source_data.at[0, 'tafsir_title']} ({source_data.at[0,'author_death_dce']})")
                p(f"ID: {source_data.at[0, 'uid']}")
                p(f"Author: {source_data.at[0, 'author_name']}")
                p(source_data.at[0, "text"])

            # Creating a separate container for all texts, starting with the source text (which should be the first in the cluster)
            for idx, row in df.iterrows():
                # Storing entry in subchapter
                if row['uid'] not in SC_DICT:
                    SC_DICT[row['uid']] = {
                        'text': row['text'],
                        'start_idx': row['begin']
                    }
                if (row["src_uid"], row["uid"]) in VISITED_LIST:
                    continue
                with div(id=f"target_text_{idx}"):
                    h2(f"{row['tafsir_title']} ({row['author_death_dce']})")
                    p(f"ID: {row['uid']}")
                    p(f"Reuses from: {row['src_uid']}")
                    p(f"Author: {row['author_name']}")
                    p(row["text"])
                    if row['src_uid'] in SC_DICT and (row["src_uid"], row["uid"]) not in VISITED_LIST:
                        src_text = SC_DICT[row["src_uid"]]["text"]
                        # Calculating start position of quote
                        tr_start_idx = int(row["src_begin"] - SC_DICT[row["src_uid"]]["start_idx"])
                        tr_end_idx = int(row["src_end"] - SC_DICT[row["src_uid"]]["start_idx"])
                        p("The source text is as follows:")
                        with p():
                            dominate.util.text(src_text[:tr_start_idx])
                            span(src_text[tr_start_idx:tr_end_idx], style="background: yellow;")
                            dominate.util.text(src_text[tr_end_idx:])
                        p("Pairwise alignment:")
                        # Searching for entries
                        df_alignment = df_pairwise.loc[(df_pairwise["uid2"] == row["uid"]) & (df_pairwise["uid"] == row["src_uid"]) & (df_pairwise["begin"] >= row["src_begin"]) & (df_pairwise["end"] <= row["src_end"]),:].reset_index()
                        if not df_alignment.empty:
                            p("The following alignment pairs have been identified:")
                            for idx1, row1 in df_alignment.iterrows():
                                p(f"Source text alignment {idx1+1}:")
                                p(row1["s1"], cls="arabic-text")
                                p(f"This text alignment {idx1+1}:")
                                p(row1["s2"], cls="arabic-text")

                        # Add this pairs to already visited pairs
                        VISITED_LIST.append((row["src_uid"], row["uid"]))

    # Save HTML file
    with open(f"analyzer/html/index_{current_cluster}.html", "w") as f:
        f.write(doc.render())
