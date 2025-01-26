from PyQt6.QtGui import QColor

from Shared.WindowRect import WindowRect

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

    def setInvisibleInCenter(self, rect: WindowRect):
        rect.line_opacity.setValue(0)
        rect.width.setValue(1200)
        rect.height.setValue(800)
        rect.x.setValue(-rect.width.getValue() / 2)
        rect.y.setValue(-rect.height.getValue() / 2)

    def initial_operations(self):
        self.data.navigation.globalPositionData.position = (0, 0)
        self.data.navigation.globalPositionData.scale = 1

        rect1: WindowRect = self.data.simulation.getRectById("rect1")
        rect1_2: WindowRect = self.data.simulation.getRectById("rect1_2")

        rect2: WindowRect = self.data.simulation.getRectById("rect2")
        rect3: WindowRect = self.data.simulation.getRectById("rect3")
        rect4: WindowRect = self.data.simulation.getRectById("rect4")

        self.setInvisibleInCenter(rect1)
        self.setInvisibleInCenter(rect1_2)
        self.setInvisibleInCenter(rect2)
        self.setInvisibleInCenter(rect3)
        self.setInvisibleInCenter(rect4)

        rect1.text = 'Окно 1'
        rect2.text = 'Окно 2'
        rect3.text = 'Окно 3'
        rect4.text = 'Окно 4'

        initial_font_size = 100

        rect1.font_size.setValue(initial_font_size)
        rect1_2.font_size.setValue(initial_font_size)

        rect2.font_size.setValue(initial_font_size)
        rect3.font_size.setValue(initial_font_size)
        rect4.font_size.setValue(initial_font_size)

    def showRect(self, rect: WindowRect, start_delay=0.0, noFlash=False):
        rect.line_opacity.fadeToValue(target_value=1, duration=5, start_delay=start_delay)
        rect.text_opacity.fadeToValue(target_value=1.0, duration=5, start_delay=start_delay)
        if not noFlash:
            rect.line_color.pulseToValue(target_color=RED_FLASH, duration=5, start_delay=start_delay)

    def showFirstRect(self):
        rect1: WindowRect = self.data.simulation.getRectById("rect1")
        self.showRect(rect1)

    def moveToQuarter(self, rect: WindowRect, x, y, start_delay = 0.0, duration=5):
        rect.x.fadeToValue(target_value=x, duration=duration, start_delay=start_delay)
        rect.y.fadeToValue(target_value=y, duration=duration, start_delay=start_delay)
        rect.width.fadeToValue(target_value=1920 / 2, duration=duration, start_delay=start_delay)
        rect.height.fadeToValue(target_value=1080 / 2, duration=duration, start_delay=start_delay)

    def moveFirstRectToCorner(self):
        rect1: WindowRect = self.data.simulation.getRectById("rect1")
        self.moveToQuarter(rect1, x=-1920 / 2, y=-1080 / 2)

    def showOther3AndMoveToCorners(self):
        rect2: WindowRect = self.data.simulation.getRectById("rect2")
        rect3: WindowRect = self.data.simulation.getRectById("rect3")
        rect4: WindowRect = self.data.simulation.getRectById("rect4")

        delay = 1

        self.showRect(rect2)
        self.showRect(rect3, start_delay=delay * 0.2)
        self.showRect(rect4, start_delay=2 * delay * 0.2)

        self.moveToQuarter(rect2, x=0, y=-1080 / 2)
        self.moveToQuarter(rect3, x=-1920 / 2, y=0, start_delay=delay * 0.2)
        self.moveToQuarter(rect4, x=0, y=0, start_delay=2 * delay * 0.2)

    def prepareForShift(self):
        rect1: WindowRect = self.data.simulation.getRectById("rect1")
        rect1_2: WindowRect = self.data.simulation.getRectById("rect1_2")

        self.data.simulation.toFront(rect1)
        self.moveToQuarter(rect1_2, x=-1920 / 2, y=-1080 / 2, duration=0)
        # self.showRect(rect1_2)
        rect1.fill_color.fadeToValue(target_color=QColor.fromRgb(0, 0, 40, 240), duration=5)
        rect1.line_color.fadeToValue(target_color=QColor.fromRgb(80, 80, 200), duration=5)

        self.data.cameraMovement.smoothMoveByXY(dTargetX=-270, dTargetY=-180, targetScale=1.3, duration=5)

    def showShiftWindow(self):
        rect1: WindowRect = self.data.simulation.getRectById("rect1")
        rect1_2: WindowRect = self.data.simulation.getRectById("rect1_2")

        rect1_2.text = "Доп. окно"
        self.showRect(rect1_2)
        rect1_2.fill_color.fadeToValue(target_color=QColor.fromRgb(0, 40, 0, 240), duration=5)
        rect1_2.line_color.fadeToValue(target_color=QColor.fromRgb(80, 200, 80), duration=5)

        rect1_2.x.moveByValue(target_value=30, duration=5)
        rect1_2.y.moveByValue(target_value=-30, duration=5)

    def moveRectDiagBy(self, rect, byValue, duration=5):
        rect.x.moveByValue(target_value=byValue, duration=duration)
        rect.y.moveByValue(target_value=-byValue, duration=duration)

    shift_duration = 3

    def performShift1_part1(self):
        rect1: WindowRect = self.data.simulation.getRectById("rect1")
        rect1_2: WindowRect = self.data.simulation.getRectById("rect1_2")

        self.moveRectDiagBy(rect1, byValue=15, duration=self.shift_duration)
        self.moveRectDiagBy(rect1_2, byValue=-60, duration=self.shift_duration)

    def performShift1_part2(self):
        rect1: WindowRect = self.data.simulation.getRectById("rect1")
        rect1_2: WindowRect = self.data.simulation.getRectById("rect1_2")

        self.data.simulation.toFront(rect1_2)

        self.moveRectDiagBy(rect1, byValue=15, duration=self.shift_duration)
        self.moveRectDiagBy(rect1_2, byValue=30, duration=self.shift_duration)

    def performShift2_part1(self):
        rect1: WindowRect = self.data.simulation.getRectById("rect1")
        rect1_2: WindowRect = self.data.simulation.getRectById("rect1_2")

        self.moveRectDiagBy(rect1_2, byValue=15, duration=self.shift_duration)
        self.moveRectDiagBy(rect1, byValue=-60, duration=self.shift_duration)

    def performShift2_part2(self):
        rect1: WindowRect = self.data.simulation.getRectById("rect1")
        rect1_2: WindowRect = self.data.simulation.getRectById("rect1_2")

        self.data.simulation.toFront(rect1)

        self.moveRectDiagBy(rect1_2, byValue=15, duration=self.shift_duration)
        self.moveRectDiagBy(rect1, byValue=30, duration=self.shift_duration)

    def init_sequences(self):
        self.sequences = (
            self.showFirstRect,
            self.moveFirstRectToCorner,
            self.showOther3AndMoveToCorners,

            self.prepareForShift,
            self.showShiftWindow,
            self.performShift1_part1,
            self.performShift1_part2,
            self.performShift2_part1,
            self.performShift2_part2,
        )
