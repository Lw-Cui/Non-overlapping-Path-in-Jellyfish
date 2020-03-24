import random
from subprocess import Popen, PIPE
from time import sleep, time
from ripl.ripl.dctopo import JellyfishTopo

def main():
	nSwitches = 10
	nPorts = 3
	adjlist_file = "rrg_3_10"

	
	jelly_topo = JellyfishTopo(nSwitches, nPorts, adjlist_file)
	randomHosts = jelly_topo.hosts()
	random.shuffle(randomHosts)
	clients = randomHosts[0::2]
	servers = randomHosts[1::2]
	pairs_list = zip(clients, servers)
	
	for pair in pairs_list:
		print pair[1] + " iperf -s &"
		print pair[0] + " iperf -c %s -P 8 -t 60 >> results/ecmp_8_eight_output.txt &" %(pair[1])
	
if __name__ == '__main__':
	main()
