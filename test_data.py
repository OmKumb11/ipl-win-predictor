import pandas as pd

# Load the files
matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

# Print the first 2 rows to check
print("--- MATCHES (The Result) ---")
print(matches.head(2))

print("\n--- DELIVERIES (The Story) ---")
print(deliveries.head(2))