import polars as pl
import matplotlib.pyplot as plt

data_path = "../data/analysis_data/2025plus_data.csv"

# Load the dataset with polars
df = pl.read_csv(data_path)

# Group by day and date to get unique days in the dataset
# First, create a combined Date-Day identifier
df = df.with_columns(
    pl.concat_str([pl.col("Date"), pl.lit("_"), pl.col("Day")]).alias("Date_Day")
)

# Count unique Date_Day combinations per day to get occurrences
day_occurrences = (
    df.group_by("Day")
    .agg(pl.col("Date_Day").n_unique().alias("Occurrences"))  # Directly name the column
)

# Count delays by day of the week
day_counts = (
    df.group_by("Day")
    .len()
    .rename({"count": "Count"})
)

# Join the counts and occurrences
day_stats = day_counts.join(day_occurrences, on="Day")

# Calculate average delays per day occurrence
day_stats = day_stats.with_columns(
    (pl.col("Count") / pl.col("Occurrences")).alias("AvgDelaysPerDay")
)

# Convert to a dictionary for plotting
day_avg_dict = {row[0]: row[3] for row in day_stats.rows()}

# Calculate percentages for the pie chart
total_avg = sum(day_avg_dict.values())
day_percentages = {day: round((value / total_avg * 100), 1) for day, value in day_avg_dict.items()}

# Define colors for each day
colors = ['#4285F4', '#80CBC4', '#E91E63', '#F57C00', '#FFC107', '#8BC34A', '#673AB7']

# Create a custom order for days of the week
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Reorder percentages according to days_order
ordered_percentages = [day_percentages.get(day, 0) for day in days_order]

# Create figure with specific size for better proportions
plt.figure(figsize=(8, 8))

# Create the pie chart
plt.pie(
    ordered_percentages,
    labels=None,
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops={'edgecolor': 'white', 'linewidth': 1}
)

# Add a legend with custom colored markers
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10)
           for color in colors]
plt.legend(handles, days_order, loc='center right', bbox_to_anchor=(1.2, 0.5))

# Add title
plt.title('Delays are evenly spread out throughout the week', fontsize=16)

# Equal aspect ratio ensures the pie chart is circular
plt.axis('equal')

# Save the figure to the appropriate location
save_path = "../outputs/03-weekday_delays.png"
plt.savefig(save_path, bbox_inches='tight', dpi=300)

# Print only necessary output (matching the style of the reference code)
print(f"Saved weekday delays chart to file")

plt.close()
