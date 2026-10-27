import heapq
import sys


def find_cycle(graph, names):
    n = len(names)

    # 0 = unvisited, 1 = currently visiting, 2 = finished
    state = [0] * n
    parent = [-1] * n

    for start in range(n):
        if state[start] != 0:
            continue

        stack = [(start, 0)]
        state[start] = 1

        while stack:
            node, index = stack[-1]

            if index == len(graph[node]):
                state[node] = 2
                stack.pop()
                continue

            neighbor = graph[node][index]
            stack[-1] = (node, index + 1)

            if state[neighbor] == 0:
                state[neighbor] = 1
                parent[neighbor] = node
                stack.append((neighbor, 0))

            elif state[neighbor] == 1:
                # Found a back edge: node -> neighbor
                cycle = [neighbor]
                current = node

                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]

                cycle.append(neighbor)
                cycle.reverse()

                return cycle

    return None


def main():
    input = sys.stdin.readline

    # n = number of modules
    # e = number of import relationships
    n, e = map(int, input().split())

    names = []
    module_id = {}

    for i in range(n):
        name = input().strip()
        names.append(name)
        module_id[name] = i

    # If A imports B:
    # B -> A
    graph = [[] for _ in range(n)]
    edges = set()

    for _ in range(e):
        a, b = input().split()

        a_id = module_id[a]
        b_id = module_id[b]

        edge = (b_id, a_id)

        # Ignore duplicate edges
        if edge not in edges:
            edges.add(edge)
            graph[b_id].append(a_id)

    # Calculate indegrees
    indegree = [0] * n

    for u in range(n):
        for v in graph[u]:
            indegree[v] += 1

    # Min-heap for lexicographically smallest module
    heap = []

    for i in range(n):
        if indegree[i] == 0:
            heapq.heappush(heap, (names[i], i))

    order = []

    while heap:
        name, node = heapq.heappop(heap)
        order.append(name)

        for neighbor in graph[node]:
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                heapq.heappush(
                    heap,
                    (names[neighbor], neighbor)
                )

    # No cycle
    if len(order) == n:
        print(" ".join(order))
        return

    # Cycle exists
    cycle = find_cycle(graph, names)

    if cycle:
        print("CYCLE", *[names[i] for i in cycle])


if __name__ == "__main__":
    main()