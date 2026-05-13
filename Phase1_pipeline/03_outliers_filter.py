import json
import sys
import pandas as py
cv_low=0.2
cv_high=0.5
# the databaset examined has 5600 rows
#thresholds examined are 0.5% 0.2% 0.1%
light_fence = 28
medium_fence = 11
tight_fence = 5
outliers_report = {}
def outliers_filtering(filepath):
    with open(filepath) as f:
        metrics = json.load(f)
    for col,m in metrics.items():
        mean = m["mean"]
        std = m["std"]
        n15 = m["1.5"]
        n20 = m["2.0"]
        n30 = m["3.0"]
        cv = std/mean
        if cv < cv_low:
            spread = "LOW"
            barrier = light_fence
        elif cv < cv_high :
            spread = "MEDIUM"
            barrier = medium_fence
        else :
            spread = "HIGH"
            barrier = tight_fence
        if n30 >0 and n30<barrier:
            outliers_report[col]= 3.0
        elif n20>0 and n20<barrier:
            outliers_report[col]= 2.0
        else: 
            if n15>0  and n15<barrier:
                outliers_report[col]=1.5
    with open ("outliers_report.json","w") as file:
        json.dump(outliers_report,file,indent=2)
    print("outliers_report.json is already created and saved!")
if len(sys.argv)<2 :
    print("Please provide json file with basic metrics to be examined")
    sys.exit(1)
else: outliers_filtering(sys.argv[1])
