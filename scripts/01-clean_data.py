"""
Merge TTC delay datasets script

This script merges two TTC streetcar delay datasets:
1. A primary dataset (delay_data_0.csv) containing delay incidents with dates, times, locations
2. A reference dataset (delay_data_1.csv) containing delay code descriptions

The merged dataset is saved to the analysis_data directory with descriptions mapped to each delay code.
"""

import polars as pl


def merge_2025plus_delay_datasets():
    # Define file paths
    first_dataset_path = "../data/raw_data/delay_data_0.csv"
    second_dataset_path = "../data/raw_data/delay_data_1.csv"
    output_path = "../data/analysis_data/2025plus_data.csv"

    # Read the datasets using polars
    df_delays = pl.read_csv(first_dataset_path)
    df_codes = pl.read_csv(second_dataset_path)

    # Rename columns in the codes dataframe for clarity
    df_codes = df_codes.rename({"CODE": "Code", "DESCRIPTION": "Description"})

    # Clean up the Description column by replacing malformed characters
    df_codes = df_codes.with_columns(
        pl.col("Description").str.replace_all('ГўВЂВ"', "-")
    )

    # Merge the datasets based on the 'Code' column
    merged_df = df_delays.join(
        df_codes.select(["Code", "Description"]),
        on="Code",
        how="left"
    )

    # Save the merged dataframe
    merged_df.write_csv(output_path)
    print(f"Merged dataset saved to {output_path}")


if __name__ == "__main__":
    merge_2025plus_delay_datasets()
