from PyQt6.QtGui import QColor

from Shared import CanvasUtils, ColorTools
from Shared.ValueInterpolator import ValueInterpolator
from Shared.ColorInterpolator import ColorInterpolator


class NumberText:
    def __init__(self, data, instanceId):
        self.data = data
        self.instanceId = instanceId

        self.x = ValueInterpolator(-200)
        self.y = ValueInterpolator(-100)

        self.text = ''
        self.text_color = ColorInterpolator(QColor.fromRgb(200, 200, 200))
        self.text_opacity = ValueInterpolator(0.0)
        self.font_size = ValueInterpolator(12)

        self.animation_extra_font_size = ValueInterpolator(2)

        self.actual_font_size = ValueInterpolator(self.font_size.getValue())
        self.actual_font_size.setCustomInternalGetFunc(lambda: self.font_size.getValue())
        self.__lastWholeNumber = None

    def drawMyself(self, painter):
        curWholeNumber = self.actual_font_size.getValueInt()
        if self.__lastWholeNumber is None:
            self.__lastWholeNumber = curWholeNumber
        else:
            if curWholeNumber != self.__lastWholeNumber:
                self.actual_font_size.pulseToValue(target_value=curWholeNumber + self.animation_extra_font_size.getValue(), duration=3)

        CanvasUtils.drawTextAt(painter=painter,
                               data=self.data,
                               raw_pos=(self.x.getValue(), self.y.getValue()),
                               text=self.text,
                               color=ColorTools.apply_opacity_to_color(self.text_color.getValue(), self.text_opacity.getValue()),
                               font_size=self.actual_font_size.getValueInt(),
                               scaleFont=True)

    def updatePhysics(self):
        pass

    def updateGraphics(self, painter):
        self.drawMyself(painter)
