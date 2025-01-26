from PyQt6.QtGui import QPainter

from Shared import Links
from Shared.FrameUpdater import FrameUpdater
from Shared.ValueInterpolator import ValueInterpolator


class VisualSizes:
    def __init__(self):
        self.eventHeight = ValueInterpolator(50)
        self.eventTextOffset = ValueInterpolator(20)
        self.durationLineGeneralOffset = ValueInterpolator(-50)
        self.durationLineTextOffset = ValueInterpolator(-10)


class Data:
    canvas = None
    navigation = None
    simulation = None
    cameraMovement = None
    cameraSequences = None
    deltaTime = None
    debug = False
    hideUi = True
    renderWindowSize: tuple[int, int] = None
    mainUi = None
    uis = []
    movementListeners = []

    mouseSensitivity = 1
    scrollSensitivity = 1

    globalData = None

    def __init__(self, fps: int, size: tuple[int, int]):
        self.animated = []
        self.fps = fps
        self.frameUpdater = FrameUpdater(self)
        self.renderWindowSize = size
        self.timeScale = 3

        Links.init(self)
        self.visualSizes = VisualSizes()
