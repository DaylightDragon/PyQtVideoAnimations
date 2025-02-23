from PyQt6.QtGui import QColor

from Shared import Easings
from Shared.NumberText import NumberText


class CameraSequences:
    sequences = None
    index = -1

    def __init__(self, data):
        self.data = data

        self.init_sequences()
        self.initial_operations()

    def __decrease_index(self):
        self.index = self.index - 1
        if self.index < 0:
            self.index = -1

    def __increase_index(self):
        self.index = self.index + 1
        if self.index >= len(self.sequences):
            self.index = len(self.sequences)

    def perform_next_sequence(self):
        self.__increase_index()
        if self.index >= len(self.sequences):
            return
        sequence = self.sequences[self.index]
        sequence()

    def perform_prev_sequence(self):
        self.__decrease_index()
        sequence = self.sequences[self.index]
        sequence()

    small_scale = 10
    # big_scale = small_scale * 1.2

    def onNewValue(self, oldValue, newValue):
        pass
        # self.data.navigation.globalPositionData.scale = self.big_scale
        # self.data.cameraMovement.smoothMoveTo(targetX=self.data.navigation.globalPositionData.position[0],
        #                                       targetY=self.data.navigation.globalPositionData.position[1],
        #                                       targetScale=self.small_scale, duration=30,
        #                                       easingFunction=Easings.easeOutExpo
        #                                       )

    def mainTextFormatFuncAccs(self, value, formattedNumber):
        return (f'Аккаунтов: {formattedNumber}')

    def initial_operations(self):
        self.data.navigation.globalPositionData.position = (0, 0)
        self.data.navigation.globalPositionData.scale = self.small_scale
        self.data.navigation.zoom_value = 1

        mainText: NumberText = self.data.simulation.getTextById('mainText')
        mainText.x.setValue(0)
        mainText.y.setValue(0)
        mainText.setFontSize(20)
        mainText.setOnValueChange(self.onNewValue)
        mainText.setCustomFormatFunc(self.mainTextFormatFuncAccs)
        mainText.value.instanceId = 'mainNum'
        mainText.font_size.instanceId = 'mainNum font_size'
        mainText.actual_font_size.instanceId = 'mainNum actual_font_size'
        mainText.outline_width.setValue(15)
        mainText.outline_color.setValue(QColor.fromRgb(60, 60, 60))

        mainText.animation_extra_font_size.setValue(3)
        mainText.value.setValue(8)

    def increaseNumber0_1(self):
        mainText: NumberText = self.data.simulation.getTextById('mainText')
        mainText.value.fadeToValue(target_value=12.5, duration=1, easingFunction=Easings.easeOutQuint, realDurationCoef=0.9)

    def increaseNumber0_2(self):
        mainText: NumberText = self.data.simulation.getTextById('mainText')
        mainText.value.fadeToValue(target_value=8, duration=1, easingFunction=Easings.easeOutQuint, realDurationCoef=0.9)

    def increaseNumber1(self):
        mainText: NumberText = self.data.simulation.getTextById('mainText')
        mainText.value.fadeToValue(target_value=400000, duration=600, easingFunction=Easings.easeOutQuint, realDurationCoef=0.0012)

    def increaseNumber2(self):
        mainText: NumberText = self.data.simulation.getTextById('mainText')
        mainText.value.fadeToValue(target_value=700000, duration=600, easingFunction=Easings.easeOutQuint, realDurationCoef=0.0012)

    def init_sequences(self):
        self.sequences = (
            # lambda: self.data.cameraMovement.smoothMoveTo(targetX=0, targetY=0, targetScale=5, duration=5),
            self.increaseNumber0_1,
            self.increaseNumber0_2,
            # self.increaseNumber1,
            # self.increaseNumber2,
        )
