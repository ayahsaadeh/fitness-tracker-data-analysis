# =============================================================================
# Fitness Tracker Datasets Analysis
# Course: Computer Applications Lab — 0907331, Spring 2023/2024
# Authors: Noor Daas (0219290) & Ayah Saadeh (0215258)
# =============================================================================
# Datasets used:
#   - dailyActivity_merged.csv  (941 rows, 15 columns)
#   - sleepDay_merged.csv       (414 rows,  5 columns)
#   - dailyCalories_merged.csv  (941 rows,  3 columns)
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# 1. LOAD DATASETS
# =============================================================================

daily_activity = pd.read_csv('dailyActivity_merged.csv')
sleep_day      = pd.read_csv('sleepDay_merged.csv')
daily_calories = pd.read_csv('dailyCalories_merged.csv')

# =============================================================================
# 2. DATA CLEANING
# =============================================================================

# -- Convert date columns to datetime --
daily_activity['ActivityDate'] = pd.to_datetime(
    daily_activity['ActivityDate'], format='%m/%d/%Y')

sleep_day['SleepDay'] = pd.to_datetime(
    sleep_day['SleepDay'], format='%m/%d/%Y %I:%M:%S %p')

daily_calories['ActivityDay'] = pd.to_datetime(
    daily_calories['ActivityDay'], format='%m/%d/%Y')

# -- Drop duplicate rows --
daily_activity = daily_activity.drop_duplicates()
sleep_day      = sleep_day.drop_duplicates()
daily_calories = daily_calories.drop_duplicates()

# -- Quick summary --
print("=" * 60)
print("Dataset shapes after cleaning:")
print(f"  daily_activity : {daily_activity.shape}")
print(f"  sleep_day      : {sleep_day.shape}")
print(f"  daily_calories : {daily_calories.shape}")
print("=" * 60)
print("\nMissing values:")
print("daily_activity:\n", daily_activity.isnull().sum())
print("sleep_day:\n",      sleep_day.isnull().sum())
print("daily_calories:\n", daily_calories.isnull().sum())
print("=" * 60)

# =============================================================================
# 3. PLOT 1 — Total Steps per Day (Line Chart)
# =============================================================================
# Shows the total steps taken by all users combined on each date.
# Peaks indicate days of higher collective physical activity.

steps_per_day = (daily_activity
                 .groupby('ActivityDate')['TotalSteps']
                 .sum()
                 .reset_index())

plt.figure(figsize=(10, 6))
plt.plot(steps_per_day['ActivityDate'], steps_per_day['TotalSteps'],
         marker='o', color='steelblue')
