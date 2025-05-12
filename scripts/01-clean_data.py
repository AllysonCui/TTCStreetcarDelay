import pandas as pd
from pathlib import Path
import glob


def merge_2025plus_delay_datasets():

    # Find the repository root directory
    current_file = Path(__file__)
    # Go up from current script location to find the root
    repo_root = current_file.parent.parent

    # Input file paths
    first_dataset_path = repo_root / "data" / "raw_data" / "delay_data_0.csv"
    second_dataset_path = repo_root / "data" / "raw_data" / "delay_data_1.csv"

    # Output file path
    output_path = repo_root / "data" / "analysis_data" / "2025plus_data.csv"

    # Create the output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Read the datasets
    df_delays = pd.read_csv(first_dataset_path)
    df_codes = pd.read_csv(second_dataset_path)

    # Rename columns in the codes dataframe for clarity
    df_codes = df_codes.rename(
        columns={'CODE': 'Code', 'DESCRIPTION': 'Description'})

    # Clean up the Description column by replacing the malformed characters
    df_codes['Description'] = df_codes['Description'].str.replace('ГўВЂВ“', '-',
                                                                  regex=False)

    # Merge the datasets based on the 'Code' column
    merged_df = pd.merge(
        df_delays,
        df_codes[['Code', 'Description']],
        on='Code',
        how='left'
    )

    # Save the merged dataframe to the output path
    merged_df.to_csv(output_path, index=False)

    print(f"Merged dataset saved to {output_path}")


if __name__ == "__main__":
    merge_2025plus_delay_datasets()
