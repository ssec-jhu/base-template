import json
import os

if __name__ == "__main__":
    # Read the coverage data from a file
    with open('coverage.json', 'r') as f:
        coverage_data = json.load(f)

    total = int(coverage_data["totals"]["percent_covered_display"])

    color = "green" if total >= 90 else "yellow" if total >= 80 else "red"

    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"percent={total}\n")
        f.write(f"color={color}\n")
