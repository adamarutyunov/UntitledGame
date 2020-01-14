from Constants import *


class Magic:
    def __init__(self, func):
        self.func = func

    def run(self):
        self.func()  


class Effect:
    def __init__(self, duration, mid_function,
                 start_function=lambda _: None,
                 end_function=lambda _: None):

        self.duration = duration
        self.basic_duration = duration

        self.start_function = start_function
        self.mid_function = mid_function
        self.end_function = end_function

        self.title = ""
        self.description = ""

        self.icon = None

    def set_duration(self, duration):
        self.duration = duration

    def is_active(self):
        if self.duration != 0:
            return True
        return False

    def run(self, obj):
        if self.duration == self.basic_duration:
            self.start_function(obj)
        
        self.mid_function(obj)
        self.duration -= 1

        if self.duration == 0:
            self.end_function(obj)
            self.function = DEF_NULL

    def copy(self):
        return Effect(self.duration, self.mid_function,
                      self.start_function, self.end_function)

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_description(self, description):
        self.description = description

    def get_description(self, description):
        return self.description

    def load_icon(self, icon):
        self.icon = icon

    def get_icon(self):
        return self.icon


class IncreaseHealthEffect:
    def __init__(self, duration, value):
        self.set_description(f"Повышение здоровья на {value} на {duration / FPS} секунд")
        self.value = value
        
        super().__init__(duration, self.mid_function)

    def mid_function(self, obj):
        obj.change_health(self.value)


class DecreaseHealthEffect:
    def __init__(self, duration, value):
        self.set_description(f"Снижение здоровья на {value} на {duration / FPS} секунд")
        self.value = value
        
        super().__init__(duration, self.mid_function)

    def mid_function(self, obj):
        obj.change_health(-self.value)


class IncreaseManaEffect:
    def __init__(self, duration, value):
        self.set_description(f"Повышение магии на {value} на {duration / FPS} секунд")
        self.value = value
        
        super().__init__(duration, self.mid_function)

    def mid_function(self, obj):
        obj.change_mana(self.value)


class DecreaseManaEffect:
    def __init__(self, duration, value):
        self.set_description(f"Снижение магии на {value} на {duration / FPS} секунд")
        self.value = value
        
        super().__init__(duration, self.mid_function)

    def mid_function(self, obj):
        obj.change_mana(-self.value)


class IncreaseIntelligenceEffect:
    def __init__(self, duration, value):
        self.set_description(f"Повышение интеллекта на {value} на {duration / FPS} секунд")
        self.value = value
        
        super().__init__(duration, lambda _: None, self.start_function, self.end_function)

    def start_function(self, obj):
        obj.change_intelligence_characteristic(self.value)

    def end_function(self, obj):
        obj.change_intelligence_characteristic(-self.value)


class DecreaseIntelligenceEffect:
    def __init__(self, duration, value):
        self.set_description(f"Снижение интеллекта на {value} на {duration / FPS} секунд")
        self.value = value
        
        super().__init__(duration, lambda _: None, self.start_function, self.end_function)

    def start_function(self, obj):
        obj.change_intelligence_characteristic(-self.value)

    def end_function(self, obj):
        obj.change_intelligence_characteristic(self.value)


class IncreaseStrengthEffect:
    def __init__(self, duration, value):
        self.set_description(f"Увеличение силы на {value} на {duration / FPS} секунд")
        self.value = value
        
        super().__init__(duration, lambda _: None, self.start_function, self.end_function)

    def start_function(self, obj):
        obj.change_strength_characteristic(self.value)

    def end_function(self, obj):
        obj.change_strength_characteristic(-self.value)


class DecreaseStrengthEffect:
    def __init__(self, duration, value):
        self.set_description(f"Уменьшение силы на {value} на {duration / FPS} секунд")
        self.value = value
        
        super().__init__(duration, lambda _: None, self.start_function, self.end_function)

    def start_function(self, obj):
        obj.change_strength_characteristic(-self.value)

    def end_function(self, obj):
        obj.change_strength_characteristic(self.value)


class IncreaseSpeedEffect:
    def __init__(self, duration, value):
        self.set_description(f"Повышение скорости на {value} на {duration / FPS} секунд")
        self.value = value
        
        super().__init__(duration, lambda _: None, self.start_function, self.end_function)

    def start_function(self, obj):
        obj.change_speed_characteristic(self.value)

    def end_function(self, obj):
        obj.change_speed_characteristic(-self.value)


class DecreaseSpeedEffect:
    def __init__(self, duration, value):
        self.set_description(f"Снижение скорости на {value} на {duration / FPS} секунд")
        self.value = value
        
        super().__init__(duration, lambda _: None, self.start_function, self.end_function)

    def start_function(self, obj):
        obj.change_speed_characteristic(-self.value)

    def end_function(self, obj):
        obj.change_speed_characteristic(self.value)



