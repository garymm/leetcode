import collections
import dataclasses
import math

def calcEquation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    """Build a graph from equations (edge and backwards edge for each equation).
    Then I want to find the shortest path between query[0] and query[1].
    """
    numeratorToDenominators = collections.defaultdict(list)
    edgeToVal = {}
    for i, eqn in enumerate(equations):
        numeratorToDenominators[eqn[0]].append(eqn[1])
        edgeToVal[(eqn[0], eqn[1])] = values[i]
        numeratorToDenominators[eqn[1]].append(eqn[0])
        edgeToVal[(eqn[1], eqn[0])] = 1 / values[i]

    # We're told both equations and queries are pretty short, so no real advantage
    # to e.g. precomputing shortest paths from each source.
    ret = []
    for src, dst in queries:
        if src not in numeratorToDenominators or dst not in numeratorToDenominators:
            ret.append(-1)
            continue

        if src == dst:
            ret.append(1.0)
            continue

        # dijkstra's algorithm
        prev = {}
        dist = collections.defaultdict(lambda: float("inf"))
        dist[src] = 0

        q = [src]
        visited = set()
        while q:
            cur = q.pop()
            if cur in visited:
                continue
            visited.add(cur)
            for neighbor in numeratorToDenominators[cur]:
                if dist[neighbor] > dist[cur] + 1:
                    dist[neighbor] = dist[cur] + 1
                    prev[neighbor] = cur
                q.append(neighbor)
            q = sorted(q, key=lambda var_name: dist[var_name], reverse=True)

        # build the path from dst to src
        if dst not in prev:
            ret.append(-1)
            continue
        edge_src = prev[dst]
        path = [(edge_src, dst)]
        while edge_src != src:
            next_edge_src = prev[edge_src]
            path.append((next_edge_src, edge_src))
            edge_src = next_edge_src

        ret.append(math.prod(edgeToVal[edge] for edge in path))

    return ret

# print(calcEquation([["a","b"],["b","c"]], [2.0,3.0], [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]))
print(calcEquation([["a","b"],["c","d"]], [1.0,1.0], [["a","c"],["b","d"],["b","a"],["d","c"]]))
