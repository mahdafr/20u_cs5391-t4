import matplotlib.pyplot as plt, numpy as np

f_data = 'res/data.npy'


def plot(data, linecolor, x, out, y='Probability'):
    plt.plot(data, linecolor, linewidth=0.75)                       # plot on separate graphs
    _save(x, y, out)


def plot_all(data, linecolor, out, x='X', y='Probability'):
    for g in range(len(data)):
        plt.plot(data[g], linecolor[g], linewidth=0.75)             # plot on a combined graph
    _save(x, y, out)


def _save(x, y, out):
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title('CDF')
    plt.savefig(out)                                                # to file
    plt.show()


if __name__ == '__main__':
    data = np.load(f_data, allow_pickle=True)
    names = {'duration': data[:,3]-data[:,2],                       # finish - start
             'n_byte': data[:,1],
             'n_pkts': data[:,0]}
    color = ['--r', '--g', '--b']

    # linear graphs
    lin_out = ['res/p2-linear/p_duration', 'res/p2-linear/p_bytes', 'res/p2-linear/p_pkts', 'res/p2-linear/all']
    p_duration = np.cumsum(names['duration'])/np.sum(names['duration'])
    plot(p_duration, color[0], 'Duration (ms)', lin_out[0])
    p_bytes = np.cumsum(names['n_byte'])/np.sum(names['n_byte'])    # flow size: number of bytes (doctets)
    plot(p_bytes, color[1], 'Flow Size (bytes)', lin_out[1])
    p_pkts = np.cumsum(names['n_pkts'])/np.sum(names['n_pkts'])     # flow size: number of packets (dpkts)
    plot(p_pkts, color[2], 'Flow Size (number of packets)', lin_out[2])
    plot_all([p_duration, p_bytes, p_pkts], color, lin_out[3])

    # logarithmic graphs
    log_out = ['res/p2-logarithmic/p_duration', 'res/p2-logarithmic/p_bytes', 'res/p2-logarithmic/p_pkts', 'res/p2-logarithmic/all']
    n_dur = np.log(names['duration'].astype(np.float))              # duration
    p_duration = np.cumsum(n_dur)/np.sum(n_dur)
    plot(p_duration, color[0], 'Duration (ms)', log_out[0])
    n_bytes = np.log(names['n_byte'].astype(np.float))
    p_bytes = np.cumsum(n_bytes)/np.sum(n_bytes)                    # flow size: number of bytes (doctets)
    plot(p_bytes, color[0], 'Flow Size (bytes)', log_out[1])
    n_pkts = np.log(names['n_pkts'].astype(np.float))
    p_pkts = np.cumsum(n_pkts)/np.sum(n_pkts)                       # flow size: number of packets (dpkts)
    plot(p_pkts, color[0], 'Flow Size (number of packets)', log_out[2])
    plot_all([p_duration, p_bytes, p_pkts], color, log_out[3])
