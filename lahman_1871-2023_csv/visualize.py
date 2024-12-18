import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data
df = pd.read_csv('lahman_1871-2023_csv/HallOfFameDataset.csv')

# Display the first few rows of the DataFrame
print(df.head())

# Example visualization: Plotting HRs vs Runs
plt.figure(figsize=(10, 6))
plt.scatter(df['HR'], df['R'])
plt.title('HRs vs Runs')
plt.xlabel('Home Runs')
plt.ylabel('Runs')
plt.grid(True)
plt.show()
