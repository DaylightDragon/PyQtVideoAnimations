from PyQt6.QtGui import QColor

from Shared import CanvasUtils, ColorTools
from Shared.ValueInterpolator import ValueInterpolator
from Shared.ColorInterpolator import ColorInterpolator


class TimelineEvent:
    width = 15

    def __init__(self, data, position, label, eventId):
        self.data = data
        self.position = position
        self.label = label
        self.eventId = eventId
        self.text_color = ColorInterpolator(defaultColor=QColor.fromRgb(200, 200, 200))
        self.text_opacity = ValueInterpolator(defaultValue=1.0)
        self.font_size = ValueInterpolator(defaultValue=14)
        self.line_opacity = ValueInterpolator(defaultValue=1.0)
        self.noDynamicTextScale = False
        self.lastDynamicTextScaleValue = 0

    def lockTextScale(self):
        self.noDynamicTextScale = True
        self.lastDynamicTextScaleValue = CanvasUtils.getAutoScaledFontSize(data=self.data, font_size=self.font_size.getValue())

    def unlockTextScale(self):
        self.noDynamicTextScale = False

    def drawMyself(self, painter):
        CanvasUtils.drawRectAtCenter(painter=painter, data=self.data, raw_pos=(self.position, 0), size=(self.width, self.data.visualSizes.eventHeight.getValue()), fill_color=ColorTools.apply_opacity_to_color(self.text_color.getValue(), self.line_opacity.getValue()), keepWidth=True, keepHeight=True)
        offset_scaled = int(pow(self.data.navigation.globalPositionData.scale, 0.2) * self.data.visualSizes.eventTextOffset.getValue())
        CanvasUtils.drawTextAt(painter=painter, data=self.data, raw_pos=(self.position, offset_scaled), text=self.label, color=ColorTools.apply_opacity_to_color(self.text_color.getValue(), self.text_opacity.getValue()), scaleFont=not self.noDynamicTextScale,
                               font_size=(self.font_size.getValueInt() if not self.noDynamicTextScale else self.lastDynamicTextScaleValue))

    def updatePhysics(self):
        pass

    def updateGraphics(self, painter):
        self.drawMyself(painter)
