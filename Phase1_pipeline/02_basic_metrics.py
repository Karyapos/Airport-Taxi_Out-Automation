import pandas as pd
import sys
import json
def basic_numbers(filepath):
    df=pd.read_csv(filepath)
    INT_COLUMNS    = {"taxi_out", "departures_traffic", "arrivals_traffic",
                   "distance_scheduled", "wind_speed"} 
    results = {}
    for col in INT_COLUMNS :
        col_numbers = {}
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3-Q1
        col_numbers= {
            "mean" : round(df[col].mean(),2),
            "std" : round(df[col].std(),2),
            "min" : int(df[col].min()),
            "max" : int(df[col].max())}
        for multiplier in [1.5,2.,3.]: 
            lower= Q1-multiplier*IQR
            upper = Q3+multiplier*IQR
            outliers = df[(df[col]<lower) |(df[col]>upper)]
            col_numbers[multiplier]= len(outliers)
        results[col]=col_numbers
    with open ("numbers.json","w") as file:
        json.dump(results,file,indent=2)
    print("numbers.json is already created and saved!")

if len(sys.argv) != 2:
    print("Usage: python detect.py <path_to_csv>")
    sys.exit(1)
basic_numbers(sys.argv[1])