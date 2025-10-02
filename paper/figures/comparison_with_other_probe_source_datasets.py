#!/usr/bin/env python3

# Usage: comparison_with_other_probe_source_datasets.py a.csv b.csv c.csv comparison_with_other_probe_source_datasets.pdf

import getopt
import sys

import matplotlib.pyplot as plt
import matplotlib
from matplotlib_venn import venn3, venn3_unweighted

import common

FIGSIZE = (common.COLUMNWIDTH, 2.0)

# Read packets from CSV.
_, (dunna_ips, ensafi_ips, ss_ips, output_filename) = getopt.gnu_getopt(sys.argv[1:], "")

# source: https://adunna.me/projects/dist/foci-2018-tor/Data/analysis-only-SYN.csv
tor_active_probing_src_ips = [line.rstrip() for line in open(dunna_ips).readlines()]

# source: https://ensa.fi/active-probing/#code
probers_active_probing_src_ips = [line.rstrip() for line in open(ensafi_ips).readlines()]

ss_active_probing_src_ips = [line.rstrip() for line in open(ss_ips).readlines()]

fig = plt.figure(figsize=FIGSIZE)
ax = plt.axes()
ax.margins(0, 0)

venn3([set(ss_active_probing_src_ips), \
                  set(tor_active_probing_src_ips), \
                  set(probers_active_probing_src_ips)], \
      set_labels = ('', '', '')
)

#       set_labels = ('Shadowsocks dataset', \
                    # 'Active probing dataset by Ensafi et al.')

ax.text(
        -0.2, 0.05,
        "Tor active probes \n (Dunna et al.)",
        transform=matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes),
        horizontalalignment="center", verticalalignment="center",
    )

ax.text(
        -0.7, 0.85,
        "Shadowsocks active probes",
        transform=matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes),
        horizontalalignment="center", verticalalignment="center",
    )

ax.text(
        0.8, 0.9,
        "Active probes \n (Ensafi et al.)",
        transform=matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes),
        horizontalalignment="center", verticalalignment="center",
    )


# legend = ax.legend(bbox_to_anchor=(0.62, 0.72), fontsize="small")
# # Make legend markers fully opaque: https://stackoverflow.com/a/42403471.
# for handle in legend.legendHandles:
#     handle._legmarker.set_alpha(1)

#fig.subplots_adjust(left=0.25, bottom=0.08, right=0.9, top=0.96)
plt.savefig(output_filename, metadata={"CreationDate": None})

