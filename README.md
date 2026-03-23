# 🏋️ Fitness Tracker Datasets Analysis

A data analysis project exploring physical activity, calorie expenditure, 
and sleep patterns across 30 Fitbit users using Python.

## 📊 Project Overview
This project analyzes three real-world fitness tracker datasets to uncover 
behavioral trends, compute dynamic metrics, and generate meaningful visualizations.

## 📁 Datasets Used
| File | Rows | Columns | Description |
|------|------|---------|-------------|
| `dailyActivity_merged.csv` | 941 | 15 | Steps, distance, active minutes, calories |
| `sleepDay_merged.csv` | 414 | 5 | Sleep records, minutes asleep, time in bed |
| `dailyCalories_merged.csv` | 941 | 3 | Daily calorie burn per user |

## 📈 Visualizations & Insights
- **Line chart** – Total steps per day across all users
- **Line chart** – Average calories burned per day
- **Histogram** – Distribution of sleep efficiency (computed metric)
- **Pie chart** – Breakdown of activity intensity levels
- **Scatter plot** – Total distance vs. calories burned
- **Stem plot** – Calories burned over time
- **Event plot** – Calorie comparison between two users
- **Box plot** – Daily calorie distribution grouped by date
- **Heatmap** – Step count vs. calories frequency
- **Multi scatter** – Calories vs. very/moderately/lightly active distances

## Dynamic Metrics Computed
- **Sleep Efficiency** = (TotalMinutesAsleep / TotalTimeInBed) × 100
- **Average Speed** = TotalActiveMinutes / TotalActiveDistance (min/mile)
- **Activity intensity breakdown** percentages per average user

## 🛠️ Tools & Libraries
- Python 3
- Pandas
- Matplotlib
- NumPy

## 🚀 How to Run
```bash
pip install pandas matplotlib numpy
python analysis.py
```

## 👩‍💻 Authors
- Noor Daas (ID: 0219290)
- Ayah Saadeh (ID: 0215258)

*Computer Applications Lab — 0907331, Spring 2023/2024*
