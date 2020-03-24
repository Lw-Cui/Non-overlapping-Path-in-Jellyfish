# Non-overlapping Path Algorithm 

This repository implements and tests
non-overlapping path algorithm in Jellyfish Network.

## Path Diversity

Jellyfish network with 246 switches
(11 for peer switches and 1 for host).
![plot](./diversity.png)


## Average Throughput per Servers

Jellyfish network with 50 switches
(8 ports connecting peer switches and 1 for host). Links between switches are 10 Mbps.

|      Routing Algorithm  | 25 Servers / 25 Clients | 12 Servers / 12 Clients |
| ------------- |:-------------:|:-------------:|
| Non-overlapping |    25.35 Mbps (↑16.1%)| 34.58 Mbps(↑23.6%) |
| K-Shortest-Paths   |  21.83 Mbps | 27.98 Mbps |



