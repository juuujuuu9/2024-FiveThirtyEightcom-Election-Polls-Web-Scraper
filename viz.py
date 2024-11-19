import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the CSV data into a DataFrame
filename = "polls_snapshot_2024-10-26_23-21-13.csv"  # Replace with the actual filename
data = pd.read_csv(filename)

# Convert the 'Date' column to a datetime format if needed (based on expected date format)
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # 'coerce' turns invalid parsing into NaT

# Drop rows with NaT dates (optional, depending on whether date parsing is essential)
data.dropna(subset=['Date'], inplace=True)

# 1. Bar Chart - Distribution of Party Affiliation
plt.figure(figsize=(8, 6))
sns.countplot(data=data, x='Party', palette='viridis')
plt.title('Distribution of Party Affiliation')
plt.xlabel('Party')
plt.ylabel('Count')
plt.show()

# 2. Line Chart - Net Values Over Time by Party (if data spans multiple dates)
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='Date', y='Net', hue='Party', marker='o')
plt.title('Net Values Over Time by Party')
plt.xlabel('Date')
plt.ylabel('Net Value')
plt.show()

# 3. Pie Chart - Party Affiliation Proportion
party_counts = data['Party'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(party_counts, labels=party_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis'))
plt.title('Party Affiliation Proportion')
plt.show()

# 4. Heatmap - Cross-tabulation of Sample Type and Party
pivot_table = data.pivot_table(index='Sample Type', columns='Party', aggfunc='size', fill_value=0)
plt.figure(figsize=(10, 8))
sns.heatmap(pivot_table, annot=True, fmt="d", cmap='coolwarm', linewidths=.5)
plt.title('Sample Type vs. Party Affiliation')
plt.xlabel('Party')
plt.ylabel('Sample Type')
plt.show()
