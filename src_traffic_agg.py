import numpy as np

f_data = 'res/data.npy'

if __name__ == '__main__':
    dataset = np.load(f_data, allow_pickle=True)
    data = {'bytes': dataset[:, 1],
            's_mask': dataset[:, 9],
            'd_mask': dataset[:, 10],
            's_as': dataset[:, 11],
            'd_as': dataset[:, 12]}

    b = data['bytes']
    uniq, pos, counts = np.unique(b, return_index=True, return_counts=True)
    sorted = np.argsort(counts*-1)                                  # sort in descending order
    top10 = pos[sorted[:10]]                                        # the top 10 ports

    # need to get top 1% of s_ip of most trafficked bytes

    print(f'Top 10 SRC IP Prefixes: {b[top10]}')
