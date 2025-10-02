#!/bin/bash

# Usage: pp.sh path/to/pcap/dir > "experiment_name.csv"

# This script Parallelly Parses pcap files in the same directory; then
# it sorts packets by the timestamps and prints to stdin.

# The script requires tshark and parallel, which can be installed by:
# Debian-based: apt install tshark parallel
# Fedora-based: dnf install tshark parallel

# Exit if no argument provided
if [ "$#" -eq 0 ]; then
    echo "Error: No argument provided." >&2
    echo "Usage: $(basename $0) path/to/pcap/dir" >&2
    exit 1
fi

parse() {
    /usr/bin/tshark -r "$1" \
		    -Y "tcp.port == 38288" \
		    -T fields \
		    -E separator=\; \
		    -o tcp.relative_sequence_numbers:FALSE \
		    -e frame.number \
		    -e frame.time_epoch \
		    -e ip.src \
		    -e ip.dst \
		    -e tcp.srcport \
		    -e tcp.dstport \
		    -e ip.ttl \
		    -e ip.id \
		    -e ip.flags.df \
		    -e tcp.options.timestamp.tsval \
		    -e tcp.seq \
		    -e tcp.flags \
		    -e tcp.stream \
		    -e tcp.len \
		    -e data
}
# Only works in Bash
export -f parse

# print column names
echo "frame.number;frame.time_epoch;ip.src;ip.dst;tcp.scrport;tcp.dstport;ip.ttl;ip.id;ip.flags.df;tcp.options.timestamp.tsval;tcp.seq;tcp.flags;tcp.stream;tcp.len;payload"

# sort on timestamp of packets
find "$1" -name "*.pcap" | parallel parse | sort -t\; -k2,2n
