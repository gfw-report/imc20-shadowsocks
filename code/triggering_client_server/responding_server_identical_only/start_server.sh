#!/bin/bash

sudo -v

hostname="bj5_to_sfo3"

# Server's port and client's IP address are reducted
SERVER_PORT="PORT"
CLIENT_IP="IP"

# Capture all traffic in every hour
tcpdump not port 22 -w "$(hostname)-%m-%d-%H-%M.pcap" -G 3600 &

./server_fake_simple 0.0.0.0:"$SERVER_PORT" "$CLIENT_IP"   | tee -a output.txt
