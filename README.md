# Assignment #4

In this task, you will analyze publicly-available measurement data to understand important properties of the Internet.
You may want to choose any tool for plotting graphs (e.g., Matlab, gnuplot, Excel, R), and have some reusable code for generating a probability distribution plot from a list of numbers (using either linear or logarithmic scales).

## Traffic Measurement
Many networks collect Netflow measurements directly from the routers.
In this part of the assignment, you'll analyze a five-minute trace of Netflow records captured from a router in the Internet2 backbone that connects the major research universities in the United States.
Note that the Netflow data from Internet2 anonymizes the last 11 bits of the source and destination IP addresses, to protect user privacy.
The records have been parsed into CSV (comma-separated variable) format, with the names of the fields listed in the first row of the file.
Internet2 collects Netflow measurements with 1/100 packet sampling, so the data reflects 1% of the traffic at the router.

The Netflow measurement dataset was downloaded is not available in this project.
The data was saved as a `npy` file.
This file can be found in the `res/` directory of this project.

The important fields in the Netflow data are:
- _dpkts_ and _doctets_ (the number of packets and bytes in the flow, respectively),
- _first_ and _last_ (the timestamps of the first and last packets in the flow, respectively),
- _srcaddr_ and _dstaddr_ (the source and destination IP addresses, respectively),
- _srcport_ and _dstport_ (the source and destination transport port numbers, respectively),
- _prot_ (the transport protocol, e.g., TCP, UDP),
- _src_mask_ and _dst_mask_ (the length of the longest matching IP prefix for the source and destination IP addresses, respectively), and
- _src_as_ and _dst_as_ (the AS that originated the IP prefixes matching the source and destination IP addresses, respectively)

### Results
- The `read_file.read_data()` method is used to read the CSV file into a NumPy array
    - The [pandas library](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) has the useful `read_csv` method which can customize the CSV file into a DataFrame object. The following fields were used and customized:
        - `filepath_or_buffer`, which is the string to the path,
        - `delimiter`, which is the character representation of the cell-separator (a `'`),
        - `usecols`, which is a list of the columns to keep (see above),
        - `converters`, which is a dictionary of what dtype is each column
    - The DataFrame was then converted to a NumPy array using the `to_numpy()` method of the [pandas library](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_numpy.html)

