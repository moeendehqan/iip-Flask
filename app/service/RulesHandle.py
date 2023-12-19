
from gpiozero import LED



class RulesHandle():
    def __init__(self):
        self.allow = LED(17)
        self.not_allow = LED(27)
        self.noting = LED(22)
    def CheckAllow(self,status):
        if status == 2:
            self.allow.on()
            self.not_allow.off()
            self.noting.off()
        if status == 1:
            self.allow.off()
            self.not_allow.on()
            self.noting.off()
        if status == 0:
            self.allow.off()
            self.not_allow.off()
            self.noting.on()
