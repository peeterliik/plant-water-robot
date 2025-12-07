from machine import Pin, ADC
import time

REMEASURE_TIME = 1800
DRY_THRESHOLD = 15000
WATERING_TIME = 5

relay = Pin(0, Pin.OUT)
sensor = ADC(Pin(26))
led = Pin(25, Pin.OUT)
logfile = open("logs.txt", "a", 0)

def water_or_not():
    led.on()
    sensor_read = sensor.read_u16()
    
    if sensor_read < DRY_THRESHOLD:
        relay.value(1)  # Turn the relay ON
        time.sleep(WATERING_TIME)
        relay.value(0)  # Turn the relay OFF
        watering = True
    else:
        watering = False
        
    write_to_log(str(sensor_read), watering)
    time.sleep(REMEASURE_TIME)
    led.off()

def write_to_log(sensor_value, watering):
    now = time.localtime()
    current_time = time.strftime("%d/%m/%Y-%H:%M:%S", now)
    if watering:
        watering_text = "Plants got SOME water!"
    else:
        watering_text = "Plants got NO water!"
    
    log_text = current_time + " | " + "Sensor value: " + sensor_value + " | " + watering_text + "\n"
    print(log_text)
    logfile.write(log_text)
    logfile.flush()
    logfile.close
    
while True:
    water_or_not()

    
