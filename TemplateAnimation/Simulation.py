from Shared.CameraMovement import CameraMovement
from TemplateAnimation.CameraSequences import CameraSequences

class Simulation:
    def __init__(self, data):
        self.data = data
        self.data.simulation = self
        self.something = []
        self.loadData()

        self.data.cameraMovement = CameraMovement(data)
        self.data.cameraSequences = CameraSequences(data)

    # def getSomethingById(self, instanceId):
    #     for instance in self.something:
    #         if instance.instanceId == instanceId:
    #             return instance

    def loadData(self):
        pass

    def resetEverything(self):
        pass


    def updatePhysics(self):
        pass

    def updateGraphics(self, painter):
        pass
        # for something in self.texts:
        #     something.updateGraphics(painter)
