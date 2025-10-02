#!/bin/bash

set -x

# IP and port are reducted
SERVER_IP_PORT="SERVER:PORT"

./client_fake_adjustable "$SERVER_IP_PORT" | tee -a output_client.txt
