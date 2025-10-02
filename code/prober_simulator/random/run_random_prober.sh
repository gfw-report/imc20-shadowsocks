#!/bin/bash

set -x

sudo pkill tcpdump || true
sudo pkill ss-server || true
sudo pkill ss-local || true

SERVER="127.0.0.1"
SERVER_PORT="50800"
PASSWORD="REDUCTED"
TIMEOUT="60"
SS_SERVER_PATH="../shadowsocks_implementations/v3.3.1/ss-server"
#SS_SERVER_PATH="../shadowsocks_implementations/v2.6.3/ss-server"
#SS_SERVER_PATH="../shadowsocks_implementations/v3.1.3/ss-server"
#SS_SERVER_PATH="../shadowsocks_implementations/v3.2.5/ss-server"
#SS_SERVER_PATH="../shadowsocks_implementations/v3.3.3/ss-server"
#SS_SERVER_PATH="../shadowsocks_implementations/v3.0.8/ss-server"
SS_SERVER_PATH="$(readlink -f $SS_SERVER_PATH)"
PROBER_PATH="./random_probers.py"
PROBER_PATH="$(readlink -f $PROBER_PATH)"
FIRST_PAYLOAD_FILE="../record_legit_payload/first_legit_payload.log"
FIRST_PAYLOAD_FILE="$(readlink -f $FIRST_PAYLOAD_FILE)"
PROBER_LOG_FILE="prober_log.log"

function probe_simulation {
  METHOD="$1"

  PCAP_FILE="probe_traffic_${METHOD}.pcap"

  SERVER_LOG_FILE="server_log_${METHOD}.log"

  sudo tcpdump -i lo port "$SERVER_PORT" -w "$PCAP_FILE" &

  sleep 2

  "${SS_SERVER_PATH}" -v \
              -s "$SERVER"\
              -p "$SERVER_PORT"\
              -k "$PASSWORD"\
              -m "$METHOD"\
              -t "$TIMEOUT"\
              > "$SERVER_LOG_FILE" 2>&1 &

  ss_server_pid="$!"

  python3 "${PROBER_PATH}" "${FIRST_PAYLOAD_FILE}" "$PROBER_LOG_FILE" "$METHOD"

  sleep 2

  sudo pkill tcpdump
  sudo kill -9 "$ss_server_pid"
}

## cd into the dir of script
cd "$(dirname "$0")" || exit

LOG_DIR="log_$(date +%s)"
mkdir "$LOG_DIR"
cd "$LOG_DIR" || exit

METHODS=('bf-cfb' 'chacha20' 'salsa20' 'rc4-md5' \
		  'aes-256-ctr' 'aes-256-cfb' 'camellia-256-cfb' 'chacha20-ietf' \
		  'aes-256-gcm' 'chacha20-ietf-poly1305'
 	)

for method in "${METHODS[@]}"; do
  echo "Method: $method"
  probe_simulation "$method"
done
