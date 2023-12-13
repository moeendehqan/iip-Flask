import cv2
import time

le = '۵۲د۶۸۹۱۱'
idplate = le[:2]
alpha = le[2:3]
serial = le[3:6]
city = le[6:]
print(int(idplate))
print(alpha)
print(serial)
print(city)