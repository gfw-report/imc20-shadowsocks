#!/usr/bin/env python3

# Usage: ./cdf_source_port_lon15.py cdf_source_port_lon15/bj17_lon15_exp1.csv.xz cdf_source_port_lon15.pdf

import getopt
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import common

FIGSIZE = (common.COLUMNWIDTH, 2.0)

# Read packets from CSV.
_, (csv_filename, output_filename) = getopt.gnu_getopt(sys.argv[1:], "")
csv_iter = pd.read_csv(csv_filename, delimiter=";", iterator=True, chunksize=10000)
packets = pd.concat([
    chunk[chunk["tcp_flags"].map(lambda x: int(x, 0)) == 0x02]
for chunk in csv_iter])

syn_by_prober = packets[packets["tcp_flags"].map(lambda x: int(x, 0) == 0x02) &
                        (packets["is_legit"] == False)]
prober_tcp_srcport = syn_by_prober["tcp_srcport"]

print("Number of probes:", len(prober_tcp_srcport))

fig = plt.figure(figsize=FIGSIZE)
ax = plt.axes()
ax.margins(0, 0.02)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))

ax.axvspan(32768, 60999, alpha=0.4, color="orange", label="Common Linux Source Port: 32768-60999")
ax.text((32768 + 60999)/2, 0.07, "Common Linux source ports\n32768–60999",
    fontsize="small",
    horizontalalignment="center", verticalalignment="center",
    transform=matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes))

ax.plot(*common.cdf(prober_tcp_srcport))
min_port = min(prober_tcp_srcport)
max_port = max(prober_tcp_srcport)
ax.text(min_port, 0.1, f"Lowest observed: {min_port}",
    horizontalalignment="left",
    transform=matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes))
ax.text(0.85, 0.9, f"Highest observed: {max_port}",
    horizontalalignment="right",
    transform=ax.transAxes)

ax.set(xlabel="TCP source port of prober SYN packets", xlim=(0, 65535))

fig.subplots_adjust(left=0.10, bottom=0.17, right=0.99, top=0.98)
plt.savefig(output_filename, metadata={"CreationDate": None})
