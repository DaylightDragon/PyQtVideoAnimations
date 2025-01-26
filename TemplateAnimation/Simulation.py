from Shared.CameraMovement import CameraMovement
from TemplateAnimation.CameraSequences import CameraSequences

class Simulation:
    def __init__(self, data):
        self.data = data
        self.data.simulation = self
        self.loadData()
        self.data.cameraMovement = CameraMovement(data)
        self.data.cameraSequences = CameraSequences(data)

    def loadData(self):
        pass
        # with open('data.json', 'r', encoding='utf-8') as file:
        #     timelineData = json.load(file)
        #     for event in timelineData['events']:
        #         self.createEvent(event)
        #     for event in timelineData['durations']:
        #         self.createDurationLine(event)


    # def createEvent(self, eventData):
    #     event = TimelineEvent(data=self.data,
    #                           position=eventData['position'],
    #                           label=eventData['label'],
    #                           eventId=eventData['id'] if 'id' in eventData.keys() else None
    #                           )
    #     self.events.append(event)


    def resetEverything(self):
        pass


    def updatePhysics(self):
        pass

    def updateGraphics(self, painter):
        pass
