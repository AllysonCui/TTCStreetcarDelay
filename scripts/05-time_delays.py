import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data_path = "../data/analysis_data/2025plus_data.csv"

# Load the data with polars
data = pl.read_csv(data_path)

# Extract hour from the 'Time' column
# First, ensure the 'Time' column is in string format
data = data.with_columns(
    pl.col("Time").cast(pl.Utf8).alias("Time")
)

# Extract hour, handle 'None' values
data = data.with_columns(
    pl.when(
        (pl.col("Time") == "None") | pl.col("Time").is_null()
    ).then(None).otherwise(
        pl.col("Time").str.split(":").list.get(0).cast(pl.Int32)
    ).alias("Hour")
)

# Create a dataframe with all hours (0-23)
all_hours = pl.DataFrame({"Hour": pl.arange(0, 24, dtype=pl.Int32)})

# Count delays by hour
hour_counts = (
    data.group_by("Hour")
    .count()
    .rename({"count": "Count"})
)

# Merge with all_hours to ensure we have all 24 hours
hour_counts = all_hours.join(hour_counts, on="Hour", how="left").fill_null(0)

# Convert "Count" column to integer
hour_counts = hour_counts.with_columns(
    pl.col("Count").cast(pl.Int32)
)

# Create time range strings (e.g., "00:00 - 00:59")
hour_counts = hour_counts.with_columns(
    pl.format("{:02d}:00 - {:02d}:59", pl.col("Hour"), pl.col("Hour")).alias("Time Range")
)

# Sort by Hour
hour_counts = hour_counts.sort("Hour")

# Convert to pandas for plotting with seaborn
hour_counts_pd = hour_counts.to_pandas()

# Set up the figure and plot
plt.figure(figsize=(14, 8))

# Create the bar chart with proper hue parameter instead of palette
# Using the x variable for hue and setting legend=False, as suggested in the warning
ax = sns.barplot(
    x='Time Range',
    y='Count',
    hue='Time Range',  # Use x variable for hue
    legend=False,      # Set legend=False to avoid duplicating the information
    data=hour_counts_pd
)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add labels and title
plt.xlabel('Time of Day', fontsize=12)
plt.ylabel('Number of Delays', fontsize=12)
plt.title('Frequency of Delays by Hour of Day', fontsize=16)

# Add grid lines for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Tight layout to ensure everything fits
plt.tight_layout()

# Add data labels on top of each bar
for i, count in enumerate(hour_counts_pd['Count']):
    if count > 0:  # Only add labels for bars with non-zero values
        ax.text(i, count + 1, str(count), ha='center', fontsize=10)

# Save the figure
save_path = "../outputs/05-delay_time_barchart.png"
plt.savefig(save_path, bbox_inches='tight', dpi=300)

print(f"Saved delay times bar chart to file: {save_path}")
plt.close()
