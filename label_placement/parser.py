from yaml import safe_load as yload
from typing import List

from .data import Position, Label


class Parser:
    POSITION_STR_TO_ENUM = {
        "LEFT_MIDDLE": Position.LEFT_MIDDLE,
        "TOP_MIDDLE": Position.TOP_MIDDLE,
        "RIGHT_MIDDLE": Position.RIGHT_MIDDLE,
        "BOTTOM_MIDDLE": Position.BOTTOM_MIDDLE,
        "LEFT_TOP": Position.LEFT_TOP,
        "RIGHT_TOP": Position.RIGHT_TOP,
        "RIGHT_BOTTOM": Position.RIGHT_BOTTOM,
        "LEFT_BOTTOM": Position.LEFT_BOTTOM,
    }

    @classmethod
    def parse(cls, fname: str) -> List[List[Label]]:
        with open(fname, "r") as stream:
            labels_raw = yload(stream)
        assert isinstance(labels_raw, list), "Wrong input format."

        labels = list()
        for label in labels_raw:
            current_labels = list()
            for position_str in label["positions"]:
                current_labels.append(
                    Label(
                        x=label["x"],
                        y=label["y"],
                        width=label["width"],
                        height=label["height"],
                        position=cls.POSITION_STR_TO_ENUM[position_str],
                    )
                )
            labels.append(current_labels)

        return labels
