import time

id="10-000802587a9e"

mytemp = ''
filename = 'w1_slave'
while True:
	f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
	line = f.readline() # read 1st line
	crc = line.rsplit(' ',1)
	crc = crc[1].replace('\n', '')
	if crc=='YES':
		line = f.readline() # read 2nd line
		mytemp = line.rsplit('t=',1)
		print mytemp[1]
		if int(mytemp[1]) >= -29000:
			print "AC working" 
	
	time.sleep(0.5)
