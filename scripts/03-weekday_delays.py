import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# Find the repository root directory
current_file = Path(__file__)
# Go up from current script location to find the root
repo_root = current_file.parent.parent
data_path = repo_root / "data" / "analysis_data" / "2025plus_data.csv"

# Load the dataset
df = pd.read_csv(data_path)

# Group by day and date to get unique days in the dataset
# First, create a combined Date-Day identifier
df['Date_Day'] = df['Date'] + '_' + df['Day']

# Count total occurrences per day
day_occurrences = df.groupby('Day')['Date_Day'].nunique()

# Count delays by day of the week
day_counts = df['Day'].value_counts()

# Calculate average delays per day occurrence
avg_delays_per_day = day_counts / day_occurrences

# Calculate percentages for the pie chart
total_avg = avg_delays_per_day.sum()
day_percentages = (avg_delays_per_day / total_avg * 100).round(1)

# Define colors for each day
colors = ['#4285F4', '#80CBC4', '#E91E63', '#F57C00', '#FFC107', '#8BC34A', '#673AB7']

# Create a custom order for days of the week
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
ordered_percentages = day_percentages.reindex(days_order)

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
save_path = repo_root / "outputs" / "03-weekday_delays.png"
plt.savefig(save_path, bbox_inches='tight', dpi=300)

# Print only necessary output (matching the style of the reference code)
print(f"Saved weekday delays chart to file")

plt.close()
