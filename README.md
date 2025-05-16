# TTC Streetcar Delay Analysis: Using Polars and UV for Efficient Data Processing

## Overview
This project analyzes the TTC streetcar delay data from 2025, looking at patterns and trends across various dimensions including time, location, day of week, and cause.

## Set Up

1. Install UV if not already installed: pip install uv
2. Create `requirments.txt` under the repository's main directory
3. Install dependencies with UV: uv pip install -r requirements.txt

## Running the Analysis
Execute the scripts in numerical order:

1. python `scripts/00-retrieve_data.py` - Downloads data from Toronto Open Data Portal
2. python `scripts/01-clean_data.py` - Processes and merges the datasets
3. python `scripts/02-monthly_delays.py` - Analyzes delays by month
4. python `scripts/03-weekday_delays.py` - Analyzes delays by day of week
5. python `scripts/04-delay_reason.py` - Analyzes causes of delays
6. python `scripts/05-time_delays.py` - Analyzes delays by time of day
7. python `scripts/06-location_delays.py` - Analyzes delays by location

## File Structure

The repo is structured as:
- `data/raw_data` contains the raw data as obtained from the TTC delay dataset.
- `data/analysis_data` contains the cleaned dataset that was constructed.
- `outputs` contains the generated visualizations.
- `scripts` contains the Python scripts used to retrieve, clean, and analyze data.
- `other/llm` contains the dialogue between me and Claude (LLM).

## Statement on LLM usage

Claude is used to format the tables. No LLMs were used for the analysis itself.
