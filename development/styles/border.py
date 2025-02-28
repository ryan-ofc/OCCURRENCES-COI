from development.styles.colors import Colors


class type_border:
    solid: str = "solid"
    dashed: str = "dashed"
    dotted: str = "dotted"
    double: str = "double"
    groove: str = "groove"
    ridge: str = "ridge"
    inset: str = "inset"
    outset: str = "outset"
    hidden: str = "hidden"
    none: str = "none"


class Border:
    def __init__(
        self,
        pixel: int = 1,
        type_border: type_border = type_border.solid,
        color: Colors = Colors.gray,
    ):
        self.pixel = pixel
        self.type_border = type_border
        self.color = color

    def __str__(self):
        return f"{self.pixel}px {self.type_border} {self.color}"
