"""
Hourly TTC Delay Analysis Script

This script analyzes TTC delay data by hour of the day, creating a visualization that
shows which times experience the highest frequency of transit delays.
"""

import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

data_path = "../data/analysis_data/2025plus_data.csv"
data = pl.read_csv(data_path)

# Extract hour from the 'Time' column
data = data.with_columns(
    pl.col("Time").cast(pl.Utf8).alias("Time")
)

data = data.with_columns(
    pl.when(
        (pl.col("Time") == "None") | pl.col("Time").is_null()
    ).then(None).otherwise(
        pl.col("Time").str.split(":").list.get(0).cast(pl.Int32)
    ).alias("Hour")
)

# Create a dataframe with all hours (0-23)
all_hours = pl.DataFrame({"Hour": pl.Series(range(24), dtype=pl.Int32)})

# Count delays by hour
hour_counts = (
    data.group_by("Hour")
    .len()
    .rename({"len": "Count"})
)

# Merge with all_hours to ensure we have all 24 hours
hour_counts = all_hours.join(hour_counts, on="Hour", how="left", coalesce=True).fill_null(0)
hour_counts = hour_counts.with_columns(
    pl.col("Count").cast(pl.Int32)
)

# Create time range strings (e.g., "00:00 - 00:59")
hour_counts = hour_counts.with_columns(
    (pl.col("Hour").cast(pl.Utf8).str.zfill(2) + ":00 - " +
     pl.col("Hour").cast(pl.Utf8).str.zfill(2) + ":59").alias("Time Range")
)

# Sort by Hour and convert to pandas for plotting
hour_counts = hour_counts.sort("Hour")
hour_counts_pd = hour_counts.to_pandas()

# Create the visualization
plt.figure(figsize=(14, 8))
ax = sns.barplot(
    x='Time Range',
    y='Count',
    hue='Time Range',
    legend=False,
    data=hour_counts_pd
)

# Format the chart
plt.xticks(rotation=45, ha='right')
plt.xlabel('Time of Day', fontsize=12)
plt.ylabel('Number of Delays', fontsize=12)
plt.title('Frequency of Delays by Hour of Day', fontsize=16)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Add data labels on top of each bar
for i, count in enumerate(hour_counts_pd['Count']):
    if count > 0:
        ax.text(i, count + 1, str(count), ha='center', fontsize=10)

# Save the figure
save_path = "../outputs/05-delay_time_barchart.png"
plt.savefig(save_path, bbox_inches='tight', dpi=300)
plt.close()
