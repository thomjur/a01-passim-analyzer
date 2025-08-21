import pandas as pd
import dominate
from dominate.tags import *
import os



def create_html_tr_doc_viewer(filepath: str, suffix: str = ""):
    '''Creating a simple HTML document showing documents and text reuse
    of a specific text-reuse cluster. Note: The data must be available as CSV file
    under the given path.'''
    doc = dominate.document(title="A01 Text-Reuse Document Viewer")

    # Storing every unique subchapter in this list
    SC_DICT = dict()

    # Loading data
    df = pd.read_csv(filepath)
    if not os.path.exists(filepath):
        print(f"Could not create HTML file. The CSV does not exist under the path: {filepath}")
    with doc:
        with div(id="main-container"):
            h1(f"A01 Text Reuse Document Viewer (Cluster: {df.at[0,'cluster']})")
            # Creating a separate container for all texts, starting with the source text (which should be the first in the cluster)
            for idx, row in df.iterrows():
                # Storing entry in subchapter
                if row['uid'] not in SC_DICT:
                    SC_DICT[float(row['uid'])] = {
                        'text': row['text'],
                        'start_idx': row['begin']
                    }
                with div(id="source-text" if idx == 0 else f"target_text_{idx}"):
                    h2(row["tafsir_title"])
                    p(f"ID: {row['uid']}")
                    p(f"Reuses from: {row['src_uid']}")
                    p(f"Date: {row['author_death_dce']} Author: {row['author_name']}")
                    p(row["text"])
                    p("Reuse in source text:")
                    if row['src_uid'] in SC_DICT:
                        src_text = SC_DICT[row["src_uid"]]["text"]
                        # Calculating start position of quote
                        tr_start_idx = int(row["src_begin"] - SC_DICT[row["src_uid"]]["start_idx"])
                        tr_end_idx = int(row["src_end"] - SC_DICT[row["src_uid"]]["start_idx"])
                        with p():
                            dominate.util.text(src_text[:tr_start_idx])
                            span(src_text[tr_start_idx:tr_end_idx], style="background: yellow;")
                            dominate.util.text(src_text[tr_end_idx:])

    # Save HTML file
    with open(f"analyzer/html/index{suffix}.html", "w") as f:
        f.write(doc.render())
