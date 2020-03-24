import pickle
import pdb

def save_routing_table(obj, name):
    with open('transformed_routes/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('pickled_routes/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def create_routing_table(paths_file_name, numSwitches):
	table = {}
	for i in range(numSwitches):
	    table[str(i)] = {}
	all_paths = load_obj(paths_file_name)
	for key, value in all_paths.iteritems():
	    start, end = key
	    for pathId in range(len(value)):
		path = value[pathId]
		for i in range(len(path)-1):
		    nextHop = path[i+1]
		    currentNode = path[i]
		    src_dst_pair = (str(start), str(end))
		    if src_dst_pair not in table[str(currentNode)]:
			table[str(currentNode)][src_dst_pair] = {}
		    table[str(currentNode)][src_dst_pair][str(pathId)] = str(nextHop)
		#same but for the reverse direction
		for j in range(len(path)-1, 0, -1):
		    nextHop = path[j-1]
		    currentNode = path[j]
		    dst_src_pair = (str(end), str(start))
		    if dst_src_pair not in table[str(currentNode)]:
                        table[str(currentNode)][dst_src_pair] = {}
                    table[str(currentNode)][dst_src_pair][str(pathId)] = str(nextHop)
	    
	return table

def transform_paths_dpid(paths_file_name, numSwitches, maxLen):
	all_paths = load_obj(paths_file_name)
	table = {}
	for key, value in all_paths.iteritems():
		key_dpid = (switch_to_dpid(key[0]), switch_to_dpid(key[1]))
		table[key_dpid] = []
		reversed_key = (switch_to_dpid(key[1]), switch_to_dpid(key[0]))
		table[reversed_key] = []
		for path in value[:maxLen]:
			transformed_path = list(map(switch_to_dpid, path))
			table[key_dpid].append(transformed_path)
			table[reversed_key].append(transformed_path[::-1])
	return table

def switch_to_dpid(switchIndex):
	return str(switchIndex) + "_1"

