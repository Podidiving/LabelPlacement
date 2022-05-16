from .data import Box, Label, Position


def has_intersection(bbox1: Box, bbox2: Box) -> bool:
    x1 = max(bbox1.x1, bbox2.x1)
    x2 = min(bbox1.x2, bbox2.x2)
    y1 = max(bbox1.y1, bbox2.y1)
    y2 = min(bbox1.y2, bbox2.y2)
    return x1 < x2 and y1 < y2


def label_to_bbox(label: Label) -> Box:
    if label.position == Position.LEFT_MIDDLE:
        x = label.x
        y = label.y - label.height // 2
    elif label.position == Position.BOTTOM_MIDDLE:
        x = label.x - label.width // 2
        y = label.y
    elif label.position == Position.RIGHT_MIDDLE:
        x = label.x - label.width
        y = label.y - label.height // 2
    elif label.position == Position.TOP_MIDDLE:
        x = label.x - label.width // 2
        y = label.y - label.height
    elif label.position == Position.LEFT_TOP:
        x = label.x
        y = label.y - label.height
    elif label.position == Position.RIGHT_TOP:
        x = label.x - label.width
        y = label.y - label.height
    elif label.position == Position.RIGHT_BOTTOM:
        x = label.x - label.width
        y = label.y
    elif label.position == Position.LEFT_BOTTOM:
        x = label.x
        y = label.y
    else:
        raise NotImplementedError

    width = label.width
    height = label.height

    return Box(x1=x, y1=y, x2=x + width, y2=y + height)
