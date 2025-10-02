#!/usr/bin/env python3

# Usage: replayed_ratio_exp3.py bj6-new_sfo4/bj6-new_sfo4.csv.xz replayed_ratio_exp3.pdf

import getopt
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import common

FIGSIZE = (common.COLUMNWIDTH, 2.0)
BINS = pd.interval_range(0.0, 8.0, 40)

# Read packets from CSV.
WANTED_PAYLOAD_TYPES = [0, 1, 2]
WANTED_COLUMNS = [
    "frame_num",
    "frame_epoch_time",
    "payload_type",
    "entropy",
]
_, (csv_filename, output_filename) = getopt.gnu_getopt(sys.argv[1:], "")
csv_iter = pd.read_csv(csv_filename, usecols=WANTED_COLUMNS, delimiter=";", iterator=True, chunksize=10000)
packets = pd.concat([chunk[chunk.payload_type.isin(WANTED_PAYLOAD_TYPES)] for chunk in csv_iter])

# Extract the subsets of packets we want to plot.
legit_psh_ack_packets = packets[packets.payload_type == 0]
replay_type1_packets = packets[packets.payload_type == 1]
replay_type2_packets = packets[packets.payload_type == 2]

fig = plt.figure(figsize=FIGSIZE)
ax = plt.axes()
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=2))

def count_entropy(packets, bins):
    return pd.cut(packets["entropy"], bins).value_counts().sort_index()

legit_psh_ack_entropy = count_entropy(legit_psh_ack_packets, BINS)
replay_type1_entropy = count_entropy(replay_type1_packets, BINS)
replay_type2_entropy = count_entropy(replay_type2_packets, BINS)

def plot_sequence(num, denom, bins, offset, label, color):
    ax.bar(bins.mid + offset, np.divide(num, denom), 0.15, label=label, color=color, alpha=0.8)

plot_sequence(replay_type1_entropy, legit_psh_ack_entropy, BINS, -0.02, "Identical replay (R1)", common.COLOR_IDENTICAL_REPLAY)
plot_sequence(replay_type2_entropy, legit_psh_ack_entropy, BINS, +0.02, "Byte-changed replay (R2–R5)", common.COLOR_BYTECHANGED_REPLAY)

ax.set(xlabel="Shannon entropy of PSH/ACK packets", ylabel="Ratio of replay-based probes\nto legitimate connections")
legend = ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.95))
# Make legend markers fully opaque: https://stackoverflow.com/a/42403471.
for handle in legend.legendHandles:
    handle.set_alpha(1)

fig.subplots_adjust(left=0.20, bottom=0.16, right=0.98, top=0.98)
fig.savefig(output_filename, metadata={"CreationDate": None})
