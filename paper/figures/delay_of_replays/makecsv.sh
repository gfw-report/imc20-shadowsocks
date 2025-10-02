#!/bin/bash

# This script converts */delay_of_first_replay.txt and */delay_of_replay.* files
# into CSV format. Each delay_of_first_replay.txt file is a subset of the
# corresponding delay_of_replay.txt file. This script outputs a row with
# is_first=="T" for each line that is common to both files, and is_first=="F"
# for each line that appears only in delay_of_replay.txt. The "delay" column is
# in seconds.
#
# It would be better to instead have a CSV where each row represents a probe,
# with a probe_id column that indicates which probes are all replays of the same
# legitimate probe. That way, the "first" probes could be extracted as the
# minimum value in each probe group. However, the logic that does this
# extraction is currently distributed across the notebooks for each experiment,
# which are what actually produce the delay_of_first_replay.txt and
# delay_of_replay.txt files. The format of this CSV file is a compromise towards
# possibly consolidating that logic and outputting CSV with probe groups
# directly.

EXPS="bj10_lon8_exp1 bj14_lon12_ncat bj16_lon14_cfb bj17_lon15_gcm sfo1_nc sfo2_entropy_low sfo3_entropy_len_varied sfo4_entropy_len_even umass_outline"

echo 'experiment,is_first,delay'
for exp in $EXPS; do
	# Lines common to both files (first).
	comm -12 <(sort "$exp"/delay_of_first_replay.txt) <(sort "$exp"/delay_of_replay.txt) \
		| awk "{printf \"%s,T,%.12f\\n\", \"$exp\", \$0 * 3600}"
	# Lines present only in the second file (replays after the first).
	comm -13 <(sort "$exp"/delay_of_first_replay.txt) <(sort "$exp"/delay_of_replay.txt) \
		| awk "{printf \"%s,F,%.12f\\n\", \"$exp\", \$0 * 3600}"
	# There should be no lines that appear only in the first file.
	if test -n "$(comm -23 <(sort "$exp"/delay_of_first_replay.txt) <(sort "$exp"/delay_of_replay.txt))"; then
		echo "unexpected unique line in $exp/delay_of_first_replay.txt" 1>&2
		exit 1
	fi
done
