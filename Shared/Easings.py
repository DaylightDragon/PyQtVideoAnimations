def easeInOutCubic(t):
    return t * t * t if t < 0.5 else (t - 1) * (t - 1) * (t - 1) + 1

# 1. Квадратичное (Quadratic)

def easeInQuad(t):
    return t*t

def easeOutQuad(t):
    return -(t)*(t-2)

def easeInOutQuad(t):
    return t*t if t < 0.5 else -((2*t)-3)*((2*t)-1) #  или как вариант t * (2-t)


#2. Кубическое (Cubic)

def easeInCubic(t):
    return t*t*t

def easeOutCubic(t):
  return ((t-1)**3)+1

# def easeInOutCubic(t):
#     return 4*t*t*t if t < 0.5 else ((2*t-2)**3) + 2


#3. Квартическое (Quartic)

def easeInQuart(t):
    return t*t*t*t

def easeOutQuart(t):
    return -(pow(t-1,4)) + 1

def easeInOutQuart(t):
    return 8*t*t*t*t if t < 0.5 else -8*(t-1)**4 + 1


#4. Квинтовое (Quintic):

def easeInQuint(t):
  return t**5

def easeOutQuint(t):
    return (t-1)**5 + 1

def easeInOutQuint(t):
    return 16*t**5 if t < 0.5 else (2*t-2)**5 + 2


#5. Синусоидальное (Sine):

import math

def easeInSine(t):
    return 1-math.cos((t*math.pi)/2)

def easeOutSine(t):
    return math.sin((t*math.pi)/2)

def easeInOutSine(t):
    return -(math.cos(math.pi*t)-1)/2


#6. Экспоненциальное (Exponential):
def easeInExpo(t):
    return 0 if t==0 else pow(2, 10 * (t - 1)) - 0.001

def easeOutExpo(t):
    return 1 if t==1 else 1 - pow(2, -10 * t)

def easeInOutExpo(t):
    if t == 0: return 0
    if t == 1: return 1
    return (pow(2, 20 * (t - 1)) - 0.001) / 2 if t < 0.5 else (2 - pow(2, -20 * t)) / 2


#7.  Обратное (Back):  Добавляет "overshoot" (перехлёст) в начале и конце.  s -  параметр, управляющий интенсивностью перехлёста (обычно от 1.70158 до 2.5).

def easeInOutBack(t, s=1.70158):
  return (t*t*((s+1)*t - s))/2 if t < 0.5 else (t-1)*(t-1)*((s+1)*(t-1) + s)/2 + 1


#8. Эластичное (Elastic):  Создает эффект "пружины".  a  - амплитуда, p - период.

def easeOutElastic(t, a=0.1, p=0.4):
  return 1 - pow(2, -10 * t) * math.sin((t - p / 4) * (2 * math.pi) / p) if t!=1 else 1

def easeInOutElastic(t, a=0.1, p=0.4):
    if t==0: return 0
    if t==1: return 1
    return -(pow(2,20*(t-1))*math.sin((t-1-(p/(4*math.pi)))*(2*math.pi)/p))/2 if t < 0.5 else (pow(2,-20*t)*math.sin((t-p/(4*math.pi))*(2*math.pi)/p))+1

