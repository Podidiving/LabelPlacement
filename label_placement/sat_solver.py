from typing import Dict, List, Optional
from collections import defaultdict

from .data import Box
from .utils import has_intersection


class TwoSatSolver:
    @classmethod
    def __get_all_nodes(cls, graph):
        nodes = set()
        for k, v in graph.items():
            nodes.update(
                [
                    k,
                ]
                + v
            )
        return nodes

    @classmethod
    def __find(cls, graph) -> Dict[str, int]:
        def _topological_sort(graph):
            def __topological_sort(graph, node, visited, order):
                visited[node] = True
                for next_node in graph[node]:
                    if not visited[next_node]:
                        __topological_sort(graph, next_node, visited, order)
                order.append(node)

            nodes = cls.__get_all_nodes(graph)

            visited = defaultdict(bool)
            order = list()
            for node in nodes:
                if not visited[node]:
                    __topological_sort(graph, node, visited, order)

            assert len(order) == len(nodes)
            return list(reversed(order))

        def _get_transposed_graph(graph):
            transposed_graph = defaultdict(list)
            for from_, to_list in graph.items():
                for to_ in to_list:
                    transposed_graph[to_].append(from_)
            return transposed_graph

        def _find_scc(graph, node, component_ix, curr_component_ix):
            component_ix[node] = curr_component_ix
            for next_node in graph[node]:
                if component_ix[next_node] is None:
                    _find_scc(
                        graph, next_node, component_ix, curr_component_ix
                    )

        order = _topological_sort(graph)
        graph_transposed = _get_transposed_graph(graph)

        component_ix = defaultdict(lambda: None)

        curr_component_ix = 0
        for node in order:
            if component_ix[node] is None:
                _find_scc(
                    graph_transposed, node, component_ix, curr_component_ix
                )
                curr_component_ix += 1

        assert len(component_ix) == len(order)
        return component_ix

    @classmethod
    def create_graph(cls, l_bboxes: List[List[Box]]) -> Dict[str, List[str]]:
        graph = defaultdict(list)

        for label_ix, bboxes in enumerate(l_bboxes):
            for i, bbox in enumerate(bboxes):
                for label_prime_ix, bboxes_prime in enumerate(l_bboxes):
                    if label_prime_ix == label_ix:
                        continue
                    for j, bbox_prime in enumerate(bboxes_prime):
                        if has_intersection(bbox, bbox_prime):
                            sat_var_impl_from = (
                                f"{'!' if i == 0 else ''}x{label_ix}"
                            )
                            sat_var_impl_to = (
                                f"{'!' if j == 1 else ''}x{label_prime_ix}"
                            )
                            graph[sat_var_impl_from].append(sat_var_impl_to)
        return graph

    @classmethod
    def solve(cls, graph: Dict[str, List[str]]) -> Optional[Dict[str, bool]]:
        variables = cls.__get_all_nodes(graph)
        variables = set(map(lambda x: x.replace("!", ""), variables))

        scc = cls.__find(graph)

        solution = dict()
        for var in variables:
            neg_var = f"!{var}"
            if scc[var] == scc[neg_var]:
                return None
            solution[var] = True if scc[var] > scc[neg_var] else False

        return solution
