import numpy as np

f_data = 'res/data.npy'
ip = '128.112.'                                                     # using 16 of the 32 bits, so this is from Org-A

if __name__ == '__main__':
    dataset = np.load(f_data, allow_pickle=True)
    data = {'src': dataset[:, 4].astype(str),
            'dst': dataset[:, 5].astype(str),
            'byt': dataset[:, 1]/1048576,                           # represent data in megabytes (1024^2)
            'pkt': dataset[:, 0]}

    s_occ = np.where(np.char.find(data['src'], ip) == 0)[0]         # find all those whose SRC IP start with 128.112
    d_occ = np.where(np.char.find(data['dst'], ip) == 0)[0]         # find all those whose DST IP start with 128.112

    bites = data['byt']
    tot = np.sum(bites)                                             # total byte flow in trace
    s_traff = np.sum(bites[s_occ])                                  # source and destination byte flow
    d_traff = np.sum(bites[d_occ])
    traff = s_traff + d_traff

    pkts = data['pkt']
    tot_p = np.sum(pkts)                                            # total packets in trace
    s_traff_p = np.sum(pkts[s_occ])                                 # source and destination packet flow
    d_traff_p = np.sum(pkts[d_occ])
    traff_p = s_traff_p + d_traff_p

    print(f'5. IP address {ip} is found {s_occ.shape[0]} times as a SRC and {d_occ.shape[0]} times as a DST address.')
    print(f'\tThere were {s_traff:.3} MB (or {s_traff_p} packets) sent from this organization.')
    print(f'\tThere were {d_traff:.3} MB (or {d_traff_p} packets) sent to this organization.')
    print(f'\tThere were {traff:.3} total MB (or {traff_p} packets) sent to/from this IP address.')
    print(f'\tThis makes up {traff/tot:.3}% of the bytes and {traff_p/tot_p:.3}% of the packets.')
