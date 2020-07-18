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
    - The average packet size can be calculated by the dividing the total amount of bytes (`sum(data[:][1])`) for all packets (or, the sum of `data`'s column 2) by the total number of packets (`sum(data[:][0])`) in the trace.
    - This value was calculated to be `768.18` bytes
2. Plot the Complementary Cumulative Probability Distribution (CCDF) of flow durations (i.e., the finish time minus the start time) and of flow sizes (i.e., number of bytes, and number of packets).
    - First plot each graph with a linear scale on each axis, and then a second time with a logarithmic scale on each axis.
    - What are the main features of the graphs?
    - What artifacts of Netflow and of network protocols could be responsible for these features?
    - Why is it useful to plot on a logarithmic scale?
3. Summarize the traffic by which TCP/UDP port numbers are used.
    - Create two tables, listing the top-ten port numbers by __sender traffic volume__ (i.e., by source port number) and by __receiver traffic volume__ (i.e., by destination port number), including the percentage of traffic (by bytes) they contribute.
        - The two tables are available as a screenshot of `ports.py` output, found in `tables.png`
        - The results were computed through the use of the [NumPy library's](https://numpy.org/doc/stable/reference/generated/numpy.unique.html) `unique()` method, which returned a list of all values that appeared in a list, and the frequency of their appearance
        - I also used the [NumPy library's](https://numpy.org/doc/stable/reference/generated/numpy.argsort.html) `argsort()` method to figure the top 10 most frequently used ports for `src` and `dst` traffic
    - Where possible, explain what applications are likely be responsible for this traffic. (_See the IANA port numbers reference for details_)
        - For the `src` ports:
            - Port 80 was used most frequently. It is dedicated to HTTP traffic, therefore it is expected to be the most used. It also makes sense the port dedicated to HTTPS (TLS/SSL encrypted) traffic is the second most frequently used port (port 443).
            - Port 0 was also used, [though it shouldn't be](https://www.speedguide.net/port.php?port=0), frequently; it is used for socket binding to determine ports to use for the connections
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
    - What fraction of the total traffic comes from the most popular (by number of bytes) 0.1% of source IP prefixes?
    - The most popular 1% of source IP prefixes?
    - The most popular 10% of source IP prefixes?
    - Some flows will have a source mask length of 0. Report the fraction of traffic (by bytes) that has a source mask of 0, and then exclude this traffic from the rest of the analysis. That is, report the top 0.1%, 1%, and 10% of source prefixes that have positive mask lengths.
5. Assume an Organization A (Org-A) has the 128.112.0.0/16 address block. What fraction of the traffic (by bytes and by packets) in the trace is sent by Org-A? To Org-A?
