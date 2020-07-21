import matplotlib.pyplot as plt, numpy as np

f_data = 'res/data.npy'


def plot(data, x, out, log, y='Probability'):
    plt.hist(data, bins=15, density=True, histtype='step', cumulative=-1, log=log)
    _save(x, y, out)


def _save(x, y, out):
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title('CCDF')
    plt.savefig(out)                                                # to file
    plt.show()


if __name__ == '__main__':
    data = np.load(f_data, allow_pickle=True)
    names = {'duration': data[:, 3]-data[:, 2],                     # finish - start
             'n_byte': data[:, 1]/1024,                             # in kilobytes
             'n_pkts': data[:, 0]}

    # linear graphs
    lin_out = ['res/p2-linear/p_duration', 'res/p2-linear/p_bytes', 'res/p2-linear/p_pkts', 'res/p2-linear/all']
    plot(names['duration'], 'Duration (ms)', lin_out[0], False)
    plot(names['n_byte'], 'Flow Size (KB)', lin_out[1], False)
    plot(names['n_pkts'], 'Flow Size (number of packets)', lin_out[2], False)

    # logarithmic graphs
    lin_out = ['res/p2-logarithmic/p_duration', 'res/p2-logarithmic/p_bytes', 'res/p2-logarithmic/p_pkts', 'res/p2-logarithmic/all']
    plot(names['duration'], 'Duration (ms)', lin_out[0], True)
    plot(names['n_byte'], 'Flow Size (KB)', lin_out[1], True)
    plot(names['n_pkts'], 'Flow Size (number of packets)', lin_out[2], True)
