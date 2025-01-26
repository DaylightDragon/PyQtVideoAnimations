import time

from PyQt6.QtGui import QColor

from Shared import Easings, Links
from Shared.Data import Data


class ColorInterpolator:
    def __init__(self, defaultColor):
        Links.globalData.animated.append(self)
        self.defaultColor = defaultColor
        self.color = defaultColor

        self.smoothColorStartTime = None
        self.smoothColorTarget = None
        self.smoothColorDuration = None
        self.smoothColorRealDuration = None
        self.smoothColorEasing = None
        self.alreadyBack = False
        self.twoWayAnimation = False
        self.realDurationCoef = None
        self.start_delay = 0

    def getValue(self):
        return self.color

    def setValue(self, color, stop=False):
        self.color = color
        if stop:
            self.stop()

    def stop(self):
        self.smoothColorStartTime = None

    def __start_animation(self, target_color, duration, start_delay, easingFunction, realDurationCoef):
        self.start_delay = start_delay
        self.smoothColorStartTime = time.time()
        self.smoothColorTarget = target_color

        self.smoothColorDuration = duration
        self.smoothColorRealDuration = duration * min(1.0, realDurationCoef)
        self.realDurationCoef = realDurationCoef

        self.smoothColorEasing = easingFunction

    def pulseToValue(self, target_color, duration, start_delay=0, easingFunction=Easings.easeInOutQuad, realDurationCoef=0.2, alreadyBack=False):
        duration = duration / 2
        self.alreadyBack = alreadyBack
        self.twoWayAnimation = True

        self.__start_animation(target_color=target_color, duration=duration, start_delay=start_delay, easingFunction=easingFunction, realDurationCoef=realDurationCoef)

    def pulseOutOfValue(self, target_color, duration, start_delay=0, easingFunction=Easings.easeInOutQuad, realDurationCoef=0.2):
        color1 = QColor(target_color)
        color2 = QColor(self.color)
        self.color = color1
        self.fadeToValue(target_color=color2, duration=duration, start_delay=start_delay, easingFunction=easingFunction, realDurationCoef=realDurationCoef)

    def fadeToValue(self, target_color, duration, start_delay=0, easingFunction=Easings.easeInOutQuad, realDurationCoef=0.2):
        self.alreadyBack = False
        self.twoWayAnimation = False

        self.__start_animation(target_color=target_color, duration=duration, start_delay=start_delay, easingFunction=easingFunction, realDurationCoef=realDurationCoef)

    def animate(self):
        if self.smoothColorStartTime is not None:
            elapsedTime = time.time() - self.smoothColorStartTime - self.start_delay

            if elapsedTime < 0:
                return

            # print('Upd', '{0:.2f}'.format(elapsedTime), "/", '{0:.2f}'.format(self.smoothColorRealDuration))
            if elapsedTime >= self.smoothColorRealDuration:
                self.color = self.smoothColorTarget
                if self.alreadyBack or not self.twoWayAnimation:
                    self.smoothColorStartTime = None
                else:
                    self.pulseToValue(target_color=self.defaultColor, duration=self.smoothColorDuration * 2, realDurationCoef=self.realDurationCoef, easingFunction=self.smoothColorEasing, alreadyBack=True)
            else:
                t = min(1.0, elapsedTime / self.smoothColorDuration)  # Нормализация времени
                t = self.smoothColorEasing(t)  # Применение easing функции

                r1, g1, b1, a1 = self.color.getRgb()
                r2, g2, b2, a2 = self.smoothColorTarget.getRgb()

                new_r = int(r1 + (r2 - r1) * t)
                new_g = int(g1 + (g2 - g1) * t)
                new_b = int(b1 + (b2 - b1) * t)
                new_a = int(a1 + (a2 - a1) * t)

                self.color = QColor(new_r, new_g, new_b, new_a)
