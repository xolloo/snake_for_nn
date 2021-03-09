import enum


class Color(tuple, enum.Enum):
    WHITE = (255, 255, 255)
    YELLOW = (223, 225, 0)
    ORANGE = (255, 191, 0)
    RED = (222, 49, 99)
    GREEN = (159, 226, 191)
    SILVER = (192, 192, 192)
    GOLD = (255, 215, 0)
    GRAY = (128, 128, 128)
    LIME = (0, 255, 0)
    BLUE = (0, 0, 255)



# sin(a) = abs(x2 - x1) / sqrt((abs(x2 - x1) ** 2) + (abs(y2 - y1) ** 2))


