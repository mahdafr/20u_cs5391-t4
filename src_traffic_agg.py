import numpy as np

f_data = 'res/data.npy'

if __name__ == '__main__':
    dataset = np.load(f_data, allow_pickle=True)
    data = {'bytes': dataset[:, 1],
            's_mask': dataset[:, 9],
            'd_mask': dataset[:, 10],
            's_as': dataset[:, 11],
            'd_as': dataset[:, 12]}

    # need to get top 1% of s_ip of most trafficked bytes
    s_ip = data['s_as']
    uniq, pos, counts = np.unique(s_ip, return_index=True, return_counts=True)
    srtd = np.argsort(counts*-1)
    top10 = uniq[srtd[:10]]                                         # top 10 s_ip prefixes
    bites = data['bytes']

    print(f'Top 10 SRC IP Prefixes:\t\t\t\t{top10}')
    print(f'Total bytes used by these prefixes:\t{top10}')
