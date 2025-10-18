"""Script to parse mRNA half-life data from a text file and convert it to CSV format."""

import pandas as pd

file_path = 'all_HLs_human.txt'

with open(file_path) as inf:
    lines = []
    for line in inf:
        line = line.strip()
        line_items = line.split()
        lines.append(line_items)

with open('mRNA_half_life.csv', 'w') as outf:
    for line in lines:
        outf.write(','.join(line) + '\n')