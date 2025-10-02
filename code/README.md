# README

## pp.sh

This script parallelly parses pcap files in the same directory; then
it sorts packets by the timestamps and prints to stdin.

Example usage:

```sh
pp.sh path/to/pcap/dir > "experiment_name.csv"
```

The script requires `tshark` and `parallel`:

```sh
apt install tshark parallel # Debian-based
dnf install tshark parallel # Fedora-based
```

## triggering_client_server

`./triggering_client_server` includes the source code of the clients and sink/responding servers used in Section 4.1.

## prober_simulator

`./prober_simulator` includes the source code of the prober simulators introduced in Section 5.1. It can simulate both random and replay-based probes. One can use it to check if other Shadowsocks implementations (or other circumvention tools) have similar vulnerabilities introduced in the paper.
