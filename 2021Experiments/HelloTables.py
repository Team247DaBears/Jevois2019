import threading
from networktables import NetworkTables
import time

duration=120
counter=0

cond=threading.Condition()
notified = [False]

def connectionListener(connected,info):
    print(info,'; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

print("Hello NetworkTables")

NetworkTables.initialize(server="10.2.47.2")
NetworkTables.addConnectionListener(connectionListener,immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()
        
print("I don't know what it means, but I made it to here")

sd=NetworkTables.getTable('SmartDashboard')
sd.putNumber("Sample Number",247)

print("Did it make it?")

while counter<duration:
    counter+=1
    sd.putNumber("pi counter",counter)
    time.sleep(1)
