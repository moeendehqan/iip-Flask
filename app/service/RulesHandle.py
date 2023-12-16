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
        GPIO.setup(1, GPIO.OUT)
        GPIO.setup(2, GPIO.OUT)
        GPIO.setup(3, GPIO.OUT)
        if status == 0:
            GPIO.output(1, GPIO.HIGH)
            GPIO.output(2, GPIO.LOW)
            GPIO.output(3, GPIO.LOW)
        if status == 1:
            GPIO.output(1, GPIO.LOW)
            GPIO.output(2, GPIO.HIGH)
            GPIO.output(3, GPIO.LOW)
        if status == 3:
            GPIO.output(1, GPIO.LOW)
            GPIO.output(2, GPIO.LOW)
            GPIO.output(3, GPIO.HIGH)

        