## Now using the dataset, answer the following questions.
1. What is the average packet size, across all traffic in the trace? Describe how you computed this number.
    - The `p1_read_file.py` script calculates this result as reported below.
    - The average packet size can be calculated by the dividing the total amount of bytes (`sum(data[:][1])`) for all packets (or, the sum of `data`'s column 2) by the total number of packets (`sum(data[:][0])`) in the trace.
    - This value was calculated to be `768.18` bytes
2. Plot the Complementary Cumulative Probability Distribution (CCDF) of flow durations (i.e., the finish time minus the start time) and of flow sizes (i.e., number of bytes, and number of packets).
    - _The `p2_ccdf.py` script outputs are saved in the `res` directory, in `p2-linear/` and `p2-logarithmic/` folders._
    - First plot each graph with a linear scale on each axis, and then a second time with a logarithmic scale on each axis.
        - The [Python matplotlib library](https://matplotlib.org/3.1.1/gallery/statistics/histogram_cumulative.html) can plot the CCDF using histograms (it really plots the CDF but plotting the CCDF)
    - What are the main features of the graphs?
    - What artifacts of Netflow and of network protocols could be responsible for these features?
    - Why is it useful to plot on a logarithmic scale?
3. Summarize the traffic by which TCP/UDP port numbers are used.
    - _The two tables are available as a screenshot of `p3_ports.py` output, found in `res/3tables.png`_
    - Create two tables, listing the top-ten port numbers by __sender traffic volume__ (i.e., by source port number) and by __receiver traffic volume__ (i.e., by destination port number), including the percentage of traffic (by bytes) they contribute.
        - The results were computed through the use of the [NumPy library's](https://numpy.org/doc/stable/reference/generated/numpy.unique.html) `unique()` method, which returned a list of all values that appeared in a list, and the frequency of their appearance
        - I also used the [NumPy library's](https://numpy.org/doc/stable/reference/generated/numpy.argsort.html) `argsort()` method to figure the top 10 most frequently used ports for `src` and `dst` traffic

            | SRC Port | Frequency | Percentage of Traffic |
            |----------|-----------|-----------------------|
            | 80       | 175117    | 0.4394%               |
            | 443      | 19605     | 0.0173%               |
            | 53       | 12927     | 0.0013%               |
            | 0        | 9176      | 0.0064%               |
            | 25       | 5698      | 0.0002%               |
            | 22       | 5408      | 0.0217%               |
            | 1935     | 4285      | 0.0366%               |
            | 3074     | 3884      | 0.0008%               |
            | 3389     | 3202      | 0.0009%               |
            | 2128     | 2293      | 0.0011%               |

            | DST Port | Frequency | Percentage of Traffic |
            |----------|-----------|-----------------------|
            | 80       | 319929    | 0.0293%               |
            | 443      | 34727     | 0.0077%               |
            | 53       | 17006     | 0.0005%               |
            | 445      | 11620     | 0.0002%               |
            | 25       | 8902      | 0.0035%               |
            | 123      | 8378      | 0.0003%               |
            | 1935     | 7933      | 0.0017%               |
            | 3074     | 6365      | 0.0011%               |
            | 2048     | 3410      | 0.0002%               |
            | 0        | 2965      | 0.0061%               |
    - Where possible, explain what applications are likely be responsible for this traffic. (_See the IANA port numbers reference for details_)
        - For the `src` ports:
            - Port 80 was used most frequently. It is dedicated to HTTP traffic, therefore it is expected to be the most used. It also makes sense the port dedicated to HTTPS (TLS/SSL encrypted) traffic is the second most frequently used port (port 443).
            - Port 0 was also used, [though it shouldn't be according to this source](https://www.speedguide.net/port.php?port=0), frequently; it is used for socket binding to determine ports to use for the connections
            - Port 53 is used by the DNS to translate domain names to IP addresses
            - Port 25 is used for SMTP (mail routing)
            - Port 22 is used for SSH logins and file transfers
            - Port 1935 is used for Adobe Flash communications
            - Port 3074 is used for Xbox Live and Windows games
            - Port 3389 is used by Microsoft for remote desktop connections
            - Port 2128 is reserved by Net Steward Control _need more looking into_
        - For the `dst` ports:
            - Much of the same in the Top 10 of `src` ports appeared in this table, as expected.
            - Port 445 is used for direct TCP networking access, making it vulnerable to threats
            - Port 123 is used for time synchronization, also making it vulnerable to threats
            - Port 2048 is reserved by a DLS-monitor _need more looking into_
    - Explain any significant differences between the results for __sender vs. receiver__ port numbers.
        - As expected, there are similar `src` and `dst` ports used in the dataset
        - However, the major differences can be found in that the most commonly used `dst` ports are also most vulnerable to threats.
4. Aggregate the traffic volumes based on the source IP prefix.
    - _The results of the `p4_src_traffic_agg.py` script can be found in `res/4agg-all_masks.png` and `res/4agg-filtered.png`_
    - What fraction of the total traffic comes from the most popular (by number of bytes) 0.1% of source IP prefixes? the most popular 1% of source IP prefixes? the most popular 10% of source IP prefixes?

        |      | Data Flow (GB) | Percentage of Total | Source IP Prefixes                                         |
        |------|----------------|---------------------|------------------------------------------------------------|
        | 0.1% | 1.254          | 0.45%               | 0                                                          |
        | 1%   | 1.626          | 0.59%               | 0, 22742, 1249, 111, 3, 557, 11, 40127, 6932, 25691, 22834 |
        | 10%  | 2.493          | 0.9%                | see program output in res/4agg-all_masks.png               |
    - Some flows will have a source mask length of 0. Report the fraction of traffic (by bytes) that has a source mask of 0, and then exclude this traffic from the rest of the analysis. That is, report the top 0.1%, 1%, and 10% of source prefixes that have positive mask lengths.
        - The traffic of the bytes that have a source mask length of `0` is 1.3e6 KB (or 1.24 GB). This comprised 0.43% of the total amount of bytes transferred.
        - The results for those packets sent from source IP prefixes whose mask length is greater than 0 now change to the following values:
        
            |      | Data Flow (GB) | Percentage of Total | Source IP Address Prefixes                                    |
            |------|----------------|---------------------|---------------------------------------------------------------|
            | 0.1% | 0.1088         | 0.039%              | 22742                                                         |
            | 1%   | 0.4651         | 0.17%               | 22742, 1249, 111, 3, 557, 11, 40127, 6932, 25691, 22834, 1351 |
            | 10%  | 1.292          | 0.47%               | see program output in `res/4agg-filtered.png`                 |
5. Assume an Organization A (Org-A) has the 128.112.0.0/16 address block. What fraction of the traffic (by bytes and by packets) in the trace is sent by Org-A? To Org-A?
    - _The script `p5_traffic.py` calculates this throughout the current trace._
        - First, we find the number of occurrences the `128.112` appears in the dataset as either a source or destination IP address. We use this substring because the `16` of the address means we have 16 bits dedicated to the address block. This was done using the [NumPy library's](https://numpy.org/devdocs/reference/generated/numpy.char.find.html) `char.find` method.
        - Then we calculate the number of bytes and packets sent to and from this IP address block.
    - The values found are presented in this table. The output of the program is also reported in `res/5traffic.png`
    
        |             | Bytes (MB) | Packets |
        |-------------|------------|---------|
        | Source      | 19.9       | 39352   |
        | Destination | 62.3       | 56974   |
        | Total       | 82.2       | 96326   |
        | Fraction    | 0.0289%    | 0.0248% |
