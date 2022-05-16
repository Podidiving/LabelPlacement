from typing import Tuple, List
from matplotlib import pyplot as plt
from matplotlib import patches


from .data import Box, Label
from .utils import label_to_bbox
from .constants import X_LIM, Y_LIM


class Painter:
    RECT_COLOR: str = "b"
    POINT_COLOR: str = "b"
    LW: int = 2

    def __init__(
        self,
        figsize: Tuple[int, int] = (15, 15),
    ):
        self._figsize = figsize
        self._fig = None
        self._ax = None
        self._initialize_canvas()

    def _initialize_canvas(self):
        self._fig = plt.figure(figsize=self._figsize)
        self._ax = self._fig.subplots()
        self._ax.set_xlim([0, X_LIM])
        self._ax.set_ylim([0, Y_LIM])

    def draw(self, labels: List[Label]):
        for label in labels:
            self.__draw_box(label_to_bbox(label))
            self.__draw_point(label.x, label.y)

    def __draw_box(self, bbox: Box):
        xy = (bbox.x1, bbox.y1)
        width = bbox.get_width()
        height = bbox.get_height()

        rect = patches.Rectangle(
            width=width,
            xy=xy,
            height=height,
            lw=self.LW,
            edgecolor=self.RECT_COLOR,
            facecolor="none",
        )
        self._ax.add_patch(rect)

    def __draw_point(self, x: float, y: float):
        self._ax.scatter([x], [y], lw=self.LW, color=self.POINT_COLOR)

    def save(self, name: str):
        self._fig.savefig(name)
