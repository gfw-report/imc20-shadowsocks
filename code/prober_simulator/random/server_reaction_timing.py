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

NR1 = [
    (7, 9),
    (11, 13),
    (15, 17),
    (21, 23),
    (32, 34),
    (40, 42),
    (48, 50),
]

packets = pd.read_csv(input_filename, names=colnames, delimiter=';', skiprows=0)

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

    for i, (start, end) in enumerate(NR1):
        axs[index].axvspan(start, end, color='red', alpha=0.5, label=i * "_" + "Type NR1 Probes")
        
    axs[index].legend(loc='upper center', bbox_to_anchor=(1.1, 0.9),
          ncol=1, fancybox=True, shadow=True)
    axs[index].set(xlabel='Random Probe Length (bytes)', ylabel='Connection Length (seconds)')
    axs[index].set_title('{}, {}, {}'.format(IMPLEMENTATION, VERSION, encryption_method))


plt.savefig(output_filename, metadata={"CreationDate": None}, bbox_inches='tight')