plt.title('Total Steps per Day', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Total Steps')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('plot1_total_steps_per_day.png', dpi=150)
plt.show()

# =============================================================================
# 4. PLOT 2 — Average Calories Burned per Day (Line Chart)
# =============================================================================
# Displays the average daily caloric expenditure across all users.
# Helps identify days where users were more or less active overall.

avg_calories_per_day = (daily_calories
                        .groupby('ActivityDay')['Calories']
                        .mean()
                        .reset_index())

plt.figure(figsize=(10, 6))
plt.plot(avg_calories_per_day['ActivityDay'],
         avg_calories_per_day['Calories'],
         marker='o', color='orange')
plt.title('Average Calories Burned per Day', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Average Calories')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('plot2_avg_calories_per_day.png', dpi=150)
plt.show()

# =============================================================================
# 5. PLOT 3 — Distribution of Sleep Efficiency (Histogram)
# =============================================================================
# DYNAMIC METRIC: Sleep Efficiency = (TotalMinutesAsleep / TotalTimeInBed) x 100
# Shows how efficiently users sleep — i.e. what fraction of bed time is
# actually spent asleep. The WHO recommends 85% or higher.

sleep_day['SleepEfficiency'] = (
    sleep_day['TotalMinutesAsleep'] / sleep_day['TotalTimeInBed'] * 100
)

plt.figure(figsize=(10, 6))
plt.hist(sleep_day['SleepEfficiency'], bins=20,
         color='teal', edgecolor='black', alpha=0.85)
plt.axvline(85, color='red', linestyle='--', linewidth=1.5,
            label='85% Recommended Threshold')
plt.title('Distribution of Sleep Efficiency', fontsize=14, fontweight='bold')
plt.xlabel('Sleep Efficiency (%)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('plot3_sleep_efficiency.png', dpi=150)
plt.show()

print(f"\nAverage sleep efficiency: {sleep_day['SleepEfficiency'].mean():.1f}%")
print(f"Users meeting 85% threshold: "
      f"{(sleep_day['SleepEfficiency'] >= 85).mean()*100:.1f}% of records")

# =============================================================================
# 6. PLOT 4 — Activity Intensity Breakdown (Pie Chart)
# =============================================================================
# DYNAMIC METRIC: Average proportion of lightly / fairly / very active minutes
# per user. Reveals that the vast majority of active time is low-intensity.

avg_light    = daily_activity['LightlyActiveMinutes'].mean()
avg_fairly   = daily_activity['FairlyActiveMinutes'].mean()
avg_very     = daily_activity['VeryActiveMinutes'].mean()

labels = ['Lightly Active', 'Fairly Active', 'Very Active']
sizes  = [avg_light, avg_fairly, avg_very]
colors = ['lightgreen', 'orange', 'red']
explode = (0, 0.05, 0.05)

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=140, explode=explode)
plt.title('Activity Intensity Breakdown (Average User)',
          fontsize=14, fontweight='bold')
plt.legend(labels, loc='upper right')
plt.tight_layout()
plt.savefig('plot4_activity_intensity_pie.png', dpi=150)
plt.show()

# =============================================================================
# 7. PLOT 5 — Total Distance vs. Calories Burned (Scatter Plot)
# =============================================================================
# Merges activity and calories datasets to explore whether users who cover
# more distance also burn more calories. A positive correlation is expected.

merged = pd.merge(
    daily_activity, daily_calories,
    left_on=['Id', 'ActivityDate'],
    right_on=['Id', 'ActivityDay']
)

plt.figure(figsize=(10, 6))
plt.scatter(merged['TotalDistance'], merged['Calories_x'],
            alpha=0.5, color='magenta', edgecolors='none')
plt.title('Total Distance vs. Calories Burned', fontsize=14, fontweight='bold')
plt.xlabel('Total Distance (miles)')
plt.ylabel('Calories Burned')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('plot5_distance_vs_calories.png', dpi=150)
plt.show()

# =============================================================================
# 8. PLOT 6 — Total Calories Burned Over Time (Stem Plot)
# =============================================================================
# Each stem represents the total calories burned by all users on that day.
# The drop toward the end of the dataset reflects fewer active users logging data.

cal_by_date = (daily_calories
               .groupby(daily_calories['ActivityDay'].dt.date)['Calories']
               .sum())

plt.figure(figsize=(12, 6))
plt.stem(range(len(cal_by_date)), cal_by_date.values,
         linefmt='b-', markerfmt='bo', basefmt='r-')
plt.title('Total Calories Burned Over Time', fontsize=14, fontweight='bold')
plt.xlabel('Day Index')
plt.ylabel('Total Calories Burned')
plt.xticks(ticks=range(len(cal_by_date)),
           labels=[str(d) for d in cal_by_date.index],
           rotation=45, fontsize=7)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('plot6_calories_stem.png', dpi=150)
plt.show()

# =============================================================================
# 9. PLOT 7 — Daily Calorie Counts for 2 Random Users (Event Plot)
# =============================================================================
# Randomly selects two users and plots each day's calorie count as a vertical
# line. The spread and clustering of lines reveal each user's consistency.

np.random.seed(42)
random_users = daily_calories['Id'].drop_duplicates().sample(n=2, random_state=42)
user1_data   = daily_calories[daily_calories['Id'] == random_users.iloc[0]]
user2_data   = daily_calories[daily_calories['Id'] == random_users.iloc[1]]

fig, ax = plt.subplots(figsize=(10, 5))
ax.eventplot(user1_data['Calories'], lineoffsets=0, linelengths=0.6,
             color='blue',   label=f'User {random_users.iloc[0]}')
ax.eventplot(user2_data['Calories'], lineoffsets=1, linelengths=0.6,
             color='orange', label=f'User {random_users.iloc[1]}')
ax.set_title('Daily Calorie Counts — 2 Random Users',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Calories')
ax.set_yticks([0, 1])
ax.set_yticklabels(['User 1', 'User 2'])
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('plot7_event_plot_two_users.png', dpi=150)
plt.show()

# =============================================================================
# 10. PLOT 8 — Average Speed per User (Line Plot)
# =============================================================================
# DYNAMIC METRIC: Speed = TotalActiveMinutes / TotalActiveDistance (min/mile)
# Combines multiple columns to derive a new metric not present in the raw data.
# Lower values = faster (fewer minutes per mile).

daily_activity['TotalActiveMinutes'] = (
    daily_activity['VeryActiveMinutes'] +
    daily_activity['FairlyActiveMinutes'] +
    daily_activity['LightlyActiveMinutes']
)
daily_activity['TotalActiveDistance'] = (
    daily_activity['VeryActiveDistance'] +
    daily_activity['ModeratelyActiveDistance'] +
    daily_activity['LightActiveDistance']
)

speed_per_user = (daily_activity
                  .groupby('Id')
                  .agg({'TotalActiveMinutes': 'sum',
                        'TotalActiveDistance': 'sum'})
                  .reset_index())

# Avoid division by zero
speed_per_user = speed_per_user[speed_per_user['TotalActiveDistance'] > 0]
speed_per_user['Speed'] = (speed_per_user['TotalActiveMinutes'] /
                            speed_per_user['TotalActiveDistance'])

plt.figure(figsize=(12, 6))
plt.plot(speed_per_user['Id'], speed_per_user['Speed'],
         marker='o', linestyle='-', color='navy')
plt.title('Average Speed (Active Time / Distance) per User',
          fontsize=14, fontweight='bold')
plt.xlabel('User ID')
plt.ylabel('Speed (minutes per mile)')
plt.xticks(rotation=45, fontsize=7)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('plot8_speed_per_user.png', dpi=150)
plt.show()

# =============================================================================
# 11. PLOT 9 — Activity Minutes Distribution (Triptych Histograms)
# =============================================================================
# Three side-by-side histograms showing how often users log very, fairly,
# and lightly active minutes. Most users skew toward light activity.

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Distribution of Activity Minutes by Intensity',
             fontsize=14, fontweight='bold')

axes[0].hist(daily_activity['VeryActiveMinutes'],
             bins=30, color='skyblue', edgecolor='black')
axes[0].set_title('Very Active Minutes')
axes[0].set_xlabel('Minutes')
axes[0].set_ylabel('Frequency')
axes[0].grid(True, linestyle='--', alpha=0.6)

axes[1].hist(daily_activity['FairlyActiveMinutes'],
             bins=30, color='lightgreen', edgecolor='black')
axes[1].set_title('Fairly Active Minutes')
axes[1].set_xlabel('Minutes')
axes[1].set_ylabel('Frequency')
axes[1].grid(True, linestyle='--', alpha=0.6)

axes[2].hist(daily_activity['LightlyActiveMinutes'],
             bins=30, color='salmon', edgecolor='black')
axes[2].set_title('Lightly Active Minutes')
axes[2].set_xlabel('Minutes')
axes[2].set_ylabel('Frequency')
axes[2].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('plot9_activity_minutes_histograms.png', dpi=150)
plt.show()

# =============================================================================
# 12. PLOT 10 — Daily Calorie Distribution by Day (Box Plot)
# =============================================================================
# Each box summarises the spread of calorie values across users on that day.
# Outlier dots above boxes may represent unusually high-activity users.

daily_calories['Day'] = daily_calories['ActivityDay'].dt.to_period('D')

fig, ax = plt.subplots(figsize=(16, 6))
daily_calories.boxplot(column='Calories', by='Day', ax=ax,
                       grid=False, patch_artist=True,
                       boxprops=dict(facecolor='skyblue', color='navy'),
                       medianprops=dict(color='red', linewidth=2))
ax.set_title('Distribution of Daily Calories Burned', fontsize=14,
             fontweight='bold')
plt.suptitle('')   # Remove the automatic pandas suptitle
ax.set_xlabel('Day')
ax.set_ylabel('Calories Burned')
plt.xticks(rotation=45, fontsize=7)
plt.tight_layout()
plt.savefig('plot10_calories_boxplot.png', dpi=150)
plt.show()

# =============================================================================
# 13. PLOT 11 — Steps vs. Calories Heatmap (2D Histogram)
# =============================================================================
# Bins users into step-count and calorie ranges and colours each cell by
# frequency. Darker cells = more common combinations.

plt.figure(figsize=(10, 6))
h = plt.hist2d(daily_activity['TotalSteps'], daily_activity['Calories'],
               bins=(10, 5), cmap='Blues')
plt.colorbar(h[3], label='Frequency')
plt.title('Heatmap: Total Steps vs. Calories Burned',
          fontsize=14, fontweight='bold')
plt.xlabel('Total Steps')
plt.ylabel('Calories Burned')
plt.tight_layout()
plt.savefig('plot11_steps_calories_heatmap.png', dpi=150)
plt.show()

# =============================================================================
# 14. PLOT 12 — Calories vs. Activity Distance by Intensity (3 Scatter Plots)
# =============================================================================
# Shows how each intensity level (very / moderately / lightly active distance)
# relates to total calories burned. Very active distance has the steepest trend.

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Calories Burned vs. Active Distance by Intensity',
             fontsize=14, fontweight='bold')

scatter_data = [
    ('VeryActiveDistance',       'Very Active Distance (miles)',       'Calories burned by Very Active Distance'),
    ('ModeratelyActiveDistance', 'Moderately Active Distance (miles)', 'Calories burned by Moderately Active Distance'),
    ('LightActiveDistance',      'Lightly Active Distance (miles)',    'Calories burned by Lightly Active Distance'),
]

for ax, (col, xlabel, title) in zip(axes, scatter_data):
    ax.scatter(daily_activity[col], daily_activity['Calories'],
               alpha=0.4, color='steelblue', edgecolors='none')
    ax.set_title(title, fontsize=10)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Calories Burned')
    ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('plot12_calories_vs_distance_scatter.png', dpi=150)
plt.show()

# =============================================================================
# END OF ANALYSIS
# =============================================================================
print("\nAll plots generated and saved successfully.")
