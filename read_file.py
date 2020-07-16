import pandas as pd, numpy as np
from os import path


dataset = 'res/flow.2001-09-29.csv'
cols = [4, 5, 6, 7, 10, 11, 15, 16, 17, 20, 21, 22, 23]             # the important columns to use
dict = {'unix_secs': int,                                           # the dtype of each column
        'unix_nsecs': int,
        'sysuptime': int,
        'exaddr': str,
        'dpkts': int,
        'doctets': int,
        'first': int,
        'last': int,
        'engine_type': int,
        'engine_id': int,
        'srcaddr': str,
        'dstaddr': str,
        'nexthop': str,
        'input': int,
        'output': int,
        'srcport': int,
        'dstport': int,
        'prot': int,
        'tos': int,
        'tcp_flags': int,
        'src_mask': int,
        'dst_mask': int,
        'src_as': int,
        'dst_as': int}
out = 'res/data.npy'


def read_data():                                                    # using the pandas library
    data = pd.read_csv(dataset, delimiter=',', usecols=cols, converters=dict)
    return data.to_numpy()                                          # header is already removed from `read_csv`


if __name__ == '__main__':
    if not path.exists(out):
        data = read_data()                                          # on first read
        np.save(out, data)
    else:                                                           # every other time
        data = np.load(out, allow_pickle=True)
    print(f'1. The average packet size in this dataset is {np.sum(data[:,1])/np.sum(data[:,0]):.2f}')
