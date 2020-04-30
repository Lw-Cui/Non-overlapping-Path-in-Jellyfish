import sys


def average(lst):
    return sum(lst) / len(lst)


def main():
    f = open(sys.argv[1], "r")
    lines = [l for l in f.readlines() if l.startswith("[SUM]")]
    print(''.join(x for x in lines)) 
    print("[REPORT] The average throughput per server is {} Mbits/sec".format(average([float(l.split()[5]) for l in lines])))


if __name__ == "__main__":
    main()
