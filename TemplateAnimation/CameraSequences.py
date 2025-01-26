from PyQt6.QtGui import QColor


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

    def initial_operations(self):
        self.data.navigation.globalPositionData.position = (0, 0)
        self.data.navigation.globalPositionData.scale = 1

    def init_sequences(self):
        self.sequences = (
            lambda: self.data.cameraMovement.smoothMoveTo(targetX=0, targetY=0, targetScale=5, duration=5),
        )
