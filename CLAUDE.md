# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based analyzer for Passim text-reuse data. It processes JSONL files from Passim (a text-reuse detection tool), parses text-reuse clusters, and generates HTML visualizations showing document relationships and pairwise alignments.

## Development Setup and Commands

### Install dependencies
```bash
uv sync
```

### Run the analyzer
```bash
uv run python analyzer/main.py
```

## Architecture

The analyzer consists of three main components:

1. **cluster.py**: Parses Passim JSONL output into structured CSV files
   - `parse_cluster_from_jsonl()`: Processes main cluster data, splits into source texts and references
   - `parse_pairwise_from_jsonl()`: Extracts pairwise alignment data
   - Handles complex data transformations including flattening nested JSON structures and managing int/float conversion issues

2. **html.py**: Generates HTML visualization documents
   - Creates interactive viewers for text-reuse clusters
   - Highlights text reuse passages in source documents
   - Shows pairwise alignments between texts
   - Uses dominate library for HTML generation

3. **main.py**: Orchestrates the workflow
   - Processes input from `analyzer/data/` directory
   - Outputs CSV files to `analyzer/output/`
   - Generates HTML files in `analyzer/html/`

## Data Flow

1. Input: JSONL files from Passim (`passim-data.json`, `passim-pairwise.json`)
2. Processing: Parse and transform into structured CSV files per cluster
3. Output: HTML visualization files showing text relationships

## Key Technical Considerations

- The codebase handles Arabic text and metadata about Islamic texts (tafsir)
- Special handling for int/float conversion issues when merging dataframes
- Source texts and reference texts are processed separately to avoid data type conflicts
- Each cluster gets its own CSV and HTML output file