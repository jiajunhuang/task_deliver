from exceptions import DAGCycleError


class DAG:
    def __init__(self):
        self.__dag = dict()

    def add_edge(self, u, v=None):
        if u in self.__dag:
            self.__dag[u].append(v)
        else:
            self.__dag[u] = [] if v is None else [v]

    def topo_sort(self):
        in_degrees = dict((u, 0) for u in self.__dag)
        for u in self.__dag:
            for v in self.__dag[u]:
                in_degrees[v] += 1

        result = []
        non_degrees = set(u for u in self.__dag if in_degrees[u] == 0)
        if not non_degrees:
            raise DAGCycleError()

        while non_degrees:
            u = non_degrees.pop()
            result.append(u)

            for v in self.__dag[u]:
                in_degrees[v] -= 1
                if in_degrees[v] == 0:
                    non_degrees.add(v)

        return result
