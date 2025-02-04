from PyQt6.QtGui import QColor

from Shared import CanvasUtils, ColorTools, Easings
from Shared.ValueInterpolator import ValueInterpolator
from Shared.ColorInterpolator import ColorInterpolator


class NumberText:
    def __init__(self, data, instanceId):
        self.data = data
        self.instanceId = instanceId

        self.x = ValueInterpolator(-200)
        self.y = ValueInterpolator(-100)

        self.text_color = ColorInterpolator(QColor.fromRgb(200, 200, 200))
        self.text_opacity = ValueInterpolator(1.0)
        self.font_size = ValueInterpolator(12)

        self.outline_color = ColorInterpolator(QColor.fromRgb(50, 50, 50))
        self.outline_opacity = ValueInterpolator(1.0)
        self.outline_width = ValueInterpolator(2)

        self.animation_extra_font_size = ValueInterpolator(10)

        self.actual_font_size = ValueInterpolator(self.font_size.getValue())
        # self.actual_font_size.setCustomInternalGetFunc(lambda: self.font_size.getValue())

        self.value = ValueInterpolator(0)
        self.__lastWholeNumber = None
        self.onValueChange = None
        self.customFormatFunc = None

    def setFontSize(self, font_size):
        self.font_size.setValue(font_size)
        self.actual_font_size.setValue(font_size)

    def setOnValueChange(self, func):
        self.onValueChange = func

    def setCustomFormatFunc(self, func):
        self.customFormatFunc = func

    def formatNumber(self, n) -> str:
        s = str(int(n))

        parts = []
        while s:
            parts.append(s[-3:])
            s = s[:-3]

        return ' '.join(reversed(parts))

    def drawMyself(self, painter):
        curWholeNumber = self.value.getValueInt()
        if self.__lastWholeNumber is None:
            self.__lastWholeNumber = curWholeNumber
        else:
            if curWholeNumber != self.__lastWholeNumber:
                self.__lastWholeNumber = curWholeNumber
                if self.onValueChange is not None:
                    self.onValueChange(self.__lastWholeNumber, curWholeNumber)
                self.actual_font_size.stop()
                self.actual_font_size.setValue(self.font_size.getValue())
                self.actual_font_size.pulseOutOfValue(target_value=self.font_size.getValue() + self.animation_extra_font_size.getValue(),
                                                      duration=30,
                                                      easingFunction=Easings.easeOutExpo)

        formattedNumber = self.formatNumber(self.value.getValueInt())
        final_text = formattedNumber
        if self.customFormatFunc is not None:
            final_text = self.customFormatFunc(self.value, formattedNumber)

        CanvasUtils.drawTextAt(painter=painter,
                               data=self.data,
                               raw_pos=(self.x.getValue(), self.y.getValue()),
                               text=final_text,
                               color=ColorTools.apply_opacity_to_color(self.text_color.getValue(), self.text_opacity.getValue()),
                               font_size=self.actual_font_size.getValue(),
                               outline=True,
                               outline_color=ColorTools.apply_opacity_to_color(self.outline_color.getValue(), self.outline_opacity.getValue()),
                               outline_width=self.outline_width.getValue(),
                               scaleFont=True,
                               offsetSize=60)

    def updatePhysics(self):
        pass

    def updateGraphics(self, painter):
        self.drawMyself(painter)
