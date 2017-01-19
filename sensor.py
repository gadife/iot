import RPi.GPIO as GPIO
import time
import os.path
import csv
from datetime import datetime

sensor = 17
id="10-000802587a9e"
mytemp = ''

last_movement = 0
ever_movement = False

#if os.path.isfile(str(time.strftime("%d-%m-%Y"))+ ".csv"):
#	print "yes"
#else:
sensor_history_file = open(str(time.strftime("%d-%m-%Y"))+ ".csv","a")
writer = csv.writer(sensor_history_file, delimiter=',')

print (time.strftime("%d-%m-%Y"))
#sensor_history_file = 

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN)

while True:
	if str(time.strftime("%d-%m-%Y")) not in str(sensor_history_file):
		sensor_history_file = open(str(time.strftime("%d-%m-%Y"))+ ".csv","wb")
		writer = csv.writer(sensor_history_file, delimiter=',')
		print "created new csv file"
	f = open('/sys/bus/w1/devices/' + id + '/w1_slave', 'r')
        line = f.readline() # read 1st line
        crc = line.rsplit(' ',1)
        crc = crc[1].replace('\n', '')
        if crc=='YES':
                line = f.readline() # read 2nd line
                mytemp = line.rsplit('t=',1)
                if int(mytemp[1]) >= -29000:
                        ac_status = "on"
		else:
			ac_status = "off"
	else:	
		current_temp=99999
		ac_status = "error"

	i = GPIO.input(sensor)
	if i == 1:
		last_movement = time.time()
		ever_movement = True
	if i == 0:
		if ever_movement:
			print "seconds from last movement: " + str(int(time.time()-last_movement))
			if int(time.time()-last_movement) > 180 and ac_status is "on":
				print "Noone in the room for last 3 minutes but AC is on"

	print str(datetime.now()) + "," + str(i) + "," + ac_status
	writer.writerow( (str(datetime.now()), str(i), ac_status) )
	time.sleep(3)

