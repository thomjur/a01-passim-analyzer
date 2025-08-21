import pandas as pd
import dominate
from dominate.tags import *
import os

doc = dominate.document(title="A01 Text-Reuse Document Viewer")

def create_html_tr_doc_viewer(filepath: str):
    '''Creating a simple HTML document showing documents and text reuse
    of a specific text-reuse cluster. Note: The data must be available as CSV file
    under the given path.'''
    # Loading data
    df = pd.read_csv(filepath)
    if not os.path.exists(filepath):
        print(f"Could not create HTML file. The CSV does not exist under the path: {filepath}")
    with doc:
        with div(id="main-container"):
            h1(df.at[0, "tafsir_title"])
            p(df.at[0, "text"])

    # Save HTML file
    with open("analyzer/html/index.html", "w") as f:
        f.write(doc.render())
