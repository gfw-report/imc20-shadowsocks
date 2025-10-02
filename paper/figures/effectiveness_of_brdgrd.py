#!/usr/bin/env python3

import getopt
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import common

FIGSIZE = (common.COLUMNWIDTH, 1.75)
BRDGRD_ENABLED_INTERVALS = (
    (pd.to_datetime("2019-11-04 04:45:02"), pd.to_datetime("2019-11-05 16:08:17")),
    (pd.to_datetime("2019-11-08T21:10:34"), None),
)

# Read packets from CSV.
WANTED_COLUMNS = [
    "tcp_flags",
    "is_legit",
    "frame_epoch_time",
    "frame_relative_time",
]
_, (csv_filename, output_filename) = getopt.gnu_getopt(sys.argv[1:], "")
csv_iter = pd.read_csv(csv_filename, usecols=WANTED_COLUMNS, delimiter=";", iterator=True, chunksize=10000)
packets = pd.concat([
    chunk[chunk["tcp_flags"].map(lambda x: int(x, 0)) == 0x02]
for chunk in csv_iter])
# Convert epoch time to date.
packets["date"] = pd.to_datetime(packets.frame_epoch_time, unit="s")

# Extract the subsets of packets we want to plot.
syn_by_prober = packets[(packets['tcp_flags'].map(lambda x: int(x, 0)) == 0x02) &
                        (packets['is_legit'] == False)]
syn_by_client = packets[(packets['tcp_flags'].map(lambda x: int(x, 0)) == 0x02) &
                        (packets['is_legit'] == True)]

start_date = min(packets["date"])
end_date = max(packets["date"])

LEGIT_CONNECTION_INTERVALS = (
    (start_date, max(syn_by_client["date"])),
)

fig = plt.figure(figsize=FIGSIZE)
ax = plt.axes()
ax.margins(0, 0)
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(50))

# Hourly intervals.
bins = pd.date_range(start_date, end_date, freq="H")

num_syn_by_client = pd.cut(syn_by_client["date"], bins).value_counts().sort_index()
num_syn_by_prober = pd.cut(syn_by_prober["date"], bins).value_counts().sort_index()
max_syn_by_prober = max(num_syn_by_prober)

# Format the x-axis as a relative number of hours.
xaxis = (bins[:-1] - start_date).total_seconds() / 3600

# Plot the times when brdgrd was enabled.
for (start, end) in BRDGRD_ENABLED_INTERVALS:
    if start is None:
        start = start_date
    if end is None:
        end = end_date
    ax.axvspan(
        (start - start_date).total_seconds() / 3600,
        (end - start_date).total_seconds() / 3600,
        color="orange", alpha=0.4,
    )
    if (end - start).days > 5:
        ax.text(
            (start + (end - start)/2 - start_date).total_seconds() / 3600, 0.45,
            "Brdgrd active", #fontsize="small",
            transform=matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes),
            horizontalalignment="center", verticalalignment="center",
        )

# Plot the times when legitimate client connections were happening.
for (start, end) in LEGIT_CONNECTION_INTERVALS:
    y = 0.8
    h = 0.15
    ax.axvspan(
        (start - start_date).total_seconds() / 3600,
        (end - start_date).total_seconds() / 3600,
        y - h/2, y + h/2,
        color=common.COLOR_LEGIT, alpha=0.4,
    )
    ax.text(
        (start + (end - start)/2 - start_date).total_seconds() / 3600, y,
        "Legitimate client connections active", #fontsize="small",
        transform=matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes),
        horizontalalignment="center", verticalalignment="center",
    )

# Draw the bars a bit wider than 1 hour, so they overlap.
ax.bar(xaxis, num_syn_by_prober, 1.1)

ax.set(xlabel="Relative time (hours)", ylabel="Prober SYNs per hour")
fig.subplots_adjust(left=0.11, bottom=0.18, right=0.97, top=0.98)
plt.savefig(output_filename, metadata={"CreationDate": None})
