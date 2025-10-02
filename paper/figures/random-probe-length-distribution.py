#!/usr/bin/env python3

import getopt
import sys

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

import common

FIGSIZE = (common.COLUMNWIDTH, 2.0)

_, (input_filename, output_filename) = getopt.gnu_getopt(sys.argv[1:], "")

data = np.loadtxt(input_filename, delimiter=",", skiprows=1)

# Because there is such a wide range in values, we split the plot horizontally.
XRANGES = ((0, 53), (219, 223))
YRANGES = ((0, 48), (0, 2400))

# Make sure the omitted parts of the plot do not contain any data.
assert all(any(xr[0] < x <= xr[1] for xr in XRANGES) for x in data[:,0])

# https://matplotlib.org/3.2.1/gallery/userdemo/demo_gridspec03.html
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(
    len(XRANGES), 2,
    width_ratios=[xr[1] - xr[0] for xr in XRANGES],
    height_ratios=(1, 5),
    wspace=0.05,
    hspace=0.05,
)
ax0 = fig.add_subplot(gs[1,0])
ax1 = fig.add_subplot(gs[:,1])

for ax in ax0, ax1:
    ax.bar(data[:,0], data[:,1], color=common.COLOR_NON_REPLAY)

ax0.set_xlim(*XRANGES[0])
ax0.set_xticks([8, 12, 16, 22, 33, 41, 49])
ax0.set_ylim(*YRANGES[0])
ax0.set_title("Type NR1")
ax0.set_xlabel("Probe length (bytes)")
ax0.set_ylabel("Count")

ax1.set_xlim(*XRANGES[1])
ax1.set_xticks([max(data[:,0])])
ax1.set_ylim(*YRANGES[1])
ax1.tick_params(left=False, labelleft=False, right=True, labelright=True)
ax1.set_title("Type NR2")

fig.subplots_adjust(left=0.11, bottom=0.16, right=0.90, top=0.90)
fig.savefig(output_filename, metadata={"CreationDate": None})
