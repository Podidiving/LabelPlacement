from loguru import logger
import os
from typing import Optional

from .painter import Painter
from .parser import Parser
from .placer import Placer


class Solver:
    @classmethod
    def solve(
        cls,
        input_file: str,
        output_file: Optional[str],
    ) -> None:
        logger.info("Algorithm started.")
        if output_file is None:
            output_file = f"{os.path.splitext(input_file)[0]}.jpg"
            logger.info("Output path was None. Set to {}", output_file)
        if os.path.isfile(output_file):
            logger.warning("File {} exists. Will be rewritten", output_file)

        labels = Parser.parse(input_file)
        labels = Placer.filter(labels)
        labels = Placer.make_placement(labels)
        if labels is None:
            logger.warning("Failed to make placement.")
            return

        painter = Painter()
        painter.draw(labels)
        painter.save(output_file)
        logger.info("Saved to {}", output_file)
