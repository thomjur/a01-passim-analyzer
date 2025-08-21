from cluster import parse_cluster_from_jsonl
from html import create_html_tr_doc_viewer
import os


def main():
    # First, we parse all TR cluster from passim's jsonl file
    # The files are stored in the output folder
    parse_cluster_from_jsonl("analyzer/data/passim-data.json")
    # Create HTML file for document viewer of a text-reuse cluster
    for idx, filename in enumerate(os.listdir("analyzer/output")):
        create_html_tr_doc_viewer(f"analyzer/output/{filename}", idx)


if __name__ == "__main__":
    main()
