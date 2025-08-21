from cluster import parse_cluster_from_jsonl
from html import create_html_tr_doc_viewer


def main():
    # First, we parse all TR cluster from passim's jsonl file
    # The files are stored in the output folder
    parse_cluster_from_jsonl("analyzer/data/passim-data.json")
    # Create HTML file for document viewer of a text-reuse cluster
    create_html_tr_doc_viewer("analyzer/output/1.csv")


if __name__ == "__main__":
    main()
