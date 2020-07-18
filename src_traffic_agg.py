import numpy as np

f_data = 'res/data.npy'


def get_top(ip_addr, bites):
    uniq = np.unique(ip_addr)                                       # a list of every s_ip addr that appears
    size = []
    for ip in uniq:
        b = np.where(ip_addr == ip)[0]                              # get all occurrences of each s_ip addr
        size.append(np.sum(bites[b]))                               # sum up each s_ip addr's byte flow
    size = np.array(size)
    srtd = np.argsort(size*-1)
    return uniq[srtd], size[srtd]


def get_top_percent(data, bites, percent, tot_bites):
    j = 0
    sum = 0
    print('want', tot_bites*percent)
    while sum <= tot_bites*percent:                       # accumulate the byte flow up to this percent
        sum += bites[j]
        j += 1                                            # move to next unique s_ip addr
        print('sum', sum, j)
    print(f'Top {percent}% of SRC IP Prefixes used:\t{sum} bytes, from addresses:\t{data[:j-1]}')
    print(f'This used up only {sum/tot_bites:.2}% of the total bytes in the dataset.')


if __name__ == '__main__':
    dataset = np.load(f_data, allow_pickle=True)
    data = {'bytes': dataset[:, 1],
            's_mask': dataset[:, 9],
            'd_mask': dataset[:, 10],
            's_as': dataset[:, 11],
            'd_as': dataset[:, 12]}

    bites = data['bytes']                                           # total bytes exchanged in this dataset
    tot_bites = np.sum(bites)

    s_ip, s_bytes = get_top(data['s_as'], bites)                    # list of src IPs and their byte size
    for percent in [0.1, 1, 10]:
        get_top_percent(s_ip, s_bytes, percent, tot_bites)          # 0.1%, 1%, 10%
