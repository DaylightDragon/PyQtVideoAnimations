from PyQt6.QtGui import QColor


def apply_opacity_to_color(color: QColor, opacity: float):
    r, g, b, a = color.red(), color.green(), color.blue(), color.alpha()
    alpha = int(opacity * 255)
    return QColor.fromRgb(r, g, b, alpha)