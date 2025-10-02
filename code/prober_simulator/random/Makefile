PYTHON = python3

ALL =	server_reactions_portion_Shadowsocks-libev_v2.6.3.png \
	server_reactions_portion_Shadowsocks-libev_v3.0.8.png \
	server_reactions_portion_Shadowsocks-libev_v3.1.3.png \
	server_reactions_portion_Shadowsocks-libev_v3.2.5.png \
	server_reactions_portion_Shadowsocks-libev_v3.3.1.png \
	server_reactions_portion_Shadowsocks-libev_v3.3.3.png \
	server_reactions_timing_Shadowsocks-libev_v2.6.3.png \
	server_reactions_timing_Shadowsocks-libev_v3.0.8.png \
	server_reactions_timing_Shadowsocks-libev_v3.1.3.png \
	server_reactions_timing_Shadowsocks-libev_v3.2.5.png \
	server_reactions_timing_Shadowsocks-libev_v3.3.1.png \
	server_reactions_timing_Shadowsocks-libev_v3.3.3.png

.PHONY: all
all: $(ALL)

server_reactions_portion_Shadowsocks-libev_v2.6.3.png: server_reaction_portion.py log_1578327998_v2.6.3/prober_log_v2.6.3.log
	$(PYTHON) server_reaction_portion.py log_1578327998_v2.6.3/prober_log_v2.6.3.log Shadowsocks-libev v2.6.3 "$@"

server_reactions_portion_Shadowsocks-libev_v3.0.8.png: server_reaction_portion.py log_1578199994_v3.0.8/prober_log_v3.0.8.log
	$(PYTHON) server_reaction_portion.py log_1578199994_v3.0.8/prober_log_v3.0.8.log Shadowsocks-libev v3.0.8 "$@"

server_reactions_portion_Shadowsocks-libev_v3.1.3.png: server_reaction_portion.py log_1578321177_v3.1.3/prober_log_v3.1.3.log
	$(PYTHON) server_reaction_portion.py log_1578321177_v3.1.3/prober_log_v3.1.3.log Shadowsocks-libev v3.1.3 "$@"

server_reactions_portion_Shadowsocks-libev_v3.2.5.png: server_reaction_portion.py log_1578270834_v3.2.5/prober_log_v3.2.5.log
	$(PYTHON) server_reaction_portion.py log_1578270834_v3.2.5/prober_log_v3.2.5.log Shadowsocks-libev v3.2.5 "$@"

server_reactions_portion_Shadowsocks-libev_v3.3.1.png: server_reaction_portion.py log_1578360326_v3.3.1/prober_log_v3.3.1.log
	$(PYTHON) server_reaction_portion.py log_1578360326_v3.3.1/prober_log_v3.3.1.log Shadowsocks-libev v3.2.1 "$@"

server_reactions_portion_Shadowsocks-libev_v3.3.3.png: server_reaction_portion.py log_1578266082_v3.3.3/prober_log_v3.3.3.log
	$(PYTHON) server_reaction_portion.py log_1578266082_v3.3.3/prober_log_v3.3.3.log Shadowsocks-libev v3.3.3 "$@"


server_reactions_timing_Shadowsocks-libev_v2.6.3.png: server_reaction_timing.py log_1578327998_v2.6.3/prober_log_v2.6.3.log
	$(PYTHON) server_reaction_timing.py log_1578327998_v2.6.3/prober_log_v2.6.3.log Shadowsocks-libev v2.6.3 "$@"

server_reactions_timing_Shadowsocks-libev_v3.0.8.png: server_reaction_timing.py log_1578199994_v3.0.8/prober_log_v3.0.8.log
	$(PYTHON) server_reaction_timing.py log_1578199994_v3.0.8/prober_log_v3.0.8.log Shadowsocks-libev v3.0.8 "$@"

server_reactions_timing_Shadowsocks-libev_v3.1.3.png: server_reaction_timing.py log_1578321177_v3.1.3/prober_log_v3.1.3.log
	$(PYTHON) server_reaction_timing.py log_1578321177_v3.1.3/prober_log_v3.1.3.log Shadowsocks-libev v3.1.3 "$@"

server_reactions_timing_Shadowsocks-libev_v3.2.5.png: server_reaction_timing.py log_1578270834_v3.2.5/prober_log_v3.2.5.log
	$(PYTHON) server_reaction_timing.py log_1578270834_v3.2.5/prober_log_v3.2.5.log Shadowsocks-libev v3.2.5 "$@"

server_reactions_timing_Shadowsocks-libev_v3.3.1.png: server_reaction_timing.py log_1578360326_v3.3.1/prober_log_v3.3.1.log
	$(PYTHON) server_reaction_timing.py log_1578360326_v3.3.1/prober_log_v3.3.1.log Shadowsocks-libev v3.2.1 "$@"

server_reactions_timing_Shadowsocks-libev_v3.3.3.png: server_reaction_timing.py log_1578266082_v3.3.3/prober_log_v3.3.3.log
	$(PYTHON) server_reaction_timing.py log_1578266082_v3.3.3/prober_log_v3.3.3.log Shadowsocks-libev v3.3.3 "$@"

.PHONY: clean
clean:
	rm -f $(ALL)

.DELETE_ON_ERROR:
