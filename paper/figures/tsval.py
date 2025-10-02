#!/usr/bin/env python3

# Usage: tsval.py probe_psh_packets_in_bj10_lon8.csv tsval_lon8.pdf

import getopt
import sys

import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import common

FIGSIZE = (common.COLUMNWIDTH, 2.0)

# Read packets from CSV.
_, (csv_filename, output_filename) = getopt.gnu_getopt(sys.argv[1:], "")
packets = pd.read_csv(csv_filename)
# Convert epoch time to date.
packets["date"] = pd.to_datetime(packets.frame_epoch_time, unit="s")

# Extract the subsets of packets we want to plot.
active_probing_psh = packets[(packets.tcp_flags == 0x18) & (packets.is_legit == False)]
replay_type1_packets = active_probing_psh[active_probing_psh.payload_type == 1]
replay_type2_packets = active_probing_psh[active_probing_psh.payload_type == 2]
non_replay_packets = active_probing_psh[active_probing_psh.payload_type == 3]

fig = plt.figure(figsize=FIGSIZE)
ax = plt.axes()
ax.margins(0, 0)
ax.xaxis.set_major_locator(matplotlib.dates.WeekdayLocator(matplotlib.dates.SU))
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %d"))
# TSval is an unsigned 32-bit integer.
ax.set_ylabel("TCP TSval")
ax.set_ylim(0, 2**32)
plt.yticks([0, 2**31, 2**32], ("$0$", "$2^{31}$", "$2^{32}$"))

# Return the y such that (x, y) lines on the line between (x, y) and (x0, y0)
# has slope m.
def point_on_point_slope_line(x0, y0, m, x):
    return y0 - m * (x0 - x).total_seconds()

# Return the (yl, yr) that will make the line segment between (xl, yl) and
# (xr, yr) have slope m and pass through the point (x0, y0).
def point_slope_segment_endpoints(x0, y0, m, xl, xr):
    yl = point_on_point_slope_line(x0, y0, m, xl)
    yr = point_on_point_slope_line(x0, y0, m, xr)
    return (yl, yr)

# Plot a line between the bounds xl and xr that has slope m and passes through
# the point (x0, y0), and let it wrap vertically in [ymin, ymax).
def plot_line_point_slope_wrapping(x0, y0, m, xl, xr, ymin, ymax):
    # Move upward, and keep plotting lines until they are no longer visible.
    y = y0
    while True:
        yl, yr = point_slope_segment_endpoints(x0, y, m, xl, xr)
        if (yl < ymin and yr < ymin) or (yl > ymax and yr > ymax):
            break
        ax.plot((xl, xr), (yl, yr), linewidth=0.8, color="gray")
        y += ymax - ymin
    # Move downward, and keep plotting lines until they are no longer visible.
    y = y0 - (ymax - ymin)
    while True:
        yl, yr = point_slope_segment_endpoints(x0, y, m, xl, xr)
        if (yl < ymin and yr < ymin) or (yl > ymax and yr > ymax):
            break
        ax.plot((xl, xr), (yl, yr), linewidth=0.8, color="gray")
        y -= ymax - ymin

# Select an arbitrary point whose frame_relative_time is between min_time and
# max_time, and whose tcp_tsval is between min_tsval and max_tsval.
def select_point_in_rect(points, min_time, max_time, min_tsval, max_tsval):
    points = points[(min_time <= points.frame_relative_time) & (points.frame_relative_time < max_time)]
    points = points[(min_tsval <= points.tcp_tsval) & (points.tcp_tsval < max_tsval)]
    return (points.date.iloc[0], points.tcp_tsval.iloc[0])

# Plot constant-slope lines, chosen to go through selected groups of points. For
# each group we define a rough rectangle of frame_relative_time and tcp_tsval,
# then pick a point within it.
xl = min(active_probing_psh.date)
xr = max(active_probing_psh.date)
for slope, min_time, max_time, min_tsval, max_tsval, draw_label in (
    (250, 0, 360000, 4.1e9, 2**32,  False),
    (250, 0, 360000, 3.8e9, 4.1e9,  False),
    (250, 0, 360000, 1.8e9, 2.0e9,  True),
    (250, 0, 360000, 1.6e9, 1.8e9,  False),
    (250, 0, 360000, 1.4e9, 1.55e9, False),
    (250, 0, 360000, 0.7e9, 0.8e9,  False),
    (1000, 1500000, 1800000, 3.0e9, 3.5e9, True),
):
    x, y = select_point_in_rect(active_probing_psh, min_time, max_time, min_tsval, max_tsval)
    plot_line_point_slope_wrapping(x, y, slope, xl, xr, 0, 2**32)
    if draw_label:
        xt = pd.to_datetime("2019-11-13 00:00:00")
        yt = point_on_point_slope_line(x, y, slope, xt)
        # https://matplotlib.org/3.1.0/gallery/text_labels_and_annotations/text_rotation_relative_to_line.html
        # matplotlib.dates.date2num numbers are in units of days, so multiply
        # the slope in Hz by the number of seconds in a day.
        angle = np.rad2deg(np.arctan(86400*slope))
        trans_angle = ax.transData.transform_angles(np.array((angle,)), np.array(((matplotlib.dates.date2num(xt), yt),)), pushoff=10)[0]
        ax.annotate(
            f"{slope} Hz", xy=(xt, yt), color="gray",
            rotation=trans_angle, rotation_mode="anchor",
            horizontalalignment="left", verticalalignment="bottom",
        )

# Plot the active probes.
ax.plot(replay_type1_packets.date, replay_type1_packets.tcp_tsval, "x", markersize=4, label="Identical replay (R1)", color=common.COLOR_IDENTICAL_REPLAY, alpha=0.5)
ax.plot(replay_type2_packets.date, replay_type2_packets.tcp_tsval, "+", markersize=4, label="Byte-changed replay (R2–R5)", color=common.COLOR_BYTECHANGED_REPLAY, alpha=0.5)
ax.plot(non_replay_packets.date, non_replay_packets.tcp_tsval, ".", markersize=4, label="Non-replay (NR1–NR2)", color=common.COLOR_NON_REPLAY, alpha=0.5)

legend = ax.legend(bbox_to_anchor=(0.59, 0.72), fontsize="small")
# Make legend markers fully opaque: https://stackoverflow.com/a/42403471.
for handle in legend.legendHandles:
    handle._legmarker.set_alpha(1)

fig.subplots_adjust(left=0.12, bottom=0.08, right=0.99, top=0.96)
plt.savefig(output_filename, metadata={"CreationDate": None})
