PYTHON = python3

ALL = \
	random-probe-length-distribution.pdf \
	cdf_ip_occurrences.pdf \
	cdf_source_port_lon15.pdf \
	asn_of_unique_prober_ips_all_experiment.tex \
	tsval_lon8.pdf \
	delay_of_replays_in_all_experiments.pdf \
	cdf_payload_length_exp1a.pdf \
	replayed_ratio_exp3.pdf \
	effectiveness_of_brdgrd.pdf \
	comparison_with_other_probe_source_datasets.pdf

# These are large files that are not checked into the repository.
# Various filtered and reduced versions of them, created by makefile
# rules, are checked in, instead. Marking the source filenames as
# "secondary" means that Make will not insist on the source files being
# present even though they are part of the dependency chain; the
# graph-producing scripts can use the filtered and reduced input files
# directly.
.SECONDARY: \
	cdf_ip_occurrences/probes_from_column_add_files.txt \
	cdf_ip_occurrences/prober_syn_across_all_exp.csv \
	cdf_ip_occurrences/excluded_ip_list.txt cdf_ip_occurrences/exclude_additional.txt \
	cdf_source_port_lon15/bj17_lon15_exp1_columns_added.csv \
	cdf_payload_length_exp1a/bj3-new_sfo1_ncatlike_all_columns_added.csv \
	replayed_ratio_exp3/bj6-new_sfo4_columns_added.csv \
	effectiveness_of_brdgrd/bj13_lon11_exp1_columns_added.csv

.PHONY: all
all: $(ALL)

random-probe-length-distribution.pdf: random-probe-length-distribution.py common.py random-probe-length-distribution.csv
	$(PYTHON) random-probe-length-distribution.py random-probe-length-distribution.csv "$@"

cdf_ip_occurrences.pdf: cdf_ip_occurrences.py common.py cdf_ip_occurrences/probes_from_column_add_files_filtered.txt cdf_ip_occurrences/prober_syn_across_all_exp_filtered.csv
	$(PYTHON) cdf_ip_occurrences.py "$@" cdf_ip_occurrences/probes_from_column_add_files_filtered.txt cdf_ip_occurrences/prober_syn_across_all_exp_filtered.csv
cdf_ip_occurrences/prober_syn_across_all_exp_filtered.csv: cdf_ip_occurrences/prober_syn_across_all_exp.csv cdf_ip_occurrences/excluded_ip_list.txt cdf_ip_occurrences/exclude_additional.txt
	$(PYTHON) cdf_ip_occurrences/filter-csv cdf_ip_occurrences/excluded_ip_list.txt cdf_ip_occurrences/exclude_additional.txt < cdf_ip_occurrences/prober_syn_across_all_exp.csv > "$@"
cdf_ip_occurrences/probes_from_column_add_files_filtered.txt: cdf_ip_occurrences/probes_from_column_add_files.txt cdf_ip_occurrences/excluded_ip_list.txt cdf_ip_occurrences/exclude_additional.txt
	$(PYTHON) cdf_ip_occurrences/filter-txt cdf_ip_occurrences/excluded_ip_list.txt cdf_ip_occurrences/exclude_additional.txt < cdf_ip_occurrences/probes_from_column_add_files.txt > "$@"

cdf_source_port_lon15.pdf: cdf_source_port_lon15.py common.py cdf_source_port_lon15/bj17_lon15_exp1.csv.xz
	$(PYTHON) cdf_source_port_lon15.py cdf_source_port_lon15/bj17_lon15_exp1.csv.xz "$@"
cdf_source_port_lon15/bj17_lon15_exp1.csv.xz: cdf_source_port_lon15/bj17_lon15_exp1_columns_added.csv
	$(PYTHON) cdf_source_port_lon15/filter-csv < "$<" | xz -v > "$@"

asn_of_unique_prober_ips_all_experiment.tex: asn_of_unique_prober_ips_all_experiment.py ss_prober_asn.csv
	$(PYTHON) asn_of_unique_prober_ips_all_experiment.py ss_prober_asn.csv > "$@"

tsval_lon8.pdf: tsval.py common.py probe_psh_packets_in_bj10_lon8.csv
	$(PYTHON) tsval.py probe_psh_packets_in_bj10_lon8.csv "$@"

delay_of_replays_in_all_experiments.pdf: delay_of_replays.py common.py delay_of_replays/delay_of_replays.csv
	$(PYTHON) delay_of_replays.py delay_of_replays/delay_of_replays.csv "$@"
delay_of_replays/delay_of_replays.csv: delay_of_replays/*/delay_of_first_replay.txt delay_of_replays/*/delay_of_replay.txt
	(cd delay_of_replays && ./makecsv.sh) > "$@"

cdf_payload_length_exp1a.pdf: cdf_payload_length_exp1a.py common.py cdf_payload_length_exp1a/bj3-new_sfo1_ncatlike.csv.xz
	$(PYTHON) cdf_payload_length_exp1a.py cdf_payload_length_exp1a/bj3-new_sfo1_ncatlike.csv.xz "$@"
cdf_payload_length_exp1a/bj3-new_sfo1_ncatlike.csv.xz: cdf_payload_length_exp1a/bj3-new_sfo1_ncatlike_all_columns_added.csv
	$(PYTHON) cdf_payload_length_exp1a/filter-csv < "$<" | xz -v > "$@"

replayed_ratio_exp3.pdf: replayed_ratio_exp3.py common.py replayed_ratio_exp3/bj6-new_sfo4.csv.xz
	$(PYTHON) replayed_ratio_exp3.py replayed_ratio_exp3/bj6-new_sfo4.csv.xz "$@"
replayed_ratio_exp3/bj6-new_sfo4.csv.xz: replayed_ratio_exp3/bj6-new_sfo4_columns_added.csv
	$(PYTHON) replayed_ratio_exp3/filter-csv < "$<" | xz -v > "$@"

effectiveness_of_brdgrd.pdf: effectiveness_of_brdgrd.py common.py effectiveness_of_brdgrd/bj13_lon11_exp1.csv.xz
	$(PYTHON) effectiveness_of_brdgrd.py effectiveness_of_brdgrd/bj13_lon11_exp1.csv.xz "$@"
effectiveness_of_brdgrd/bj13_lon11_exp1.csv.xz: effectiveness_of_brdgrd/bj13_lon11_exp1_columns_added.csv
	$(PYTHON) effectiveness_of_brdgrd/filter-csv < "$<" | xz -v > "$@"

comparison_with_other_probe_source_datasets.pdf: comparison_with_other_probe_source_datasets.py common.py comparison_with_other_probe_source_datasets/probers.txt comparison_with_other_probe_source_datasets/tor_active_probing_src_ips.csv comparison_with_other_probe_source_datasets/ss_active_probing_unique_ips_across_all_exps.csv
	$(PYTHON) comparison_with_other_probe_source_datasets.py comparison_with_other_probe_source_datasets/probers.txt comparison_with_other_probe_source_datasets/tor_active_probing_src_ips.csv comparison_with_other_probe_source_datasets/ss_active_probing_unique_ips_across_all_exps.csv "$@"

.PHONY: clean
clean:
	rm -f $(ALL)

.DELETE_ON_ERROR:
