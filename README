## Explanations on datasets

This open dataset contains code and datasets for the IMC 2020 paper: [How China Detects and Blocks Shadowsocks](https://gfw.report/publications/imc20/en/).

We introduce the major components of the dataset below.

### Paper

The [`paper`](./paper) directory includes:

1. the CSVs of probe metadata, along with the code that generates CSVs from PCAPs
2. the source code, including Makefile, that reproduces all figures (except Figure 1 and 10) in the paper
3. the source code of latex

### pp.sh

[`code/pp.sh`](./code/pp.sh) Parallelly Parses all pcap files in a specified directory;
then it sorts packets by the timestamps and prints to stdin.

Example usage:

```sh
pp.sh path/to/pcap/dir > experiment_name.csv
````

The script requires `tshark` and `parallel`:

```sh
apt install tshark parallel   # Debian-based
dnf install tshark parallel   # Fedora-based
```

### triggering_client_server

[`code/triggering_client_server`](./code/triggering_client_server) includes the source code of the clients and sink/responding servers used in [Section 4.1](./paper/shadowsocks.pdf#page=6).

### Prober simulator

[`code/prober_simulator`](../data/code/prober_simulator) includes the source code of the prober simulators introduced in [Section 5.1](../data/paper/shadowsocks.pdf#page=8).
It can simulate both random and replay-based probes.
One can use it to check if other Shadowsocks implementations (or other circumvention tools) have similar vulnerabilities introduced in the paper.

## Updates

* As of October 7, 2020, we have released our code and datasets to the maximum extend that does not harm our anonymity. These code and datasets support all major findings in our paper.
