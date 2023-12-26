import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("word_statistics.csv")

plt.figure(figsize=(12, 6))
plt.hist(df['Average Time'], bins=20, color='orange')
plt.title('Histogram of Average Time per Word')
plt.xlabel('Average Time (s)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig("plots/average_time_histogram.png")  # Save the figure
plt.close()  # Close the figure

plt.figure(figsize=(12, 6))
df.boxplot(column=['Average Time'])
plt.title('Box plot of Average Time per Word')
plt.ylabel('Time (s)')
plt.savefig("plots/average_time_boxplot.png")  # Save the figure
plt.close()  # Close the figure
