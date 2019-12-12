from Constants import *

class Magic:
    def __init__(self, func):
        self.func = func

    def run(self):
        self.func()  


class Effect:
    def __init__(self, duration, function):
        self.duration = duration
        self.function = function

    def set_duration(self, duration):
        self.duration = duration

    def is_active(self):
        if self.duration > 0:
            return True
        return False

    def run(self, obj):
        self.function(obj)
        self.duration -= 1

        if self.duration <= 0:
            self.function = DEF_NULL
