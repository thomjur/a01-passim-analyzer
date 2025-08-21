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
                    h2(f"{row['tafsir_title']} ({row['author_death_dce']})")
                    p(f"ID: {row['uid']}")
                    p(f"Reuses from: {int(row['src_uid']) if not pd.isna(row['src_uid']) else "-"}")
                    p(f"Author: {row['author_name']}")
                    target_text_para = p()
                    p("Reuse in source text:")
                    if row['src_uid'] in SC_DICT:
                        source_text_para = p()
                        src_text = SC_DICT[row["src_uid"]]["text"]
                        # Calculating start position of quote
                        tr_start_idx = int(row["src_begin"] - SC_DICT[row["src_uid"]]["start_idx"])
                        tr_end_idx = int(row["src_end"] - SC_DICT[row["src_uid"]]["start_idx"])
                        # We start creating target and source texts and highlighting matching words
                        # First, we add the text to the source part that is not included in the text-reuse section
                        source_text_para += text(src_text[:tr_start_idx])
                        # Next, we get the slice of source text from which the TR stems
                        reused_text = src_text[tr_start_idx:tr_end_idx]
                        reused_text_tokens = reused_text.split(" ")
                        # DEBUG: Clean tokens
                        reused_text_tokens = [token for token in reused_text_tokens if len(token) > 1 and token.isalpha()]
                        print(reused_text_tokens)
                        # Iterating over token list of target text and highlight similar words in both target and source texts
                        source_loop_index = 0 # Keep track of position in source list
                        for token_target in [token for token in row['text'].split(" ") if len(token) > 1 and token.isalpha()]:
                            print(token_target)
                            match = False
                            for inner_idx,token_source in enumerate(reused_text_tokens[source_loop_index:]):
                                if token_target == token_source:
                                    # First add the previous tokens
                                    source_text_para += text(" ".join(reused_text_tokens[source_loop_index:inner_idx]))
                                    # Mark current word as match
                                    source_text_para += span(f" {token_source} ", style="background: green;")
                                    # Set inner loop index
                                    source_loop_index = inner_idx + 1
                                    match = True
                                    break
                            if match:
                                target_text_para += span(f" {token_target} ", style="background: green;")
                            else:
                                target_text_para += text(f" {token_target} ")
                        # Add remaining text
                        source_text_para += text(src_text[tr_end_idx:])

    # Save HTML file
    with open(f"analyzer/html/index{suffix}.html", "w") as f:
        f.write(doc.render())
