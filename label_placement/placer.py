from typing import Dict, List, Optional
from copy import deepcopy
from loguru import logger

from .constants import X_LIM, Y_LIM
from .sat_solver import TwoSatSolver
from .data import Label, Box
from .utils import label_to_bbox


class Placer:
    @classmethod
    def __spatial_filtering(cls, labels: List[Label]) -> List[Label]:
        def bbox_in_boundaries(bbox: Box) -> bool:
            return (
                (bbox.x1 >= 0)
                & (bbox.y1 >= 0)
                & (bbox.x2 <= X_LIM)
                & (bbox.y2 <= Y_LIM)
            )

        return list(
            filter(
                lambda label: bbox_in_boundaries(label_to_bbox(label)),
                labels,
            )
        )

    @classmethod
    def filter(cls, labels: List[List[Label]]) -> Optional[List[List[Label]]]:
        for idx in range(len(labels)):
            labels[idx] = cls.__spatial_filtering(labels[idx])
            if not labels[idx]:
                logger.warning("Can't find placement for {}", idx + 1)
        return list(filter(lambda x: x, labels))

    @classmethod
    def __return_labels(
        cls, solution: Optional[Dict[str, bool]], l_labels: List[List[Label]]
    ) -> Optional[List[Label]]:

        if solution is None:
            logger.warning("SAT solution is None.")
            return None

        labels_solution = []
        for idx, labels in enumerate(l_labels):
            try:
                labels_solution.append(labels[int(solution[f"x{idx}"])])
            except KeyError:
                labels_solution.append(labels[0])

        return labels_solution

    @classmethod
    def make_placement(
        cls, possible_labels: List[List[Label]]
    ) -> Optional[List[Label]]:
        if not possible_labels:
            logger.warning("0 possible labels.")
            return None

        possible_labels = deepcopy(possible_labels)

        for labels in possible_labels:
            if len(labels) == 1:
                labels.append(labels[0])
            elif len(labels) > 2:
                logger.warning(
                    "Maximum 2 positions are "
                    + "possible for every label, found {}",
                    len(labels),
                )
                labels = labels[:2]

        bboxes = [
            list(map(label_to_bbox, labels)) for labels in possible_labels
        ]

        graph = TwoSatSolver.create_graph(bboxes)
        solution = TwoSatSolver.solve(graph)
        return cls.__return_labels(solution, possible_labels)
