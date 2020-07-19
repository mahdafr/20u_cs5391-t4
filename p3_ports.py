import numpy as np

f_data = 'res/data.npy'
names = ['SRC', 'DST']


def build_table(data, bytes, title):
    uniq, counts = np.unique(data, return_counts=True)
    sorted = np.argsort(counts*-1)                                  # sort in descending order
    top10 = uniq[sorted[:10]]                                       # the top 10 ports
    percentage = []
    for i in top10:                                                 # accumulate the sum of each port's data flow
        percentage.append(np.sum(bytes[data==i]))
    percentage = np.array(percentage)/np.sum(bytes)
    print(f'3. {title} ports with the highest traffic volume:\t\t{top10}')
    print(f'\tOccurrences using these ports:\t\t\t\t\t{counts[sorted[:10]]}')
    print(f'\tPercentage of traffic contributed at each port:\t{np.round(percentage, decimals=4)}')


if __name__ == "__main__":
    data = np.load(f_data, allow_pickle=True)
    ports = {names[0]: data[:, 6],
             names[1]: data[:, 7],
             'byt': data[:, 1]}
    build_table(ports[names[0]], ports['byt'], names[0])
    build_table(ports[names[1]], ports['byt'], names[1])
