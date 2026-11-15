import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from graph_model import load_csv, build_graph

class DisjointSet:
    """Union-Find (DSU) for Kruskal."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False

        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1
        return True

def collect_undirected_edges(graph):
    """
    Convert adjacency list into unique undirected edges.
    Each edge appears once as (u, v, weight) with u < v.
    """
    edges = []
    seen = set()

    for u, neighbors in graph.items():
        for v, weight in neighbors:
            if weight is None:
                continue
            a, b = sorted([u, v])
            key = (a, b)
            if key in seen:
                continue
            seen.add(key)
            edges.append((a, b, float(weight)))

    return edges

def kruskal_mst(graph):
    """
    Kruskal's algorithm.
    Returns:
      mst_edges: list of (u, v, weight)
      total_weight: sum of MST edge weights
    """
    nodes = list(graph.keys())
    edges = collect_undirected_edges(graph)
    edges.sort(key=lambda e: e[2])  # sort by weight ascending

    dsu = DisjointSet(nodes)
    mst_edges = []
    total_weight = 0.0

    for u, v, w in edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            # stop early if tree is complete
            if len(mst_edges) == len(nodes) - 1:
                break

    return mst_edges, total_weight

def main():
    locations = load_csv("locations_checked.csv")
    relationships = load_csv("relationships_checked.csv")
    nodes, graph = build_graph(locations, relationships)

    mst_edges, total_weight = kruskal_mst(graph)

    print("=== Kruskal Minimum Spanning Tree ===")
    print(f"MST edges: {len(mst_edges)}")
    print(f"Total weight: {total_weight:.1f} m")
    print()
    print("Edges in MST:")
    for u, v, w in mst_edges:
        u_name = nodes.get(u, {}).get("name", "?")
        v_name = nodes.get(v, {}).get("name", "?")
        print(f"  {u} ({u_name}) -- {v} ({v_name})  {w:.1f} m")

if __name__ == "__main__":
    main()