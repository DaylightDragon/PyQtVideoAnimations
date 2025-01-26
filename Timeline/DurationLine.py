from PyQt6.QtGui import QColor

from Shared import CanvasUtils
from Shared.ColorInterpolator import ColorInterpolator


class DurationLine:
    height = 2

    def __init__(self, data, start, end, text, lineId):
        self.data = data
        self.start = start
        if isinstance(start, str):
            self.start = self.data.simulation.getEventById(start).position
        self.end = end
        if isinstance(end, str):
            self.end = self.data.simulation.getEventById(end).position
        self.text = text
        self.lineId = lineId

        self.lineColor = ColorInterpolator(defaultColor=QColor.fromRgb(170, 170, 170))
        self.textColor = ColorInterpolator(defaultColor=QColor.fromRgb(255, 255, 255))

    arrow_base_side_size = 4
    arrow_long_side_size = 5

    arrow_offset_inwards = 3
    line_offset_inwards = 5

    def drawMyself(self, painter):
        center_x = self.start + (self.end - self.start) / 2
        CanvasUtils.drawRectAtCenter(painter=painter, data=self.data, raw_pos=(center_x, self.data.visualSizes.durationLineGeneralOffset.getValue()),
                                     size=(self.end - self.start - self.line_offset_inwards * 2, self.height), fill_color=self.lineColor.getValue(),
                                     keepHeight=False)

        CanvasUtils.drawArrowPointerAt(painter=painter, data=self.data,
                                       start_point_raw=(self.start + self.arrow_offset_inwards + self.line_offset_inwards, self.data.visualSizes.durationLineGeneralOffset.getValue()),
                                       angle_degrees=180, base_side_size=self.arrow_base_side_size, long_side_size=self.arrow_long_side_size, color=self.lineColor.getValue(),
                                       outlineColor=self.lineColor.getValue(), outlineWidth=2)
        CanvasUtils.drawArrowPointerAt(painter=painter, data=self.data,
                                       start_point_raw=(self.end - self.arrow_offset_inwards - self.line_offset_inwards, self.data.visualSizes.durationLineGeneralOffset.getValue()),
                                       angle_degrees=0, base_side_size=self.arrow_base_side_size, long_side_size=self.arrow_long_side_size, color=self.lineColor.getValue(),
                                       outlineColor=self.lineColor.getValue(), outlineWidth=2)

        offset_scaled = int(pow(self.data.navigation.globalPositionData.scale, 0.2) * self.data.visualSizes.durationLineTextOffset.getValue())
        CanvasUtils.drawTextAt(painter=painter, data=self.data,
                               raw_pos=(center_x, self.data.visualSizes.durationLineGeneralOffset.getValue() + offset_scaled), text=self.text,
                               color=self.textColor.getValue(), font_size=10, scaleFont=True)

    def updatePhysics(self):
        pass

    def updateGraphics(self, painter):
        self.drawMyself(painter)

    smoothColorStartTime = None
    smoothColorTarget = None
    smoothColorDuration = None
    smoothColorRealDuration = None
    smoothColorEasing = None
    alreadyBack = False
    realDurationCoef = None

    def pulseLineColor(self, target_color, duration, easingFunction=lambda t: t, realDurationCoef=1):
        self.lineColor.pulseToValue(target_color=target_color, duration=duration, easingFunction=easingFunction, realDurationCoef=realDurationCoef)

    def pulseTextColor(self, target_color, duration, easingFunction=lambda t: t, realDurationCoef=1):
        self.textColor.pulseToValue(target_color=target_color, duration=duration, easingFunction=easingFunction, realDurationCoef=realDurationCoef)
