"""Main entry point for the Passim text-reuse analyzer.

This module orchestrates the processing of Passim output data, converting JSONL
files into structured CSV files and generating HTML visualizations for each
text-reuse cluster.
"""

from cluster import parse_cluster_from_jsonl, parse_pairwise_from_jsonl
from html import create_html_tr_doc_viewer
import os


def main() -> None:
    """Execute the main text-reuse analysis pipeline.
    
    This function performs three main steps:
    1. Parses text-reuse clusters from Passim JSONL output
    2. Extracts pairwise alignment data
    3. Generates HTML visualizations for each cluster
    
    The pipeline expects input files in analyzer/data/ and produces:
    - CSV files in analyzer/output/
    - HTML visualization files in analyzer/html/
    
    Returns:
        None
        
    Side Effects:
        - Creates multiple CSV files in analyzer/output/
        - Creates HTML files in analyzer/html/ for each cluster
    """
    # Parse all text-reuse clusters from Passim's JSONL file
    # The files are stored in the output folder
    parse_cluster_from_jsonl("analyzer/data/passim-data.json")
    parse_pairwise_from_jsonl("analyzer/data/passim-pairwise.json")
    
    # Create HTML file for document viewer of each text-reuse cluster
    output_files: list[str] = os.listdir("analyzer/output")
    for idx, filename in enumerate(output_files):
        # Skip the aggregated CSV files, only process individual cluster files
        if filename not in ("pairwise.csv", "sources.csv"):
            filepath: str = f"analyzer/output/{filename}"
            create_html_tr_doc_viewer(filepath, idx)


if __name__ == "__main__":
    main()
