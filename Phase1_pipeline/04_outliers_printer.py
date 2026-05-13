import json
import sys
import pandas as pd
def outliers_printer(filepath,data):
    results = {}
    df = pd.read_csv(data)
    with open(filepath) as f:
        decision = json.load(f)
    for col,m in decision.items():
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3-Q1
        lower= Q1 - m * IQR
        upper = Q3 + m * IQR
        results[col]=df[(df[col]<lower) |(df[col]>upper)]
    print(results)
if len(sys.argv) != 3:
    print("Usage: python detect.py <path_to_csv>")
    sys.exit(1)
outliers_printer(sys.argv[1],sys.argv[2])