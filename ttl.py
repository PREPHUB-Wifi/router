import config

#http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None

def reach_all(graph, start):
    vertices = set(graph.keys())
    vertices.remove(start)
    longest = 0
    for vertex in vertices:
        path = shortest_path(graph, start, vertex)
        print(vertex, path)
        longest = max(longest, len(path))
    return longest

def ttl(start=config.HUB, graph=config.GRAPH):
    num_thru = reach_all(graph, start)
    num_jumps = max(0, num_thru - 1)
    return num_jumps

