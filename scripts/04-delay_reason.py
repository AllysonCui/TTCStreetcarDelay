"""
TTC Delay Incident Analysis Script

This script categorizes TTC delay incidents based on their code prefixes and creates
two visualizations:
1. A treemap showing the distribution of delay incidents by category
2. A bar chart of the top 15 specific delay codes with their descriptions
"""

import polars as pl
import matplotlib.pyplot as plt
import squarify
import seaborn as sns

def categorize_incidents(df):
    # Extract code prefix and map to categories
    df = df.with_columns(
        pl.col("Code").str.slice(0, 2).alias("code_prefix")
    )

    # Map prefixes to descriptive categories
    df = df.with_columns(
        pl.col("code_prefix").replace({
            'ET': 'Equipment [ET]',
            'MT': 'Miscellaneous Operations [MT]',
            'PT': 'Plant [PT]',
            'ST': 'Security [ST]',
            'TT': 'Transportation [TT]'
        }, default='Other').alias("Category")
    )

    return df

def create_treemap(df):
    # Count incidents by category
    category_counts = (
        df.group_by("Category")
        .len()
        .sort("len", descending=True)
    )

    # Convert to dictionary for treemap
    category_dict = {row[0]: row[1] for row in category_counts.rows()}

    # Prepare data for treemap
    labels = []
    sizes = []
    sorted_items = sorted(category_dict.items(), key=lambda x: x[1], reverse=True)

    for category, count in sorted_items:
        labels.append(f"{category} ({count})")
        sizes.append(count)

    # Create a colormap with blues
    cmap = plt.cm.Blues
    colors = [cmap(0.4 + (i / len(labels)) * 0.6) for i in range(len(labels))]

    # Create and configure the treemap
    plt.figure(figsize=(15, 8))
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8, text_kwargs={'fontsize': 12})
    plt.title('The most common Incidents which cause delays', fontsize=18)
    plt.axis('off')

    # Save the visualization
    save_path = "../outputs/04-delay_incidents_treemap.png"
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()

def create_category_bar_chart(df):
    # Fill any null values in the Description column
    df = df.with_columns(
        pl.col("Description").fill_null("Unknown")
    )

    # Group by code and count occurrences
    code_counts = (
        df.group_by("Code")
        .len()
        .sort("len", descending=True)
        .rename({"len": "Count"})
    )

    # Add description and category information
    code_desc_cat = df.select(["Code", "Description", "Category"]).unique()
    code_analysis = code_counts.join(code_desc_cat, on="Code")
    top_codes = code_analysis.head(15)

    # Convert to pandas for matplotlib plotting
    top_codes_pd = top_codes.to_pandas()

    # Create and configure the bar chart
    plt.figure(figsize=(15, 8))
    bars = plt.bar(top_codes_pd['Code'], top_codes_pd['Count'],
                   color=sns.color_palette("Blues_d", len(top_codes_pd)))

    # Add descriptions as annotations
    for i, (_, row) in enumerate(top_codes_pd.iterrows()):
        description = row['Description'] if row['Description'] is not None else "Unknown"
        plt.annotate(f"{description}",
                     xy=(i, row['Count']),
                     xytext=(0, 5),
                     textcoords="offset points",
                     ha='center', va='bottom',
                     rotation=90,
                     fontsize=9)

    plt.title('Top 15 Delay Incident Codes', fontsize=18)
    plt.xlabel('Incident Code')
    plt.ylabel('Number of Occurrences')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the visualization
    save_path = "../outputs/04-top_delay_codes.png"
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()

# Main execution
data_path = "../data/analysis_data/2025plus_data.csv"
df = pl.read_csv(data_path)

# Process data and create visualizations
df = categorize_incidents(df)
create_treemap(df)
create_category_bar_chart(df)
