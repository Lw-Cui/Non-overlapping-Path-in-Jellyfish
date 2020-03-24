# Non-overlapping Path Algorithm 

This repository implement and test 
non-overlapping path algorithm in Jellyfish Network.

## Path Diversity

Jellyfish network with 246 switches
(11 for peer switches and 1 for host).
![plot](./diversity.png)


## Throughput Comparision

Jellyfish network with 50 switches
(8 ports connecting peer switches and 1 for host). Links between switches are 10 Mbps.


|      Routing Algorithm  | All Hosts are Activated | Half Hosts are Activated |
| ------------- |:-------------:|:-------------:|
| Non-overlapping |    25.35 Mbps (↑16.1%)| 34.58 Mbps(↑23.6%) |
| K-Shortest-Paths   |  21.83 Mbps | 27.98 Mbps |

*All Hosts are Activated: 25 hosts as server, 25 hosts as client*

*Half Hosts are Activated: 12 hosts as server, 12 hosts as client*


