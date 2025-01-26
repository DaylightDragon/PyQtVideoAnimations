from Shared.CameraMovement import CameraMovement
from WindowsAnim.CameraSequences import CameraSequences
from Shared.WindowRect import WindowRect


class Simulation:
    def __init__(self, data):
        self.data = data
        self.data.simulation = self
        self.rects = []
        self.loadData()

        self.data.cameraMovement = CameraMovement(data)
        self.data.cameraSequences = CameraSequences(data)

    def getRectById(self, instanceId):
        for rect in self.rects:
            if rect.instanceId == instanceId:
                return rect

    def toFront(self, rect):
        if rect in self.rects:
            self.rects.remove(rect)
            self.rects.append(rect)

    def loadData(self):
        self.rects.append(WindowRect(self.data, "rect1"))
        self.rects.append(WindowRect(self.data, "rect1_2"))

        self.rects.append(WindowRect(self.data, "rect2"))
        self.rects.append(WindowRect(self.data, "rect3"))
        self.rects.append(WindowRect(self.data, "rect4"))

    def resetEverything(self):
        pass

    def updatePhysics(self):
        pass

    def updateGraphics(self, painter):
        for rect in self.rects:
            rect.updateGraphics(painter)
