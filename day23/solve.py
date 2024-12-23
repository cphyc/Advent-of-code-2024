from functools import reduce
from itertools import combinations
from pathlib import Path
import networkx as nx

test_data = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

data = (Path(__file__).parent / "input").read_text()


def parse(data: str) -> nx.Graph:
    g = nx.Graph()
    g.add_edges_from(line.split("-") for line in data.splitlines())
    return g


def part1(g: nx.Graph):
    # Find 3-loops in the graph
    candidates = helper(g, list(set((_,)) for _ in g.nodes), 3)
    t_candidates = [
        truple for truple in candidates if any(node.startswith("t") for node in truple)
    ]
    print(f"Part 1: {len(t_candidates)}")
    return candidates



def helper(g: nx.Graph, nuples: list[set[str]], max_depth: int) -> list[set[str]]:
    # print(f"Length: {len(nuples[0])}, found {len(nuples)=}")
    if len(nuples[0]) == max_depth:
        return nuples

    muples = []
    # Try all combinations of n-uples
    for s1, s2 in combinations(nuples, 2):
        new1 = list(s1 - s2)
        new2 = list(s2 - s1)

        if not (len(new1) == len(new2) == 1):
            continue

        n1 = new1[0]
        n2 = new2[0]

        # Make sure new1 is connected to all of s2
        ok = all(g.has_edge(n1, old2) for old2 in s2)
        if not ok:
            continue
        ok &= all(g.has_edge(n2, old1) for old1 in s1)
        if not ok:
            continue

        s12 = s1.union({n2})
        if s12 not in muples:
            muples.append(s12)

    if len(muples) == 0:
        return nuples

    all_nodes = reduce(set.union, muples)

    current_degree = len(muples[0])
    new_g = nx.Graph()
    new_g.add_edges_from(
        (ni, nj)
        for ni, nj in g.edges
        if (
            ni in all_nodes
            and nj in all_nodes
            and g.degree(ni) >= current_degree
            and g.degree(nj) >= current_degree
        )
    )

    # print(f"Started with {g}, now {new_g}")

    return helper(new_g, muples, max_depth)

def part2(g: nx.Graph):
    max_len = 0
    biggest_boy = []
    for n in list(g.nodes):
        candidates = set(g.neighbors(n))
        candidates.add(n)
        g2 = nx.Graph()
        g2.add_edges_from(
            (ni, nj) for ni, nj in g.edges if ni in candidates or nj in candidates
        )
        ret = helper(g2, list(set((_,)) for _ in g2.nodes), 100)
        if ret and len(ret[0]) > max_len:
            max_len = len(ret[0])
            biggest_boy = ret
            print(f"New max: {max_len}")
        if len(ret[0]) == 13:
            break
        else:
            g.remove_node(n)

    answer = ",".join(sorted(biggest_boy[0]))
    print(f"Part 2: {answer}")


g = parse(data)

# truples = part1(g)
part1(g)
part2(g)
