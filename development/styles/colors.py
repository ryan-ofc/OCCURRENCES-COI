class rgba:
    def __init__(self, r: int = 255, g: int = 255, b: int = 255, a: int | float = 1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self):
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"
    
    def adjust_tonality(self, percentage: int = 50):
        """Ajusta a tonalidade de cada componente de cor individualmente com base em um percentual.
        A cor escurece abaixo de 50% até 0% (preto) e clareia acima de 50% até 100% (branco).
        """

        percentage = max(0, min(100, percentage))

        if percentage == 50:
            return self
        
        if percentage > 50:
            factor = (percentage - 50) * 2
            self.r = min(255, self.r + factor)
            self.g = min(255, self.g + factor)
            self.b = min(255, self.b + factor)

        elif percentage < 50:
            factor = (50 - percentage) * 2
            self.r = max(0, self.r - factor)
            self.g = max(0, self.g - factor)
            self.b = max(0, self.b - factor)

        return self


def adjust_color(color: rgba, factor, is_percentage=False):
    """Ajusta o brilho de uma cor com base em um fator, podendo ser percentual ou exato.
    Um valor positivo clareia a cor e um valor negativo escurece.

    :param color: Instância da classe rgba (r, g, b, a)
    :param factor: Fator de ajuste (positivo para clarear, negativo para escurecer).
    :param is_percentage: Se for True, o fator é interpretado como percentual (em relação a 255).
    :return: Nova cor RGBA ajustada.
    """
    if is_percentage:
        factor = (factor / 100) * 255  # Converte o percentual para valor absoluto baseado em 255

    r, g, b, a = color.r, color.g, color.b, color.a
    r = max(0, min(255, int(r + factor)))
    g = max(0, min(255, int(g + factor)))
    b = max(0, min(255, int(b + factor)))
    return rgba(r, g, b, a)


class Colors:
    red = rgba(255, 0, 0)
    green = rgba(0, 255, 0)
    blue = rgba(0, 0, 255)
    black = rgba(0, 0, 0)
    white = rgba(255, 255, 255)
    gray = rgba(128, 128, 128)
    light_gray = rgba(211, 211, 211)
    dark_gray = rgba(64, 64, 64)
    yellow = rgba(255, 255, 0)
    orange = rgba(255, 165, 0)
    purple = rgba(128, 0, 128)
    pink = rgba(255, 192, 203)
    brown = rgba(139, 69, 19)
    cyan = rgba(0, 255, 255)
    magenta = rgba(255, 0, 255)
    transparent = rgba(0, 0, 0, 0)

    @staticmethod
    def adjust_color_for_all(factor, is_percentage=False):
        """Ajusta a tonalidade de todas as cores definidas na classe Colors."""
        adjusted_colors = {
            color: adjust_color(getattr(Colors, color), factor, is_percentage)
            for color in dir(Colors)
            if isinstance(getattr(Colors, color), rgba)
        }
        for color, adjusted in adjusted_colors.items():
            setattr(Colors, color, adjusted)
