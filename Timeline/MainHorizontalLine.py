from PyQt6.QtGui import QColor

from Shared import CanvasUtils


class MainHorizontalLine:
    width = 10000
    height = 10

    def __init__(self, data):
        self.data = data

    def drawMyself(self, painter):
        CanvasUtils.drawRectAtCenter(painter=painter, data=self.data, raw_pos=(0, 0), size=(self.width, self.height), fill_color=QColor.fromRgb(255, 255, 255), keepHeight=True)

    def updatePhysics(self):
        pass

    def updateGraphics(self, painter):
        self.drawMyself(painter)
