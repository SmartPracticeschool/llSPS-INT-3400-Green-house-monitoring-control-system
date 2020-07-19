import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
#Provide your IBM Watson Device Credentials
organization = "bmu240"
deviceType = "rasberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='motoron':
                print("motor is on")
        elif i=='motoroff':
                print("motor is off")
        
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        hum=random.randint(10, 40)
        #print(hum)
        temp =random.randint(30, 80)
        soil=random.randint(10,60)
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : temp, 'Humidity': hum, 'soilmoisture':soil }
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum,"soilmoisture= %s %"%soil, "to IBM Watson")

        success = deviceCli.publishEvent("Weather", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback
       
        r=requests.get('https://www.fast2sms.com/dev/bulk?authorization=nO5pF9ULeKwo8EvHfVImxDaB1XqMbdGrs20C74ZluYhA3tTJzyNze7VmUb1AYkhZySL69xa3goW84qpK&sender_id=FSTSMS&message=temp is above threshold values&language=english&route=p&numbers=9182519168,9912233583')
        if temp>=70:
                print(r.status_code)
                       


# Disconnect the device and application from the cloud
deviceCli.disconnect()


