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
        meta(charset="utf-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        # Import Google Fonts for Arabic text
        link(href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Scheherazade+New:wght@400;500;600;700&display=swap", rel="stylesheet")
        style("""
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f8f9fa;
                color: #333;
            }
            
            #main-container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            h1 {
                color: #2c3e50;
                text-align: center;
                border-bottom: 3px solid #3498db;
                padding-bottom: 15px;
                margin-bottom: 30px;
            }
            
            h2 {
                color: #34495e;
                border-left: 4px solid #3498db;
                padding-left: 15px;
                margin-top: 30px;
                margin-bottom: 15px;
            }
            
            #source-text {
                background: #e8f4fd;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                border-left: 5px solid #3498db;
            }
            
            #source-text h2 {
                color: #2980b9;
                border-left: none;
                padding-left: 0;
                margin-top: 0;
            }
            
            div[id^="target_text_"] {
                background: #f9f9f9;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
                border-left: 5px solid #95a5a6;
            }
            
            div[id^="target_text_"] h2 {
                color: #7f8c8d;
                border-left: none;
                padding-left: 0;
                margin-top: 0;
            }
            
            p {
                margin: 10px 0;
            }
            
            .arabic-text {
                direction: rtl;
                text-align: right;
                font-family: 'Scheherazade New', 'Amiri', 'Arabic Typesetting', serif;
                font-size: 18px;
                line-height: 2.0;
                background: #fefefe;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                margin: 15px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                unicode-bidi: isolate;
            }
            
            span[style*="background: yellow"] {
                background: #fff3cd !important;
                padding: 2px 4px;
                border-radius: 3px;
                border: 1px solid #ffeaa7;
                font-weight: bold;
            }
            
            .metadata {
                font-size: 14px;
                color: #666;
                background: #f8f9fa;
                padding: 8px 12px;
                border-radius: 4px;
                margin: 5px 0;
                display: inline-block;
            }
            
            .alignment-section {
                background: #fff5f5;
                padding: 15px;
                margin: 15px 0;
                border-radius: 6px;
                border-left: 3px solid #e74c3c;
            }
            
            .alignment-pair {
                background: white;
                padding: 12px;
                margin: 8px 0;
                border-radius: 4px;
                border: 1px solid #ddd;
            }
            
            .alignment-label {
                font-weight: bold;
                color: #e74c3c;
                font-size: 14px;
                margin-bottom: 5px;
            }
            
            .source-highlight {
                background: linear-gradient(120deg, #a8e6cf 0%, #dcedc1 100%);
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #27ae60;
                box-shadow: 0 2px 8px rgba(39, 174, 96, 0.1);
            }
            
            .source-highlight h3 {
                color: #27ae60;
                margin-top: 0;
                margin-bottom: 15px;
                font-size: 16px;
                border-left: none;
                padding-left: 0;
            }
            
            h3 {
                color: #2c3e50;
                font-size: 16px;
                margin: 15px 0 10px 0;
                font-weight: 600;
            }
            
            .alignment-section h3 {
                color: #e74c3c;
                margin-top: 0;
            }
            
            /* Responsive design */
            @media (max-width: 768px) {
                #main-container {
                    padding: 20px;
                    margin: 10px;
                }
                
                .arabic-text {
                    font-size: 16px;
                    padding: 15px;
                }
                
                h1 {
                    font-size: 24px;
                }
                
                h2 {
                    font-size: 20px;
                }
            }
        """)

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
                p(f"ID: {source_data.at[0, 'uid']}", cls="metadata")
                p(f"Author: {source_data.at[0, 'author_name']}", cls="metadata")
                p(source_data.at[0, "text"], cls="arabic-text")

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
                    p(f"ID: {row['uid']}", cls="metadata")
                    p(f"Reuses from: {row['src_uid']}", cls="metadata")
                    p(f"Author: {row['author_name']}", cls="metadata")
                    p(row["text"], cls="arabic-text")
                    if row['src_uid'] in SC_DICT and (row["src_uid"], row["uid"]) not in VISITED_LIST:
                        src_text = SC_DICT[row["src_uid"]]["text"]
                        # Calculating start position of quote
                        tr_start_idx = int(row["src_begin"] - SC_DICT[row["src_uid"]]["start_idx"])
                        tr_end_idx = int(row["src_end"] - SC_DICT[row["src_uid"]]["start_idx"])
                        with div(cls="source-highlight"):
                            h3("Source Text with Highlighted Reuse:")
                            with p(cls="arabic-text"):
                                dominate.util.text(src_text[:tr_start_idx])
                                span(src_text[tr_start_idx:tr_end_idx], style="background: yellow;")
                                dominate.util.text(src_text[tr_end_idx:])
                        
                        # Searching for entries
                        df_alignment = df_pairwise.loc[(df_pairwise["uid2"] == row["uid"]) & (df_pairwise["uid"] == row["src_uid"]) & (df_pairwise["begin"] >= row["src_begin"]) & (df_pairwise["end"] <= row["src_end"]),:].reset_index()
                        if not df_alignment.empty:
                            with div(cls="alignment-section"):
                                h3("Pairwise Text Alignments:")
                                for idx1, row1 in df_alignment.iterrows():
                                    with div(cls="alignment-pair"):
                                        div(f"Source alignment {idx1+1}:", cls="alignment-label")
                                        p(row1["s1"], cls="arabic-text")
                                        div(f"Target alignment {idx1+1}:", cls="alignment-label")
                                        p(row1["s2"], cls="arabic-text")

                        # Add this pairs to already visited pairs
                        VISITED_LIST.append((row["src_uid"], row["uid"]))

    # Save HTML file
    with open(f"analyzer/html/index_{current_cluster}.html", "w") as f:
        f.write(doc.render())
