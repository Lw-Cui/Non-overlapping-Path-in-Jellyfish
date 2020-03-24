import os
import sys
import networkx
import matplotlib as mpl
import random

mpl.use('Agg')
import matplotlib.pyplot as plt
import pickle
from itertools import islice
from jelly_utils import *


def reset_weight(networkx_graph, n):
    for u, v, a in networkx_graph.edges(data=True):
        networkx_graph[u][v]["weight"] = 1
        networkx_graph[v][u]["weight"] = 1


def get_weight(networkx_graph, path):
    cnt = 0
    for hd in range(len(path) - 1):
        cnt += networkx_graph[str(path[hd])][str(path[hd + 1])]["weight"]
    return cnt


def compute_non_overlapping_paths(networkx_graph, n):
    paths = {}
    for a in range(n):
        paths[(str(a), str(a))] = [[str(a)]]
        for b in range(a + 1, n):
            reset_weight(networkx_graph, n)
            while True:
                shortest_path = networkx.shortest_path(networkx_graph, source=str(a), target=str(b), weight="weight")
                if get_weight(networkx_graph, shortest_path) > 100000:
                    break
                if (str(a), str(b)) not in paths:
                    paths[(str(a), str(b))] = [shortest_path]
                else:
                    paths[(str(a), str(b))].append(shortest_path)

                for hd in range(len(shortest_path) - 1):
                    networkx_graph[str(shortest_path[hd])][str(shortest_path[hd + 1])]["weight"] += 100000
                    networkx_graph[str(shortest_path[hd + 1])][str(shortest_path[hd])]["weight"] += 100000

    return paths


def compute_ecmp_paths(networkx_graph, n):
    ecmp_paths = {}
    for a in range(n):
        ecmp_paths[(str(a), str(a))] = [[str(a)]]
        for b in range(a + 1, n):
            shortest_paths = networkx.all_shortest_paths(networkx_graph, source=str(a), target=str(b))
            ecmp_paths[(str(a), str(b))] = [p for p in shortest_paths]
    return ecmp_paths


def compute_k_shortest_paths(networkx_graph, n, k=8):
    all_ksp = {}
    for a in range(n):
        all_ksp[(str(a), str(a))] = [[str(a)]]
        for b in range(a + 1, n):
            ksp = list(islice(networkx.shortest_simple_paths(networkx_graph, source=str(a), \
                                                             target=str(b)), k))
            all_ksp[(str(a), str(b))] = ksp
    return all_ksp


def get_path_counts(distinct, ecmp_paths, all_ksp, traffic_matrix, all_links):
    counts = {}
    # initialize counts for all links
    for link in all_links:
        a, b = link
        counts[(str(a), str(b))] = {"8-ksp": 0, "8-ecmp": 0, "64-ecmp": 0, "distinct": 0}
        counts[(str(b), str(a))] = {"8-ksp": 0, "8-ecmp": 0, "64-ecmp": 0, "distinct": 0}
    for start_host in range(len(traffic_matrix)):
        dest_host = traffic_matrix[start_host]
        start_node = start_host / 3
        dest_node = dest_host / 3
        if start_node == dest_node:
            continue
        # swap them so that start_node < dest_node
        if start_node > dest_node:
            start_node, dest_node = dest_node, start_node
        paths = ecmp_paths[(str(start_node), str(dest_node))]
        if len(paths) > 64:
            paths = paths[:64]
        for i in range(len(paths)):
            path = paths[i]
            prev_node = None
            for node in path:
                if not prev_node:
                    prev_node = node
                    continue
                link = (str(prev_node), str(node))
                if i < 8:
                    counts[link]["8-ecmp"] += 1
                counts[link]["64-ecmp"] += 1
                prev_node = node

        ksp = all_ksp[(str(start_node), str(dest_node))]
        for path in ksp:
            prev_node = None
            for node in path:
                if not prev_node:
                    prev_node = node
                    continue
                link = (str(prev_node), str(node))
                counts[link]["8-ksp"] += 1
                prev_node = node

        ksp = distinct[(str(start_node), str(dest_node))]
        for path in ksp:
            prev_node = None
            for node in path:
                if not prev_node:
                    prev_node = node
                    continue
                link = (str(prev_node), str(node))
                counts[link]["distinct"] += 1
                prev_node = node

    return counts


