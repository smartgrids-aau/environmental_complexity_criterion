class Color():
    def __init__(self, r:int, g:int, b:int):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def hex_format(self):
        return '#{:02X}{:02X}{:02X}'.format(self.r, self.g, self.b)

def rgba_to_rgb(color: Color, alpha, back_color = Color(255, 255, 255)):
    return Color(
        (1 - alpha) * back_color.r + alpha * color.r,
        (1 - alpha) * back_color.g + alpha * color.g,
        (1 - alpha) * back_color.b + alpha * color.b
    ).hex_format()

def compute_alpha(value, min_alpha = 0.3, step_count = 5):
    fraction_alpha = 1 - min_alpha
    return min_alpha + min(value / step_count * fraction_alpha, fraction_alpha)