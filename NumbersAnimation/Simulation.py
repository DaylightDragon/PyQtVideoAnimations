from PyQt6.QtGui import QColor

from Shared import CanvasUtils
from Shared.CameraMovement import CameraMovement
from NumbersAnimation.CameraSequences import CameraSequences
from Shared.NumberText import NumberText


class Simulation:
    def __init__(self, data):
        self.data = data
        self.data.simulation = self
        self.texts = []

        self.loadData()
        self.data.cameraMovement = CameraMovement(data)
        self.data.cameraSequences = CameraSequences(data)

    def getTextById(self, instanceId):
        for instance in self.texts:
            if instance.instanceId == instanceId:
                return instance

    def loadData(self):
        self.texts.append(NumberText(data=self.data, instanceId="mainText"))

    def resetEverything(self):
        pass

    def updatePhysics(self):
        pass

    def updateGraphics(self, painter):
        for something in self.texts:
            something.updateGraphics(painter)
        if not self.data.hideUi:
            # CanvasUtils.drawLineAt(painter=painter,
            #                        data=self.data,
            #                        point1_raw=(self.data.renderWindowSize[0]/2 - 100, self.data.renderWindowSize[1]/2),
            #                        point2_raw=(self.data.renderWindowSize[0]/2 + 100, self.data.renderWindowSize[1]/2),
            #                        color=QColor.fromRgb(255, 255, 255),
            #                        width=2,
            #                        displaySpaceAlready=True)
            # CanvasUtils.drawLineAt(painter=painter,
            #                        data=self.data,
            #                        point1_raw=(self.data.renderWindowSize[0] / 2, self.data.renderWindowSize[1] / 2 - 100),
            #                        point2_raw=(self.data.renderWindowSize[0] / 2, self.data.renderWindowSize[1] / 2 + 100),
            #                        color=QColor.fromRgb(255, 255, 255),
            #                        width=2,
            #                        displaySpaceAlready=True)

            CanvasUtils.drawLineAt(painter=painter,
                                   data=self.data,
                                   point1_raw=(-100, 0),
                                   point2_raw=(+100, 0),
                                   color=QColor.fromRgb(255, 255, 255),
                                   width=2,
                                   displaySpaceAlready=False)
            CanvasUtils.drawLineAt(painter=painter,
                                   data=self.data,
                                   point1_raw=(0, -100),
                                   point2_raw=(0, +100),
                                   color=QColor.fromRgb(255, 255, 255),
                                   width=2,
                                   displaySpaceAlready=False)
