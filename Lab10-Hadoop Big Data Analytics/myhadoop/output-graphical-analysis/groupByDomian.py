import pandas as pd
import matplotlib.pyplot as plt

# Function to extract domain from email
def extract_domain(email):
    return email.split('@')[-1]

# Read the output file into a pandas DataFrame
df = pd.read_csv('part-r-00000.csv', sep=',', header=None, names=['Recipient', 'Count'])

# Extract domain from each email recipient
df['Domain'] = df['Recipient'].apply(extract_domain)

# Group by domain and sum the counts
domain_counts = df.groupby('Domain')['Count'].sum().reset_index()

# Sort the DataFrame by the 'Count' column in descending order
domain_counts_sorted = domain_counts.sort_values(by='Count', ascending=False)

# Plot the data
plt.figure(figsize=(15, 10))
bars = plt.bar(domain_counts_sorted['Domain'], domain_counts_sorted['Count'], color='skyblue')

# Add labels and title
plt.xlabel('Email Domain', fontsize=12)
plt.ylabel('Number of Emails', fontsize=12)
plt.title('Number of Emails per Domain', fontsize=14)

# Rotate x-axis labels for better readability
plt.xticks(rotation=90, fontsize=10)

# Set y-axis range from 0 to 5000
plt.ylim(0, 5000)

# Add gridlines
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add text annotations on top of each bar (vertically)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 20, int(yval), ha='center', va='bottom', fontsize=10, rotation=90)

# Display the plot
plt.tight_layout()
plt.show()
