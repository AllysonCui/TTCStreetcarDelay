"""
Monthly TTC Delay Visualization Script

This script analyzes TTC delay data by month, identifying patterns and trends across time periods.
It generates a bar chart showing monthly delay counts, highlighting the month with the highest
average delays, and saves the visualization to the outputs directory.
"""

import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import calendar

# Define path and load data
data_file = "../data/analysis_data/2025plus_data.csv"
df = pl.read_csv(data_file)

# Convert Date column to datetime and extract year and month
df = df.with_columns([
    pl.col("Date").str.to_datetime(),
    pl.col("Date").str.to_datetime().dt.year().alias("Year"),
    pl.col("Date").str.to_datetime().dt.month().alias("Month")
])

# Count delays by year and month
monthly_counts = (
    df.group_by(["Year", "Month"])
    .len()
    .rename({"count": "Count"})
)

# Get unique years and months in the data
years = sorted(monthly_counts.select("Year").unique().to_series().to_list())
months_present = sorted(
    monthly_counts.select("Month").unique().to_series().to_list())

# Find the month with the highest average number of delays
avg_by_month = (
    monthly_counts.group_by("Month")
    .agg(pl.col("Count").mean())
    .sort("Month")
)

max_month_row = avg_by_month.filter(
    pl.col("Count") == pl.col("Count").max()
).row(0)
max_month_num = max_month_row[0]
max_month_name = calendar.month_name[max_month_num]

# Convert the month numbers to month names
month_names = [calendar.month_name[month] for month in months_present]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

# Available colors for years
color_palette = ['#4285F4', '#4ecdc4', '#F87171', '#6366F1', '#A78BFA',
                 '#EC4899', '#F97316']

# Create a pivot table for easier plotting
pivot_df = (
    monthly_counts.to_pandas()
    .pivot(index='Month', columns='Year', values='Count')
    .fillna(0)
)
pivot_df = pivot_df.loc[months_present]
years = [int(year) for year in years]


# Helper function to format values to k format
def format_to_k(val):
    if val >= 1000:
        return f"{val / 1000:.1f}k".replace('.0k', 'k')
    else:
        return f"{val}"


# Plotting based on number of years
if len(years) == 1:
    # Single year - simple bar chart
    year = years[0]
    year_data = pivot_df[year].values
    bars = ax.bar(month_names, year_data, color=color_palette[0], width=0.8,
                  label=str(year))

    # Add value annotations
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height - (height * 0.05),
                format_to_k(height),
                ha='center', va='top', color='black', fontsize=9)
else:
    # Multiple years - stacked bar chart
    bottom = np.zeros(len(months_present))
    all_bars = []

    for i, year in enumerate(years):
        if year in pivot_df.columns:
            year_data = pivot_df[year].values
            color = color_palette[i % len(color_palette)]
            bars = ax.bar(month_names, year_data, label=str(year), color=color,
                          width=0.8, bottom=bottom)

            # Add value annotations for significant bars
            for j, bar in enumerate(bars):
                bar_height = bar.get_height()
                text_y = bottom[j] + bar_height - (bar_height * 0.1)

                if bar_height > 100:
                    ax.text(bar.get_x() + bar.get_width() / 2., text_y,
                            format_to_k(bar_height),
                            ha='center', va='top', color='black', fontsize=9,
                            fontweight='bold', alpha=0.9)

            all_bars.append(bars)
            bottom += year_data

# Set plot title with the month that has the highest average delays
ax.set_title(f'Most of the Delays occur during {max_month_name} :', fontsize=16,
             loc='left')

# Configure y-axis based on data range
max_value = pivot_df.values.max() * (2 if len(years) > 1 else 1.2)

if max_value > 15000:
    max_tick = 20000
    y_labels = ['0', '5K', '10K', '15K', '20K']
elif max_value > 10000:
    max_tick = 15000
    y_labels = ['0', '3.75K', '7.5K', '11.25K', '15K']
elif max_value > 5000:
    max_tick = 10000
    y_labels = ['0', '2.5K', '5K', '7.5K', '10K']
else:
    max_tick = 5000
    y_labels = ['0', '1.25K', '2.5K', '3.75K', '5K']

y_ticks = np.linspace(0, max_tick, 5)
ax.set_ylim(0, max_tick)
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels)

# Add gridlines and legend
ax.grid(axis='y', linestyle='-', alpha=0.2)
ax.legend(loc='upper left')

# Save the figure
output_path = "../outputs/02-monthly_delays.png"
plt.savefig(output_path, dpi=300)
plt.close(fig)
