import json

from Shared.CameraMovement import CameraMovement
from CameraSequences import CameraSequences
from TimelineEvent import TimelineEvent
from MainHorizontalLine import MainHorizontalLine
from DurationLine import DurationLine


class Timeline:
    def __init__(self, data):
        self.data = data
        self.data.simulation = self
        self.horizontalLine = MainHorizontalLine(self.data)
        self.events = []
        self.durationLines = []
        self.loadTimelineData()
        self.data.cameraMovement = CameraMovement(data)
        self.data.cameraSequences = CameraSequences(data)

    def getEventById(self, eventId):
        for event in self.events:
            if event.eventId == eventId:
                return event

    def getDurationLineById(self, durationLineId):
        for durationLine in self.durationLines:
            if durationLine.lineId == durationLineId:
                return durationLine

    def loadTimelineData(self):
        with open('data.json', 'r', encoding='utf-8') as file:
            timelineData = json.load(file)
            for event in timelineData['events']:
                self.createEvent(event)
            for event in timelineData['durations']:
                self.createDurationLine(event)

    def createEvent(self, eventData):
        event = TimelineEvent(data=self.data,
                              position=eventData['position'],
                              label=eventData['label'],
                              eventId=eventData['id'] if 'id' in eventData.keys() else None
                              )
        self.events.append(event)

    def createDurationLine(self, durationData):
        durationLine = DurationLine(data=self.data,
                                    start=durationData['start'],
                                    end=durationData['end'],
                                    text=durationData['text'],
                                    lineId=durationData['id'] if 'id' in durationData.keys() else None
                                    )
        self.durationLines.append(durationLine)

    def resetEverything(self):
        pass

    def updatePhysics(self):
        self.horizontalLine.updatePhysics()
        for event in self.events:
            event.updatePhysics()
        for line in self.durationLines:
            line.updatePhysics()

    def updateGraphics(self, painter):
        self.horizontalLine.updateGraphics(painter)
        for event in self.events:
            event.updateGraphics(painter)
        for line in self.durationLines:
            line.updateGraphics(painter)
