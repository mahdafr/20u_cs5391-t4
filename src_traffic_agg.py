import numpy as np, math

f_data = 'res/data.npy'


def get_top(ip_addr, bites, tot_bites, mask, with_mask=False):
    if with_mask:                                                   # if want to check only those whose mask_len > 0
        ip_addr, bites = get_masks(mask, ip_addr, bites, tot_bites)

    uniq, counts = np.unique(ip_addr, return_counts=True)           # a list of every s_ip addr that appears
    size = []
    for ip in uniq:
        b = np.where(ip_addr == ip)[0]                              # get all occurrences of each s_ip addr
        size.append(np.sum(bites[b]))                               # sum up each s_ip addr's byte flow
    size = np.array(size)
    srtd = np.argsort(counts*-1)                                    # by most popular
    return uniq[srtd], size[srtd]


def prev_overflow(a, factor=1024):                                  # to prevent overflow, divide by a factor
    return a/factor


def get_top_percent(data, bites, percent, max_ip, tot_bites):
    j = 0
    sum = 0
    while j <= max_ip:                                              # accumulate the byte flow up to this ip addr
        sum += bites[j]
        j += 1
    print(f'4. Top {percent}% of SRC IP Prefixes used:\n\t{sum:.4} KB, from addresses:\t{data[:max_ip]}')
    print(f'\tThis used up only {sum/tot_bites:.2}% of the total bytes in the dataset.')


def get_masks(mask, ip_addr, bites, tot_bites, m=0):
    rep = np.where(mask == m)[0]                                   # get all occurrences where s_mask==0
    mask0 = np.sum(bites[rep])
    print(f'There are {mask0:.2} KB whose mask length is 0. This is {mask0/tot_bites:.2}% of the total bytes.')

    keep = np.where(mask != m)[0]                                  # get all occurrences where s_mask>0
    return ip_addr[keep], bites[keep]


if __name__ == '__main__':
    dataset = np.load(f_data, allow_pickle=True)
    data = {'bytes': dataset[:, 1],
            's_mask': dataset[:, 9],
            'd_mask': dataset[:, 10],
            's_as': dataset[:, 11],
            'd_as': dataset[:, 12]}

    bites = prev_overflow(data['bytes'])                            # total bytes exchanged in this dataset
    tot_bites = np.sum(bites)
    mask = data['s_mask']
    s_ip, s_b = get_top(data['s_as'], bites, tot_bites, mask, with_mask=True)

    for percent in [0.1, 1, 10]:
        max_ip = math.floor((percent/100)*s_ip.shape[0])            # up to what index is the top X% of IP addr?
        get_top_percent(s_ip, s_b, percent, max_ip, tot_bites)
