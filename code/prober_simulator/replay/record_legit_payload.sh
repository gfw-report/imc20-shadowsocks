#!/bin/bash

set -x

sudo pkill tcpdump
sudo pkill ss-server
sudo pkill ss-local

SERVER="127.0.0.1"
SERVER_PORT="50800"
LOCAL_PORT="10800"
PASSWORD="REDUCTED"
TIMEOUT="60"
SS_SERVER_PATH="./ss-server"
SS_SERVER_PATH="$(readlink -f $SS_SERVER_PATH)"
SS_LOCAL_PATH="/usr/bin/ss-local"
SS_LOCAL_PATH="$(readlink -f $SS_LOCAL_PATH)"
FIRST_PAYLOAD_FILE="first_legit_payload.log"

function record_legit_payload {
  METHOD="$1"

  PCAP_FILE="legit_traffic_${METHOD}.pcap"
  PAYLOAD_FILE="legit_payloads_${METHOD}.log"
  SERVER_LOG_FILE="legit_server_log_${METHOD}.log"
  LOCAL_LOG_FILE="legit_client_log_${METHOD}.log"
  CURL_OUTPUT_FILE="legit_curl_output_${METHOD}.log"

  sudo tcpdump -i lo port "$SERVER_PORT" -w "$PCAP_FILE" &

  sleep 3

  "${SS_SERVER_PATH}" -v \
              -s "$SERVER"\
              -p "$SERVER_PORT"\
              -k "$PASSWORD"\
              -m "$METHOD"\
              -t "$TIMEOUT"\
              > "$SERVER_LOG_FILE" 2>&1 &

  ss_server_pid="$!"

  "${SS_LOCAL_PATH}" -v \
              -s "$SERVER"\
              -p "$SERVER_PORT"\
              -l "$LOCAL_PORT"\
              -k "$PASSWORD"\
              -m "$METHOD"\
              -t "$TIMEOUT"\
              > "$LOCAL_LOG_FILE" 2>&1 &

  ss_local_pid="$!"

  curl -x socks5h://127.0.0.1:"$LOCAL_PORT" \
    http://example.com \
    -v \
    -o "$CURL_OUTPUT_FILE"

  sleep 3

  sudo pkill tcpdump
  sudo kill -9 "$ss_server_pid"
  sudo kill -9 "$ss_local_pid"

  tshark -r "$PCAP_FILE" \
          -Y "(tcp.dstport == 50800) && (tcp.flags == 0x018)" \
          -T fields -e data \
          > "$PAYLOAD_FILE"

  ( echo -n "$(date +%s)"
    echo -n ";"
    echo -n "${METHOD}"
    echo -n ";"
    first_payload="$(head -n 1 "${PAYLOAD_FILE}")"
    [[ -z "$first_payload" ]] && echo "" || echo "$first_payload"
  ) >> "../${FIRST_PAYLOAD_FILE}"
}

METHODS=('bf-cfb' 'chacha20' 'salsa20' 'rc4-md5' \
  'aes-256-ctr' 'aes-256-cfb' 'camellia-256-cfb' 'chacha20-ietf' \
  'aes-256-gcm' 'chacha20-ietf-poly1305')

## cd into the dir of script
cd "$(dirname "$0")" || exit

LOG_DIR="log_$(date +%s)"
mkdir "$LOG_DIR"
cd "$LOG_DIR" || exit

for method in "${METHODS[@]}"; do
  echo "Method: $method"
  record_legit_payload "$method"
done
