import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar

# Define path to data file
data_file = "../data/analysis_data/2025plus_data.csv"

# Load the data
df = pd.read_csv(data_file)

# Convert the Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Extract year and month
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Count delays by year and month
monthly_counts = df.groupby(['Year', 'Month']).size().reset_index(name='Count')

# Get unique years and months in the data
years = sorted(monthly_counts['Year'].unique())
months_present = sorted(monthly_counts['Month'].unique())

print(f"Years found in data: {years}")
print(f"Months found in data: {months_present}")

# Find the month with the highest average number of delays
# Group by month and calculate mean across years
avg_by_month = monthly_counts.groupby('Month')['Count'].mean()
max_month_num = avg_by_month.idxmax()
max_month_name = calendar.month_name[max_month_num]

print(f"Month with highest average delays: {max_month_name} ({max_month_num})")

# Convert the month numbers to month names
month_names = [calendar.month_name[month] for month in months_present]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

# Available colors for years
color_palette = ['#4285F4', '#4ecdc4', '#F87171', '#6366F1', '#A78BFA',
                 '#EC4899', '#F97316']

# Create a pivot table for easier plotting
pivot_df = pd.pivot_table(
    monthly_counts,
    values='Count',
    index='Month',
    columns='Year',
    fill_value=0
)

# Only keep the months that are present in the data
pivot_df = pivot_df.loc[months_present]

# Convert numpy int32 to regular Python int for years (for cleaner labels)
years = [int(year) for year in years]


# Helper function to format values to k format with one decimal
def format_to_k(val):
    if val >= 1000:
        # Format to one decimal place and add k
        return f"{val / 1000:.1f}k".replace('.0k',
                                            'k')  # Remove .0 if it's a whole number
    else:
        # For small numbers, just return the integer
        return f"{val}"


# Plotting based on number of years
if len(years) == 1:
    # Single year - simple bar chart
    year = years[0]
    year_data = pivot_df[year].values
    # Include the year in the label for the legend
    bars = ax.bar(month_names, year_data, color=color_palette[0], width=0.8,
                  label=str(year))

    # Add value annotations under the top of the bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height - (height * 0.05),
                # Position text 5% below top
                format_to_k(height),
                ha='center', va='top', color='black', fontsize=9)
else:
    # Multiple years - stacked bar chart
    bottom = np.zeros(len(months_present))
    all_bars = []  # Store all bar collections

    for i, year in enumerate(years):
        if year in pivot_df.columns:
            # Get data for this year
            year_data = pivot_df[year].values

            # Select color from palette
            color = color_palette[i % len(color_palette)]

            # Plot the bars
            bars = ax.bar(month_names, year_data, label=str(year), color=color,
                          width=0.8, bottom=bottom)

            # For each bar in this year's set
            for j, bar in enumerate(bars):
                # Calculate where to put the text (just below the top of this section)
                bar_height = bar.get_height()
                text_y = bottom[j] + bar_height - (
                            bar_height * 0.1)  # 10% below the top of this section

                # Add the text if the bar is tall enough to be visible
                if bar_height > 100:  # Only label bars with significant height
                    ax.text(bar.get_x() + bar.get_width() / 2., text_y,
                            format_to_k(bar_height),
                            ha='center', va='top', color='black', fontsize=9,
                            fontweight='bold', alpha=0.9)

            all_bars.append(bars)
            # Update bottom for next stack
            bottom += year_data

# Set plot title with the month that has the highest average delays
ax.set_title(f'Most of the Delays occur during {max_month_name} :', fontsize=16,
             loc='left')

# Set y-axis ticks
max_value = pivot_df.values.max() * (2 if len(years) > 1 else 1.2)

# Determine the appropriate y-axis maximum based on data
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

# Add gridlines
ax.grid(axis='y', linestyle='-', alpha=0.2)

# Add the legend, regardless of the number of years
ax.legend(loc='upper left')

# Adjust layout
plt.tight_layout()

# Save the figure
output_path = "../outputs/02-monthly_delays.png"
plt.savefig(output_path, dpi=300)
print(f"Figure saved to: {output_path}")

# Close the figure to release memory
plt.close(fig)
