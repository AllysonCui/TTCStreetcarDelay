import pandas as pd
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
    df['code_prefix'] = df['Code'].str[:2]

    # Apply the mapping function to get categories
    df['Category'] = df['code_prefix'].apply(map_code_to_category)

    return df


def create_treemap(df):
    # Count incidents by category
    category_counts = df['Category'].value_counts().to_dict()

    # Prepare data for treemap
    labels = []
    sizes = []

    # Create sorted items for consistent order
    sorted_items = sorted(category_counts.items(), key=lambda x: x[1],
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

    # Group by code and count occurrences
    code_counts = df['Code'].value_counts().reset_index()
    code_counts.columns = ['Code', 'Count']

    # Add description and category
    code_desc_cat = df[['Code', 'Description', 'Category']].drop_duplicates()
    code_analysis = pd.merge(code_counts, code_desc_cat, on='Code')

    # Get top 15 codes
    top_codes = code_analysis.sort_values('Count', ascending=False).head(15)

    # Create stacked bar chart
    plt.figure(figsize=(15, 8))
    bars = plt.bar(top_codes['Code'], top_codes['Count'],
                   color=sns.color_palette("Blues_d", len(top_codes)))

    # Add descriptions as annotations
    for i, (_, row) in enumerate(top_codes.iterrows()):
        plt.annotate(f"{row['Description'][:]}",
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
df = pd.read_csv(data_path)

# Categorize incidents
df = categorize_incidents(df)

# Create and save treemap
create_treemap(df)

create_category_bar_chart(df)

print("Analysis complete!")
