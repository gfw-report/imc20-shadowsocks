#!/usr/bin/env python3

import getopt
import sys

import pandas as pd

# Output the table in two side-by-side pieces to save space.
COLUMN_BREAKPOINT = 6

_, (csv_filename,) = getopt.gnu_getopt(sys.argv[1:], "")
data = pd.read_csv(csv_filename)

def asn_as_int(asn):
    assert asn.startswith("AS"), asn
    return int(asn[2:])

freq_table = data["asn"].map(asn_as_int).value_counts().sort_index(ascending=False).sort_values(ascending=False)

rows = []
for i, (asn, count) in enumerate(freq_table.items()):
    cells = [rf"AS{asn:<5}", rf"{count:>4}"]
    if i < COLUMN_BREAKPOINT:
        rows.append(cells)
    elif i < COLUMN_BREAKPOINT * 2:
        rows[i - COLUMN_BREAKPOINT].extend(cells)
    else:
        rows.append(["       ", "    "] + cells)

print(r"\begin{tabular}{lr@{\qquad}lr}")
print(" \\\\\n".join(" & ".join(row) for row in rows))
print(r"\end{tabular}")
