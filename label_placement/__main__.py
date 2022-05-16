import os
from argparse import ArgumentParser, Namespace

from .solver import Solver


def parse_args() -> Namespace:
    parser = ArgumentParser("Label placement script.")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=False,
        default=os.path.join("misc", "data.yaml"),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        default=None,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    Solver.solve(args.input, args.output)


if __name__ == "__main__":
    main()
