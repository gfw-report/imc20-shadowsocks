#!/usr/bin/env python3

from collections import Counter
import getopt
import os.path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import common

FIGSIZE = (common.COLUMNWIDTH, 1.75)

source_ip = []
_, (output_filename, *input_filenames) = getopt.gnu_getopt(sys.argv[1:], "")
for filename in input_filenames:
    _, ext = os.path.splitext(filename)
    if ext == ".txt":
        with open(filename) as f:
            source_ip.extend(line.strip() for line in f)
    elif ext == ".csv":
        source_ip.extend(pd.read_csv(filename, sep=";")["ip_src"])
    else:
        raise ValueError(f"unrecognized input filename extension in {filename}")

counter_of_source_ip = Counter(source_ip)
print(counter_of_source_ip.most_common(10))

ip_occurrences = list(counter_of_source_ip.values())
ip_occurrences.sort()

prober_ips = list(counter_of_source_ip.keys())
total_number_of_unique_prober_ip = len(prober_ips)

fig = plt.figure(figsize=FIGSIZE)
ax = plt.axes()
ax.margins(0, 0.02)

ax.axhline(y=total_number_of_unique_prober_ip,
    label="Number of unique IP addresses: {}".format(total_number_of_unique_prober_ip),
    color="r", alpha=0.4)

c = Counter(ip_occurrences)
x = [elem[0] for elem in sorted(c.items())]
n = [elem[1] for elem in sorted(c.items())]
ax.step([0] + x, np.cumsum([0] + n), where="post")

ax.set(xlabel="Number of probes sent from one IP address", ylabel="Count of IP addresses")
plt.legend()

fig.subplots_adjust(left=0.15, bottom=0.18, right=0.99, top=0.97)
plt.savefig(output_filename, metadata={"CreationDate": None})
