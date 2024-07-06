import pandas as pd
import matplotlib.pyplot as plt

# Read the output file into a pandas DataFrame
df = pd.read_csv('./part-r-00000.csv', sep=',', header=None, names=['Recipient', 'Count'])

# Sort the DataFrame by the 'Count' column in descending order
df_sorted = df.sort_values(by='Count', ascending=False)

# Select the top ten email recipients
df_top_ten = df_sorted.head(20)

# Plot the data
plt.figure(figsize=(15, 10))
bars = plt.bar(df_top_ten['Recipient'], df_top_ten['Count'], color='blue')

# Add labels and title
plt.xlabel('Email Recipient', fontsize=14)
plt.ylabel('Number of Emails', fontsize=14)
plt.title('Top 20 Email Recipients', fontsize=16)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, fontsize=12, ha='right')

# Add text annotations on top of each bar (vertically)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha='center', va='bottom', fontsize=10, rotation=90)

# Add gridlines
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Display the plot
plt.tight_layout()
plt.show()
