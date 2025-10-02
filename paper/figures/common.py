# Common code for graph plotting, for a uniform look.

import matplotlib.pyplot
import numpy

# \the\columnwidth → 241.14749pt
COLUMNWIDTH = 241.14749 / 72.27

# Returns (x, y) arrays for an empirical CDF.
def cdf(values):
    return numpy.sort(values), numpy.arange(len(values)) / float(len(values)-1)

# Set default plot style.
matplotlib.pyplot.style.use("seaborn-whitegrid")
matplotlib.pyplot.rcParams.update({"font.size": 8})
matplotlib.pyplot.rcParams.update({"font.family": "serif"})
matplotlib.pyplot.rcParams.update({"font.serif": ["Linux Libertine O"]})
matplotlib.pyplot.rcParams.update({"legend.frameon": True})
matplotlib.pyplot.rcParams.update({"legend.framealpha": 0.8})
matplotlib.pyplot.rcParams.update({"legend.fancybox": False})
matplotlib.pyplot.rcParams.update({"legend.frameon": True})
matplotlib.pyplot.rcParams.update({"mathtext.default": "regular"})

# Colors that should be consistent across graphs.
# From http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/#a-colorblind-friendly-palette
# with an adjusted blue.
COLOR_LEGIT = "#999999"
COLOR_IDENTICAL_REPLAY = "#e69f00"
COLOR_BYTECHANGED_REPLAY = "#0072b2"
COLOR_NON_REPLAY = "dodgerblue"
