from app.models.Rules import Rulse
from rpi.gpio_proxy import GPIOProxy as GPIO


class RulseHandle():
    def __init__(self):
        self.rules_models = Rulse()
    
    def status(self, idplate, alpha, serial, city):
        res = self.rules_models(idplate, alpha, serial, city)
        if res == True:
            return 2
        elif res == False:
            return 0
        else:
            return 1
    def gate(self,status):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(status+1, GPIO.OUT)
        GPIO.output(status+1, GPIO.HIGH)

        

