# CS 244 Assignment 2
## Group: Austin Poore and Tommy Fan

This repository contains our code to reproduce experiments from Jellyfish: Networking Data Centers Randomly

## Setup
1. Run `bash setup.sh` to install Ripl and Riplpox

## Reproducing Figure 9

1. Open `build_topology.py` and set n to the number of desired switches and d to the number of inter-switch links
2. Run `python build_topology.py`
3. The plot should exist in the plots/ folder, and routes should be saved in transformed_routes. For example if n=10, d=3 then
the routing files should be ecmp_8_rrg_3_10.pkl and ksp_rrg_3_10.pkl

## Reproducing Table 1

1. In one terminal, start up Pox with the command 
```
pox/pox.py riplpox.riplpox --topo=jelly,[N_SWITCHES],[N_PORTS],[ADJLIST_FILE] --routing=jelly,[ROUTING_FILE] --mode=reactive

```
In this command, ADJLIST_FILE refers to the adjacency file that represents our topology, for example rrg_3_10. The ROUTING_FILE is as specified in transformed_routes.

2. In another terminal, open up tcp_tests.py and set the correct nSwitches, nPorts and adjlist_file. In this example, we'll do nSwitches=10, nPorts=3, adjlist_file="rrg_3_10". Change the mininet shell command to the appropriate one on line 38. For example if we're testing
8 parallel flows using ECMP-8, then it should read `iperf -c %s -P 8 -t 60 >> results/ecmp_8_eight_output.txt &`

3. Run `python tcp_tests.py > mn_script_ecmp_8_eight_flows`

4. Start Mininet. ```sudo mn --custom ripl/ripl/mn.py --topo jelly,[N_SWITCHES],[N_PORTS],[ADLIST_FILE] --link tc --controller=remote --mac```

5. In Mininet CLI, type `source mn_script_ecmp_8_eight_flows`

6. The output will be in the results folder.
