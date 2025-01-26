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
