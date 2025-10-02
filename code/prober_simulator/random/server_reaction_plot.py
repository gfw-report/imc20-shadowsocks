#!/usr/bin/env python3

import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 150
plt.style.use('seaborn-whitegrid')

import numpy as np
from numpy import genfromtxt
import pandas as pd
from collections import Counter
import math
import sys
import getopt

_, (input_filename, IMPLEMENTATION, VERSION, output_filename) = getopt.gnu_getopt(sys.argv[1:], "")

colnames = ['timestamp', 'encryption_method', 'probe_type', 'ip_src',
            'tcp_srcport', 'ip_dst', 'tcp_dstport', 'connection_length',
            'payload', 'payload_length', 'connection_success',
            'errno', 'err_message', 'message']

# log_1578199994_v3.0.8/prober_log_v3.0.8.log
packets = pd.read_csv(input_filename, names=colnames, delimiter=';', skiprows=0)

# IMPLEMENTATION = "Shadowsocks-libev"
# VERSION = "v3.0.8"

num_methods = len(packets.groupby(['encryption_method']))

fig, axs = plt.subplots(num_methods, 1, figsize=(10, 25), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .5, wspace=1)
axs = axs.ravel()

index = -1
for encryption_method, an_encryption_group in packets.groupby(['encryption_method']):
    index += 1

    print(encryption_method)
    
    for err_message, an_error_group in an_encryption_group.groupby(['err_message']):
        if err_message == 'No Error':
            err_message = 'Server FIN/ACK'
            color = 'g'
        if err_message == '[Errno 104] Connection reset by peer':
            err_message = 'Server RST'
            color = 'r'
        if err_message == 'timed out':
            err_message = 'Prober Timeout'
            color = 'b'
        axs[index].scatter(an_error_group['payload_length'], an_error_group['connection_length'], \
                   label="{}".format(err_message), s=3, alpha=0.7, color=color)
        axs[index].legend(loc='upper center', bbox_to_anchor=(1.1, 0.9),
          ncol=1, fancybox=True, shadow=True)
    axs[index].set(xlabel='Random Probe Length (bytes)', ylabel='Connection Length (seconds)')
    axs[index].set_title('{}, {}, {}'.format(IMPLEMENTATION, VERSION, encryption_method))
fig.savefig('server_reactions_timing_{}_{}.png'.format(IMPLEMENTATION, VERSION))

num_methods = len(packets.groupby(['encryption_method']))

fig, axs = plt.subplots(num_methods, 1, figsize=(10, 25), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .5, wspace=1)

index = -1
for encryption_method, an_encryption_group in packets.groupby(['encryption_method']):
    index += 1
    
    print(encryption_method)
    
    payload_length_list = []
    timeout_ratio_list = []
    server_fin_ack_ratio_list = []
    rst_ratio_list = []
    
    for payload_length, a_same_payload_length_group in an_encryption_group.groupby(['payload_length']):
        server_fin_ack_ratio = 0
        timeout_ratio = 0
        rst_ratio = 0
        for err_message, an_error_group in a_same_payload_length_group.groupby(['err_message']):
            if err_message == 'No Error':
                err_message = 'Server FIN/ACK'
                server_fin_ack_ratio = len(an_error_group) * 1.0 / len(a_same_payload_length_group)
            if err_message == '[Errno 104] Connection reset by peer':
                err_message = 'Server RST'
                rst_ratio = len(an_error_group) / len(a_same_payload_length_group)
            if err_message == 'timed out':
                err_message = 'Prober Timeout'
                timeout_ratio = len(an_error_group) / len(a_same_payload_length_group)
        payload_length_list.append(payload_length)
        server_fin_ack_ratio_list.append(server_fin_ack_ratio)
        rst_ratio_list.append(rst_ratio)
        timeout_ratio_list.append(timeout_ratio)

    axs[index].plot(payload_length_list, timeout_ratio_list, 'x-',
               label="{}".format("Prober Timeout"), alpha=0.7)
    axs[index].plot(payload_length_list, rst_ratio_list, 'x-',
               label="{}".format("Server RST"), alpha=0.7)
    axs[index].plot(payload_length_list, server_fin_ack_ratio_list, 'x-',
               label="{}".format("Server FIN/ACK"), alpha=0.7)
    axs[index].axhline(y =  15/ 16, c='r', label='15/16', alpha=0.7, ls='--')
    axs[index].axhline(y =  13/ 16, c='r', label='13/16', alpha=0.7, ls='--')

    axs[index].axhline(y =  2/ 16, c='purple', label='2/16', alpha=0.7, ls='--')
    axs[index].legend(loc='upper center', bbox_to_anchor=(1.1, 1.0),
              ncol=1, fancybox=True, shadow=True)
    axs[index].set(xlabel='Random Probe Length (bytes)', ylabel='Portion')
    axs[index].set_title("Portion of Server Reactions, {}, {}, {}".format(IMPLEMENTATION, VERSION, encryption_method))
fig.savefig('server_reactions_portion_{}_{}.png'.format(IMPLEMENTATION, VERSION))
