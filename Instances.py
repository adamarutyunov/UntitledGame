from BaseModule import *
from Constants import *
from LocationModule import *
from TechnicalModule import *
from EntityModule import *
from MagicModule import *


class HealthUpPotion(Item):
    def __init__(self):
        super().__init__(self.use, "Зелье лечения")

        self.load_icon(load_image("textures/items/potions/health_up_potion.png"))

    def use(self, obj):
        effect = IncreaseHealthEffect(60, 0.5)
        obj.affect_effect(effect)
        obj.remove_item(self)


class IntelligenceUpPotion(Item):
    def __init__(self):
        super().__init__(self.use, "Зелье интеллекта")

        self.load_icon(load_image("textures/items/potions/intelligence_up_potion.png"))

    def use(self, obj):
        effect = IncreaseIntelligenceEffect(600, 10)
        obj.affect_effect(effect)
        obj.remove_item(self)


class StrengthUpPotion(Item):
    def __init__(self):
        super().__init__(self.use, "Зелье силы")

        self.load_icon(load_image("textures/items/potions/strength_up_potion.png"))

    def use(self, obj):
        effect = IncreaseStrengthEffect(600, 10)
        obj.affect_effect(effect)
        obj.remove_item(self)


class SpeedUpPotion(Item):
    def __init__(self):
        super().__init__(self.use, "Зелье скорости")

        self.load_icon(load_image("textures/items/potions/speed_up_potion.png"))

    def use(self, obj):
        effect = IncreaseSpeedEffect(600, 10)
        obj.affect_effect(effect)
        obj.remove_item(self)