def assemble_histogram(path_counts, file_name):
    ksp_distinct_paths_counts = []
    ecmp_8_distinct_paths_counts = []
    ecmp_64_distinct_paths_counts = []
    distinct_paths_counts = []

    for _, value in sorted(path_counts.iteritems(), key=lambda (k, v): (v["8-ksp"], k)):
        ksp_distinct_paths_counts.append(value["8-ksp"])
    for _, value in sorted(path_counts.iteritems(), key=lambda (k, v): (v["8-ecmp"], k)):
        ecmp_8_distinct_paths_counts.append(value["8-ecmp"])
    for _, value in sorted(path_counts.iteritems(), key=lambda (k, v): (v["64-ecmp"], k)):
        ecmp_64_distinct_paths_counts.append(value["64-ecmp"])
    for _, value in sorted(path_counts.iteritems(), key=lambda (k, v): (v["distinct"], k)):
        distinct_paths_counts.append(value["distinct"])

    #	print ksp_distinct_paths_counts
    #	print ecmp_8_distinct_paths_counts
    #	print ecmp_64_distinct_paths_counts
    x = range(len(ksp_distinct_paths_counts))
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(x, ksp_distinct_paths_counts, color='b', label="8 Shortest Paths")
    ax1.plot(x, ecmp_64_distinct_paths_counts, color='r', label="64-way ECMP")
    ax1.plot(x, ecmp_8_distinct_paths_counts, color='g', label="8-way ECMP")
    ax1.plot(x, distinct_paths_counts, color='y', label="Non-overlapping Paths")
    plt.legend(loc="upper left");
    ax1.set_xlabel("Rank of Link")
    ax1.set_ylabel("# of Distinct Paths Link is on")
    plt.savefig("plots/%s_plot.png" % file_name)


def save_obj(obj, name):
    with open('pickled_routes/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('pickled_routes/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


# Code adapted from:
# https://stackoverflow.com/questions/25200220/generate-a-random-derangement-of-a-list
def random_derangement(n):
    while True:
        v = range(n)
        for j in range(n - 1, -1, -1):
            p = random.randint(0, j)
            if v[p] == j:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if v[0] != 0:
                return tuple(v)


def main():
    n = 246
    numHosts = 3 * n
    d = 11
    reuse_old_result = True
    ecmp_paths = {}
    all_ksp = {}
    file_name = "rrg_%s_%s" % (d, n)
    if not reuse_old_result:
        graph = networkx.random_regular_graph(d, n)
        networkx.write_adjlist(graph, file_name)
        graph = networkx.read_adjlist(file_name)

        print "Computing ECMP paths"
        ecmp_paths = compute_ecmp_paths(graph, n)
        save_obj(ecmp_paths, "ecmp_%s" % (file_name))
        print "Computing K shortest paths"
        all_ksp = compute_k_shortest_paths(graph, n)
        save_obj(all_ksp, "ksp_%s" % (file_name))
        print "Computing non-overlapping paths"
        non_overlapping = compute_non_overlapping_paths(graph, n)
        save_obj(non_overlapping, "unique_%s" % (file_name))
    else:
        graph = networkx.read_adjlist(file_name)

        ecmp_paths = load_obj("ecmp_%s" % (file_name))
        all_ksp = load_obj("ksp_%s" % (file_name))
        non_overlapping = load_obj("unique_%s" % (file_name))
    print "Assembling counts from paths"

    derangement = random_derangement(numHosts)
    all_links = graph.edges()
    path_counts = get_path_counts(non_overlapping,ecmp_paths, all_ksp, derangement, all_links)
    print "Making the plot"
    assemble_histogram(path_counts=path_counts, file_name=file_name)

    print "Transforming routes for Ripl/Riplpox use"
    print "Transforming KSP"
    transformed_ksp_routes = transform_paths_dpid("ksp_%s" % (file_name), n, 8)
    save_routing_table(transformed_ksp_routes, "ksp_%s" % (file_name))
    print "Transforming ECMP 8"
    transformed_ecmp_routes = transform_paths_dpid("ecmp_%s" % (file_name), n, 8)
    save_routing_table(transformed_ecmp_routes, "ecmp_8_%s" % (file_name))
    print "Transforming non-overlapping"
    transformed_ecmp_routes = transform_paths_dpid("unique_%s" % (file_name), n, 8)
    save_routing_table(transformed_ecmp_routes, "unique_%s" % (file_name))


if __name__ == "__main__":
    main()
