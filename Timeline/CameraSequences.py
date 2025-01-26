from lib2to3.fixes.fix_tuple_params import simplify_args
from wsgiref.simple_server import server_version

from PyQt6.QtGui import QColor

from Shared import Easings

RED_FLASH = QColor.fromRgb(200, 80, 80)

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

    def hideEvent(self, event):
        event.text_opacity.fadeToValue(target_value=0, duration=0)
        event.line_opacity.fadeToValue(target_value=0, duration=0)

    def initial_operations(self):
        keruku = self.data.simulation.getEventById("keruku")
        sigmatox = self.data.simulation.getEventById("sigmatox")
        etheralotus = self.data.simulation.getEventById("etheralotus")

        self.hideEvent(keruku)
        self.hideEvent(sigmatox)
        self.hideEvent(etheralotus)

        keruku.font_size.fadeToValue(target_value=7, duration=0)
        sigmatox.font_size.fadeToValue(target_value=7, duration=0)

    # INSTRUCTIONS          INSTRUCTIONS          INSTRUCTIONS          INSTRUCTIONS          INSTRUCTIONS

    def diveIntoCurrent(self, duration=10):
        self.data.cameraMovement.smoothMoveTo(targetX=self.data.cameraMovement.getX(), targetY=-15, targetScale=100, duration=duration, easingFunction=Easings.easeInExpo)

    def diveIntoCurrentInstant(self):
        self.diveIntoCurrent(0)

    def focusOnAfterAer(self):
        self.data.cameraMovement.smoothMoveTo(targetX=-200, targetScale=4, duration=5)
        self.data.visualSizes.durationLineGeneralOffset.fadeToValue(target_value=-50, duration=5)

    def flashOnStartAndGettingAer(self):
        start = self.data.simulation.getEventById("cosStart")
        gettingAer = self.data.simulation.getEventById("gettingAer")

        self.data.visualSizes.durationLineGeneralOffset.fadeToValue(target_value=-30, duration=5)
        self.data.cameraMovement.smoothMoveTo(targetX=start.position + (gettingAer.position - start.position)/2, targetScale=5, duration=5)
        start.text_color.pulseToValue(target_color=RED_FLASH, duration=3, start_delay=5 * 0.2)
        gettingAer.text_color.pulseToValue(target_color=RED_FLASH, duration=3, start_delay=7 * 0.2)

    def focusAndFlashOnAerVid(self):
        aerVid = self.data.simulation.getEventById("aerVideo")
        self.data.cameraMovement.smoothMoveTo(targetX=aerVid.position, targetScale=5, duration=8)
        aerVid.text_color.pulseToValue(target_color=RED_FLASH, duration=3, start_delay=6 * 0.2)

    def focusBetweenGettingAerAndAerVid(self):
        gettingAer = self.data.simulation.getEventById("gettingAer")
        aerVid = self.data.simulation.getEventById("aerVideo")
        self.data.cameraMovement.smoothMoveTo(targetX=gettingAer.position + (aerVid.position - gettingAer.position)/2, targetScale=5, duration=7)
        # aerVid.text_color.pulseToColor(target_color=RED_FLASH, duration=3, start_delay=6 * 0.2)

    def flashOnBeforeAerVidDurationLine(self):
        BeforeAerVidDL = self.data.simulation.getDurationLineById("BeforeAerVidDL")
        BeforeAerVidDL.textColor.pulseToValue(target_color=RED_FLASH, duration=7, start_delay=2 * 0.2)
        BeforeAerVidDL.lineColor.pulseToValue(target_color=RED_FLASH, duration=7)

    # KER SIGMA       KER SIGMA       KER SIGMA       KER SIGMA       KER SIGMA       KER SIGMA       KER SIGMA

    def focusOnBeginningTillAerVid(self):
        self.data.cameraMovement.smoothMoveTo(targetX=-200, targetY=0, targetScale=5, duration=5)

    def focusOnBeginningTillAerVidInstant(self):
        self.data.cameraMovement.smoothMoveTo(targetX=-100, targetY=0, targetScale=5, duration=0)

    def flashOnGettingAer(self):
        gettingAer = self.data.simulation.getEventById("gettingAer")
        gettingAer.text_color.pulseToValue(target_color=QColor.fromRgb(200, 80, 80), duration=3)

    def flashOnAerVid(self):
        aerVid = self.data.simulation.getEventById("aerVideo")
        aerVid.text_color.pulseToValue(target_color=QColor.fromRgb(200, 80, 80), duration=4, start_delay=5 * 0.2)
        self.data.cameraMovement.smoothMoveTo(targetX=aerVid.position - 30, targetY=0, targetScale=7, duration=5),
        self.data.visualSizes.durationLineGeneralOffset.fadeToValue(target_value=-50, duration=5)

    def revealSecretEventsBetween(self):
        keruku = self.data.simulation.getEventById("keruku")
        sigmatox = self.data.simulation.getEventById("sigmatox")
        gettingAer = self.data.simulation.getEventById("gettingAer")
        aerVid = self.data.simulation.getEventById("aerVideo")

        keruku.label = "???"
        sigmatox.label = "???"

        self.data.visualSizes.durationLineGeneralOffset.fadeToValue(target_value=-50, duration=5)
        gettingAer.text_opacity.fadeToValue(target_value=0, duration=3)
        aerVid.text_opacity.fadeToValue(target_value=0, duration=3)

        gettingAer.lockTextScale()
        aerVid.lockTextScale()

        gettingAer.font_size.fadeToValue(target_value=8, duration=7)
        aerVid.font_size.fadeToValue(target_value=8, duration=7)

        keruku.text_opacity.fadeToValue(target_value=1.0, duration=7, start_delay=2 * 0.2)
        keruku.line_opacity.fadeToValue(target_value=1.0, duration=7, start_delay=2 * 0.2)

        sigmatox.text_opacity.fadeToValue(target_value=1.0, duration=7, start_delay=4 * 0.2)
        sigmatox.line_opacity.fadeToValue(target_value=1.0, duration=7, start_delay=4 * 0.2)

        self.data.visualSizes.eventTextOffset.fadeToValue(target_value=10, duration=5)
        self.data.visualSizes.durationLineGeneralOffset.fadeToValue(target_value=-20, duration=5)
        self.data.cameraMovement.smoothMoveTo(targetX=-150, targetY=0, targetScale=8, duration=6),

    def focusOnSecretKeruku(self):
        keruku = self.data.simulation.getEventById("keruku")
        self.data.cameraMovement.smoothMoveTo(targetX=keruku.position, targetY=0, targetScale=10, duration=6)

    def revealKeruku(self):
        keruku = self.data.simulation.getEventById("keruku")
        keruku.text_opacity.setValue(0, stop=True)
        keruku.text_opacity.fadeToValue(target_value=1, duration=5)
        keruku.label = 'Получение\nКеруку'
        # keruku.text_color.pulseOutOfColor(target_color=QColor.fromRgb(255, 80, 80), duration=5)

    def focusOnSecretSigmatox(self):
        sigmatox = self.data.simulation.getEventById("sigmatox")
        sigmatox.text_opacity.fadeToValue(target_value=1.0, duration=7)
        sigmatox.line_opacity.fadeToValue(target_value=1.0, duration=7)
        self.data.cameraMovement.smoothMoveTo(targetX=sigmatox.position, targetY=0, targetScale=10, duration=6)

    def revealSecretSigmatox(self):
        sigmatox = self.data.simulation.getEventById("sigmatox")
        sigmatox.label = 'Получение\nСигматокса'
        sigmatox.text_opacity.setValue(0, stop=True)
        sigmatox.text_opacity.fadeToValue(target_value=1, duration=5)
        # sigmatox.text_color.pulseOutOfColor(target_color=QColor.fromRgb(255, 80, 80), duration=5)

    # MAIN          MAIN          MAIN          MAIN          MAIN          MAIN          MAIN          MAIN

    def afterAerSequence(self):
        return (
            lambda: (self.focusOnBeginningTillAerVidInstant(), self.diveIntoCurrentInstant()),
            self.focusOnAfterAer,
            self.flashOnStartAndGettingAer,
            self.focusAndFlashOnAerVid,
            self.focusBetweenGettingAerAndAerVid,
            self.flashOnBeforeAerVidDurationLine,
            self.diveIntoCurrent
        )

    def kerSigmaSequence(self):
        return (
            self.focusOnBeginningTillAerVid,
            self.flashOnGettingAer,
            self.flashOnAerVid,
            self.revealSecretEventsBetween,
            self.focusOnSecretKeruku,
            self.revealKeruku,
            self.diveIntoCurrent,
            self.focusOnSecretKeruku,
            self.focusOnSecretSigmatox,
            self.revealSecretSigmatox,
            self.diveIntoCurrent,
        )

    def init_sequences(self):
        self.sequences = (
            *self.afterAerSequence(),
            *self.kerSigmaSequence(),
            lambda: self.data.cameraMovement.smoothMoveTo(targetX=-100, targetY=0, targetScale=3, duration=5)
        )
