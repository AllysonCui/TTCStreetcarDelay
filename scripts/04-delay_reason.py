import polars as pl
import matplotlib.pyplot as plt
import squarify
import seaborn as sns


def categorize_incidents(df):
    # Create a function to map code prefixes to categories
    def map_code_to_category(code_prefix):
        if code_prefix == 'ET':
            return 'Equipment [ET]'
        elif code_prefix == 'MT':
            return 'Miscellaneous Operations [MT]'
        elif code_prefix == 'PT':
            return 'Plant [PT]'
        elif code_prefix == 'ST':
            return 'Security [ST]'
        elif code_prefix == 'TT':
            return 'Transportation [TT]'
        else:
            # Handle any other prefixes that might exist
            return 'Other'

    # Create a new column with just the first two characters of the code
    df = df.with_columns(
        pl.col("Code").str.slice(0, 2).alias("code_prefix")
    )

    # Apply the mapping function to get categories
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

    # Create sorted items for consistent order
    sorted_items = sorted(category_dict.items(), key=lambda x: x[1],
                          reverse=True)

    for category, count in sorted_items:
        labels.append(f"{category} ({count})")
        sizes.append(count)

    # Create a colormap with blues
    cmap = plt.cm.Blues
    colors = [cmap(0.4 + (i / len(labels)) * 0.6) for i in range(len(labels))]

    # Create the figure
    plt.figure(figsize=(15, 8))

    # Create treemap
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8,
                  text_kwargs={'fontsize': 12})

    # Add title
    plt.title('The most common Incidents which cause delays', fontsize=18)
    plt.axis('off')

    # Save the figure to the appropriate location
    save_path = "../outputs/04-delay_incidents_treemap.png"
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()

    print("Treemap saved as 'delay_incidents_treemap.png'")


# Function to analyze and create stacked bar chart
def create_category_bar_chart(df):
    # Fill any null values in the Description column with a placeholder
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

    # Add description and category
    code_desc_cat = df.select(["Code", "Description", "Category"]).unique()

    # Join counts with descriptions and categories
    code_analysis = code_counts.join(code_desc_cat, on="Code")

    # Get top 15 codes
    top_codes = code_analysis.head(15)

    # Convert to pandas for matplotlib plotting
    top_codes_pd = top_codes.to_pandas()

    # Create stacked bar chart
    plt.figure(figsize=(15, 8))
    bars = plt.bar(top_codes_pd['Code'], top_codes_pd['Count'],
                   color=sns.color_palette("Blues_d", len(top_codes_pd)))

    # Add descriptions as annotations
    for i, (_, row) in enumerate(top_codes_pd.iterrows()):
        # Handle any None values in Description
        description = row['Description'] if row[
                                                'Description'] is not None else "Unknown"

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

    # Save the figure to the appropriate location
    save_path = "../outputs/04-top_delay_codes.png"
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()

    print("Bar chart saved as 'top_delay_codes.png'")


data_path = "../data/analysis_data/2025plus_data.csv"

# Load the main dataset directly from the specified path
df = pl.read_csv(data_path)

# Categorize incidents
df = categorize_incidents(df)

# Create and save treemap
create_treemap(df)

# Create and save bar chart
create_category_bar_chart(df)

print("Analysis complete!")
