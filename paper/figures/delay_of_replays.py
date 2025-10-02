#!/usr/bin/env python3

# Usage: delay_of_replays.py delay_of_replays.csv delay_of_replays_in_all_experiments.pdf

import csv
import getopt
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import common

FIGSIZE = (common.COLUMNWIDTH, 2.5)

def parse_bool(v):
    if v == "F":
        return False
    elif v == "T":
        return True
    else:
        raise ValueError(f"unknown boolean value {v!r}")

delay_of_first_replay = []
delay_of_replay = []
_, (csv_filename, output_filename) = getopt.gnu_getopt(sys.argv[1:], "")
with open(csv_filename) as f:
    for row in csv.DictReader(f):
        is_first = parse_bool(row["is_first"])
        delay = float(row["delay"])

        if is_first:
            delay_of_first_replay.append(delay)
        delay_of_replay.append(delay)

# print(len(delay_of_first_replay))
# print(len(delay_of_replay))


fig = plt.figure(figsize=FIGSIZE)
ax = plt.axes()
ax.margins(0, 0.02)
ax.set_xscale("log")
ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.25))
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))

# Draw a labeled vertical line at significant milestones.
for x, y, label in (
    (1, 0.54, "1 second"),
    (1*60, 0.54, "1 minute"),
    (15*60, 0.12, "15 minutes"),
    (60*60, 0.54, "1 hour"),
    (10*60*60, 0.54, "10 hours"),
):
    ax.axvline(x, color="gray", linewidth=0.8)
    ax.text(x, y, label, color="gray", rotation=90, horizontalalignment="right", verticalalignment="bottom")

# Add labels for minimum and maximum delays.
ax.annotate(
    "Minimum delay: {:.2f} s".format(min(delay_of_replay)),
    xy=(min(delay_of_replay), 0.0),
    textcoords="offset points", xytext=(19, 0),
    horizontalalignment="left", verticalalignment="bottom",
)
ax.annotate(
    "Maximum delay:\n{:.2f} h".format(max(delay_of_replay)/3600),
    xy=(max(delay_of_replay), 1.0),
    textcoords="offset points", xytext=(-2, -4),
    horizontalalignment="right", verticalalignment="top",
)

# Plot CDFs. NB the colors orange and blue are referred to in the text.
ax.step(*common.cdf(delay_of_first_replay), where="post", label="First replay", color="darkorange")
ax.step(*common.cdf(delay_of_replay), where="post", label="All replays", color="blue")

ax.set(xlabel="Delay until replay of legitimate connection (seconds)")
ax.legend(loc="lower right")

fig.subplots_adjust(left=0.11, bottom=0.14, right=0.99, top=0.98)
fig.savefig(output_filename, metadata={"CreationDate": None})
