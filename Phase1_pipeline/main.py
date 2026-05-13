import subprocess
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python main.py <path_to_csv>")
    sys.exit(1)

csv = sys.argv[1]

steps = [
    (["python", "01_validate_csv.py", csv],          "01 — validate"),
    (["python", "02_basic_metrics.py", csv],          "02 — basic metrics"),
    (["python", "03_outliers_filter.py", "numbers.json"], "03 — outlier filter"),
    (["python", "04_outliers_printer.py", "outliers_report.json", csv], "04 — outlier rows"),
]

for cmd, label in steps:
    print(f"\n{'─'*40}\n{label}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"FAILED at {label} — pipeline stopped.")
        sys.exit(1)

print("\n✓ pipeline complete")