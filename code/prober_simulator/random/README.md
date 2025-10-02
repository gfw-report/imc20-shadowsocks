# Descriptions

This directory contains the data and code to reproduce the figures related to server reactions. Specifically:

* Run `run_random_prober.sh` will:

1. start a specified Shadowsocks binary;
2. run the `random_prober.py` to probe the specified binary.

The result will be in a directory like `log_${epochtime}_v*`.

* The all figures can be generated with `make` once the log files are available.
