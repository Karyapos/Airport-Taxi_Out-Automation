import pandas as pd
import sys
df = pd.read_csv("all_data.csv")


df = df.sample(frac=0.1, random_state=42)

if len(sys.argv)!=2:
    print("Usage: python samples_creator.py <number>")
    sys.exit(1)
df.to_csv(f"sample{sys.argv[1]}.csv", index=False)