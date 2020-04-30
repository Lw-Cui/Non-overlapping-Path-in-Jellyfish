import argparse
import random
from ripl.ripl.dctopo import JellyfishTopo

def main():
	parser = argparse.ArgumentParser(description='Generate topology')
	parser.add_argument('-n', '--node', nargs="?", type=int, default=50, help='number of switches')
	parser.add_argument('-p', '--port', nargs="?", type=int, default=8, help='number of ports for each switch')
	parser.add_argument('-t', '--test', nargs="?", type=int, default=20, help='number of server / client')

	args = parser.parse_args()
	nSwitches = args.node
	nPorts = args.port
	adjlist_file = "rrg_{}_{}".format(nSwitches, nPorts)


	jelly_topo = JellyfishTopo(nSwitches, nPorts, adjlist_file)
	randomHosts = jelly_topo.hosts()
	random.shuffle(randomHosts)
	clients = randomHosts[0::2]
	servers = randomHosts[1::2]
	pairs_list = zip(clients, servers)

	for pair in pairs_list[:args.test]:
		print pair[1] + " iperf -s &"
		print pair[0] + " iperf -c %s -P 8 >> results/output.txt &" %(pair[1])

if __name__ == '__main__':
	main()
