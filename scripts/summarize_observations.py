#!/usr/bin/env python3
"""Show structured, provenance-aware observations from a project CSV."""
from pathlib import Path
import argparse
import csv

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('csv_file',type=Path)
    args=ap.parse_args()
    with args.csv_file.open(newline='',encoding='utf8') as f:
        rows=list(csv.DictReader(f))
    print(f'{len(rows)} independently recorded metrics')
    for row in rows:
        print(f"{row['id']:7} {row['metric']:35} {row['value']:>10} {row['units']:20} source={row['source']} ({row['interpretation']})")
if __name__=='__main__':main()
