#!/usr/bin/env python3

# Usage: cdf_payload_length_exp1a.py bj3-new_sfo1_ncatlike_all_columns_added.csv cdf_payload_length_exp1a.pdf

import getopt
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import common

FIGSIZE = (common.COLUMNWIDTH, 2.5)
# When Exp 1 was switched from sink mode (Exp 1.a) to responding mode (Exp 1.b).
RESPONDING_EXP_START_TS = 1590727761.602623000

# Read packets from CSV.
WANTED_PAYLOAD_TYPES = [0, 1, 2, 3]
_, (csv_filename, output_filename) = getopt.gnu_getopt(sys.argv[1:], "")
csv_iter = pd.read_csv(csv_filename, delimiter=";", iterator=True, chunksize=10000)
packets = pd.concat([
    chunk[chunk.payload_type.isin(WANTED_PAYLOAD_TYPES) & (chunk.frame_epoch_time < RESPONDING_EXP_START_TS)]
for chunk in csv_iter])

# Extract the subsets of packets we want to plot.
legit_psh_ack_packets = packets[packets.payload_type == 0]
replay_type1_packets = packets[packets.payload_type == 1]
replay_type2_packets = packets[packets.payload_type == 2]
non_replay_packets = packets[packets.payload_type == 3]

print(replay_type1_packets[replay_type1_packets.payload_len == 168])
print(replay_type1_packets[replay_type1_packets.payload_len == 264])
print(replay_type1_packets[replay_type1_packets.payload_len == 384])
print(replay_type1_packets[replay_type1_packets.payload_len == 688])
for (left, right), remainders in (
    ((168, 263), (9,)),
    ((264, 383), (9, 2)),
    ((384, 687), (2,)),
):
    group = replay_type1_packets[(left <= replay_type1_packets.payload_len) & (replay_type1_packets.payload_len <= right)]
    total = len(group)
    parts = [f"total: {total}"]
    for r in remainders:
        n = len(group[group.payload_len % 16 == r])
        parts.append(f"remainder {r}: {n} ({float(n) / total * 100:.1f}%)")
    print(f"{left}--{right}: " + "; ".join(parts))

fig = plt.figure(figsize=FIGSIZE)
ax = plt.axes()
ax.margins(0, 0.02)
ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.25))
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))

# Plot a CDF of the payload_len of the given packets.
def plot_cdf(packets, label, color):
    ax.step(
        *common.cdf(packets.payload_len),
        where="post",
        color=color, alpha=0.8,
        label=f"{label}\nN={len(packets)} min={min(packets.payload_len)} max={max(packets.payload_len)}",
    )

plot_cdf(legit_psh_ack_packets, "Trigger connections", common.COLOR_LEGIT)
plot_cdf(replay_type1_packets, "Identical replay (R1)", common.COLOR_IDENTICAL_REPLAY)
plot_cdf(replay_type2_packets, "Byte-changed replay (R2–R5)", common.COLOR_BYTECHANGED_REPLAY)
plot_cdf(non_replay_packets, "Non-replay (NR1–NR2)", common.COLOR_NON_REPLAY)

ax.set(xlabel="Payload length (bytes)")
legend = ax.legend(loc="upper left", bbox_to_anchor=(0.46, 0.48), fontsize="small")
# Make legend markers fully opaque: https://stackoverflow.com/a/42403471.
for handle in legend.legendHandles:
    handle._legmarker.set_alpha(1)

fig.subplots_adjust(left=0.11, bottom=0.13, right=0.96, top=0.98)
fig.savefig(output_filename, metadata={"CreationDate": None})
