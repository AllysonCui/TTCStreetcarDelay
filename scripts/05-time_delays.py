import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Find the repository root directory
current_file = Path(__file__)
# Go up from current script location to find the root
repo_root = current_file.parent.parent

data_path = repo_root / "data" / "analysis_data" / "2025plus_data.csv"

# Load the data
data = pd.read_csv(data_path)

# Extract hour from the 'Time' column
# First, ensure the 'Time' column is in string format
data['Time'] = data['Time'].astype(str)

# Extract hour, handle 'None' values
def extract_hour(time_str):
    if time_str == 'None' or pd.isna(time_str):
        return np.nan
    time_parts = time_str.split(':')
    if len(time_parts) >= 2:
        try:
            return int(time_parts[0])  # Extract just the hour as an integer
        except ValueError:
            return np.nan
    return np.nan

data['Hour'] = data['Time'].apply(extract_hour)

# Create a dataframe with all hours (0-23)
all_hours = pd.DataFrame({'Hour': range(24)})

# Count delays by hour
hour_counts = data['Hour'].value_counts().reset_index()
hour_counts.columns = ['Hour', 'Count']

# Merge with all_hours to ensure we have all 24 hours
hour_counts = pd.merge(all_hours, hour_counts, on='Hour', how='left').fillna(0)
hour_counts['Count'] = hour_counts['Count'].astype(int)

# Create time range strings (e.g., "00:00 - 00:59")
def create_time_range(hour):
    return f"{hour:02d}:00 - {hour:02d}:59"

hour_counts['Time Range'] = hour_counts['Hour'].apply(create_time_range)

# Sort by Hour
hour_counts = hour_counts.sort_values('Hour')

# Set up the figure and plot
plt.figure(figsize=(14, 8))

# Create the bar chart with proper hue parameter instead of palette
# Using the x variable for hue and setting legend=False, as suggested in the warning
ax = sns.barplot(
    x='Time Range',
    y='Count',
    hue='Time Range',  # Use x variable for hue
    legend=False,      # Set legend=False to avoid duplicating the information
    data=hour_counts
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
for i, count in enumerate(hour_counts['Count']):
    if count > 0:  # Only add labels for bars with non-zero values
        ax.text(i, count + 1, str(count), ha='center', fontsize=10)

# Save the figure
save_path = repo_root / "outputs" / "05-delay_time_barchart.png"
plt.savefig(save_path, bbox_inches='tight', dpi=300)

print(f"Saved delay times bar chart to file: {save_path}")
plt.close()
