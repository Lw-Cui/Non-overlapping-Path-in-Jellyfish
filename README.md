# k-non-overlapping Path Algorithm 

## Motivation
The high capacity mentioned in the [Jellyfish paper](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final82.pdf) inspires us to explore its potential to tackle burst flow. We want to maximize the average throughput at the expense of tolerable latency.

[slides](https://docs.google.com/presentation/d/1iPXMhChZSoxUF0wdVdqB6OcjMytnGAiv8M9-n3hED6o/edit?usp=sharing)

## Progress

We put forward and implemented a new routing algorithm named **k-non-overlapping Path**, which guarantees all links on paths from A to B have no overlapping.

This repository implements and tests non-overlapping path algorithm in Jellyfish Network.

### Path Diversity

Jellyfish network with 246 switches (11 for peer switches and 1 for host). Based on Jellyfish Paper Figure 9.
![plot](./diversity.png)


### Average Throughput per Server

Jellyfish network with 50 switches
(8 ports connecting peer switches and 1 for host). Links between switches are 10 Mbps.

|      Routing Algorithm  | 25 Servers / 25 Clients | 12 Servers / 12 Clients |
| ------------- |:-------------:|:-------------:|
| 8-Non-overlapping |    25.35 Mbps (↑16.1%)| 34.58 Mbps(↑23.6%) |
| 8-Shortest-Paths   |  21.83 Mbps | 27.98 Mbps |


The result is subject to lots of factors and may differ in different machine.

## Build

### Creating Environment

The most recommended way to reproduce it is using [google computer engine](https://cloud.google.com/compute); we provided a public image for the whole test environment. Simply run in [google cloud shell](https://cloud.google.com/shell):

```
gcloud compute instances create [VM Name] --image non-overlapping --image-project winter-cargo-272015
```

and then you are all set. 

Any questions, please check documents on [Creating an instance with an image shared with you](https://cloud.google.com/compute/docs/instances/create-start-instance#sharedimage). You may want to create a high-performance VM for the following experiments.

Alternatively, if you would like to build it from scratch, you should install [Mininet](https://github.com/mininet/mininet) first, clone the repo and execute `bash setup.sh`.
During this process, you may encounter some problems like `ModuleNotFoundError: No module named 'networkx'`. Deal with it yourself and good luck to you.

###  Test Prep
After finishing configuration, 
```
ssh mininet@[Your VM IP]
```
the password is also `mininet`.

Then run
```
sudo git fetch origin master
sudo git reset --hard origin/master
sudo bash setup.sh
```
to assure you get and install the lastest code.

To generate topology and test script, run 
```
python build_topology.py && python tcp_test.py > test.sh
```
The default settings is 50 switches (8 ports connecting peer switches and 1 for host); 12 senders and 12 receivers.

### Run Test

Start controller first:
```
pox/pox.py riplpox.riplpox --topo=jelly,50,8,rrg_8_50 --routing=jelly,unique_rrg_8_50 --mode=reactive
```
Then in a new shell, run
```
sudo mn --custom ripl/ripl/mn.py --topo jelly,50,8,rrg_8_50 --link tc --controller=remote --mac
```

Wait until `result/output.txt` exists (about half minute), then run
```
python data_process.py results/output.txt
```
Result is like this:

```
[SUM]  0.0-10.6 sec  42.9 MBytes  33.9 Mbits/sec
[SUM]  0.0-11.2 sec  47.8 MBytes  35.9 Mbits/sec
[SUM]  0.0-10.7 sec  48.0 MBytes  37.6 Mbits/sec
[SUM]  0.0-11.5 sec  57.0 MBytes  41.6 Mbits/sec
[SUM]  0.0-10.7 sec  36.0 MBytes  28.1 Mbits/sec
[SUM]  0.0-10.7 sec  46.2 MBytes  36.3 Mbits/sec
[SUM]  0.0-11.6 sec  48.6 MBytes  35.1 Mbits/sec
[SUM]  0.0-11.3 sec  41.9 MBytes  31.1 Mbits/sec
[SUM]  0.0-11.3 sec  26.9 MBytes  20.0 Mbits/sec
[SUM]  0.0-10.9 sec  32.4 MBytes  24.9 Mbits/sec
[SUM]  0.0-10.6 sec  52.0 MBytes  41.0 Mbits/sec
[SUM]  0.0-10.9 sec  43.2 MBytes  33.4 Mbits/sec
33.2416666667
```

Then the average throughput per server is 33.24 Mbps.

### Comparsion with ksp

**Stop** pox & mininet and **delete** `result/output.txt` first; old routing table in switches may influence result.

This time start controller, change `unique_rrg_8_50` to `ksp_rrg_8_50`:
```
pox/pox.py riplpox.riplpox --topo=jelly,50,8,rrg_8_50 --routing=jelly,ksp_rrg_8_50 --mode=reactive
```
and do things again.

## Acknowledge

We leveraged several libraries ([Mininet](https://github.com/mininet/mininet), [Pox](https://github.com/noxrepo/pox), [RipL](https://github.com/brandonheller/ripl), [RipL-POX](https://github.com/brandonheller/riplpox)) and some [open-source code](https://github.com/lechengfan/cs244-assignment2) to reproduce the Jellyfish network and k-shortest-paths routing. Thanks for their contribution!

