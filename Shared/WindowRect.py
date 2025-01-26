from PyQt6.QtGui import QColor

from Shared import CanvasUtils, ColorTools
from Shared.ValueInterpolator import ValueInterpolator
from Shared.ColorInterpolator import ColorInterpolator


class WindowRect:
    def __init__(self, data, instanceId):
        self.data = data
        self.instanceId = instanceId

        self.marginInwards = ValueInterpolator(30)
        self.lineWidth = ValueInterpolator(8)

        self.width = ValueInterpolator(400)
        self.height = ValueInterpolator(200)

        self.x = ValueInterpolator(-200)
        self.y = ValueInterpolator(-100)

        self.line_color = ColorInterpolator(QColor.fromRgb(200, 200, 200))
        self.line_opacity = ValueInterpolator(1.0)

        self.text_x = ValueInterpolator(0)
        self.text_y = ValueInterpolator(0)

        self.text = ''
        self.text_color = ColorInterpolator(QColor.fromRgb(200, 200, 200))
        self.text_opacity = ValueInterpolator(0.0)
        self.font_size = ValueInterpolator(12)

        self.fill_color = ColorInterpolator(QColor.fromRgb(0, 0, 0, 0))

    def drawMyself(self, painter):
        CanvasUtils.drawRectAt(painter=painter,
                               data=self.data,
                               raw_pos=(self.x.getValue() + self.marginInwards.getValue(), self.y.getValue() + self.marginInwards.getValue()),
                               size=(self.width.getValue() - 2 * self.marginInwards.getValue(), self.height.getValue() - 2 * self.marginInwards.getValue()),
                               outline_width=self.lineWidth.getValue(),
                               outline_color=ColorTools.apply_opacity_to_color(self.line_color.getValue(), self.line_opacity.getValue()),
                               fill_color=self.fill_color.getValue())

        CanvasUtils.drawTextAt(painter=painter, data=self.data,
                               raw_pos=(self.x.getValue() + self.width.getValue() / 2 + self.text_x.getValue(), self.y.getValue() + self.height.getValue() / 2 + self.text_y.getValue()),
                               text=self.text,
                               color=ColorTools.apply_opacity_to_color(self.text_color.getValue(), self.text_opacity.getValue()), font_size=self.font_size.getValue(), scaleFont=True)

    def updatePhysics(self):
        pass

    def updateGraphics(self, painter):
        self.drawMyself(painter)
