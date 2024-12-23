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
    g.add_edges_from(
        line.split("-") for line in data.splitlines()
    )
    return g

def part1(g: nx.Graph):
    # Find 3-loops in the graph
    candidates = sorted(
        truple for truple in nx.simple_cycles(g, 3)
        if any(node.startswith("t") for node in truple)
    )
    print(f"Part 1: {len(candidates)}")


g = parse(data)

part1(g)
