from itertools import product
from pathlib import Path
import networkx as nx

test_data = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

data = (Path(__file__).parent / "input").read_text().strip()

def parse(data: str) -> nx.DiGraph:
    topomap = [[int(c) for c in line] for line in data.splitlines()]
    Nrow = len(topomap)
    Ncol = len(topomap[0])

    graph = nx.DiGraph()
    # Create a graph connecting each node to its neighbors
    for (irow, icol) in product(range(Nrow), range(Ncol)):
        graph.add_node((irow, icol), height=topomap[irow][icol])

    for (irow, icol) in product(range(Nrow), range(Ncol)):
        for di, dj in ((-1, 0), (1, 0), (0, -1,), (0, 1)):
            if (
                0 <= irow + di < Nrow and
                0 <= icol + dj < Ncol and
                topomap[irow][icol] == topomap[irow+di][icol+dj] - 1
            ):
                graph.add_edge((irow, icol), (irow+di, icol+dj),)

    return graph

def part1(graph: nx.DiGraph):
    endpoints = [inode for inode in graph.nodes if graph.nodes[inode]["height"] == 9]
    trailheads = [inode for inode in graph.nodes if graph.nodes[inode]["height"] == 0]

    # Iterate over trailheads
    score = 0
    for trailhead in trailheads:
        for endpoint in endpoints:
            if nx.has_path(graph, trailhead, endpoint):
                score += 1

    print(f"Part 1: {score}")

def part2(graph: nx.DiGraph):
    ...

graph = parse(data)
part1(graph)
