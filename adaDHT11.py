import time
import Adafruit_DHT
sensor = Adafruit_DHT.DHT11
pin = 32
try:
    while True :
        t = Adafruit_DHT.read_retry(sensor, pin)
        if t is not None:
            print("Temperature = {0:0.1f}*C".format(t))
        else :
            print('Read error')
        time.sleep(1)
except KeyboardInterrupt:
    print("Terminated by Keyboard")
 
finally:
    print("End of Program")