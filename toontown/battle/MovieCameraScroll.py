from direct.task import Task
import math
#Task to move the camera
SPIN_CAM = 0
SUIT_SCROLL_CAM = 1
TOON_SCROLL_CAM = 2
SIDE_VIEW_CAM = 3
BACK_SIDE_VIEW_CAM = 4

SPIN_TIME = 0

 
counter = 0
isGoingBack = False
CameraIsRunning = None

def spinCameraTask(task):
    global SPIN_TIME
    global CameraIsRunning
    CameraIsRunning = True
    SPIN_TIME+= 1
    if SPIN_TIME == 180:
        SPIN_TIME = 0
        CameraIsRunning = False
        return Task.done
    angledegrees = task.time * 6.0
    angleradians = angledegrees * (math.pi / 180.0)
    base.camera.setX(20*math.sin(angleradians))
    base.camera.setY(-20.0*math.cos(angleradians))
    base.camera.setH(angledegrees)
    return Task.cont
    
def toonScrollCameraTask(task):
    global counter
    global isGoingBack
    global CameraIsRunning
    CameraIsRunning = True
    if isGoingBack:
        if counter < -6:
            isGoingBack = False
        counter -=.08
        base.camera.setX(counter)
    elif counter > 7:
        counter = 0
        CameraIsRunning = False
        return Task.done
        '''
        isGoingBack = True
        counter-= .02
        base.camera.setX(counter)
        '''
    elif counter < 6:
        counter+= .08
        base.camera.setX(counter)
    else:
        counter +=.08
        base.camera.setX(counter)
    return Task.cont
    
def suitScrollCameraTask(task):
    global counter
    global isGoingBack
    global CameraIsRunning
    CameraIsRunning = True
    if isGoingBack:
        if counter < -8:
            isGoingBack = False
        counter -=.08
        base.camera.setX(counter)
    elif counter > 8:
        counter = 0
        CameraIsRunning = False
        return Task.done
        '''
        isGoingBack = True
        counter-= .05
        base.camera.setX(counter)
        '''
    elif counter < -8:
        counter+= .08
        base.camera.setX(counter)
    else:
        counter +=.08
        base.camera.setX(counter)
    return Task.cont
    
ycoord = -11
def suitForwardYScrollCameraTask(task):
    global counter
    global isGoingBack
    global CameraIsRunning
    global ycoord
    CameraIsRunning = True
    if isGoingBack:
        if counter < -8:
            isGoingBack = False
        counter -=.08
        base.camera.setY(counter)
    elif counter > 8:
        counter = 0
        CameraIsRunning = False
        return Task.done
        '''
        isGoingBack = True
        counter-= .05
        base.camera.setX(counter)
        '''
    elif counter < -8:
        counter+= .08
        base.camera.setY(ycoord+counter)
    else:
        counter +=.08
        base.camera.setY(ycoord+counter)
    return Task.cont 

def suitBackwardYScrollCameraTask(task):
    global counter
    global isGoingBack
    global CameraIsRunning
    CameraIsRunning = True
    if isGoingBack:
        if counter < -8:
            isGoingBack = False
        counter -=.08
        base.camera.setY(counter)
    elif counter < -8:
        counter = 0
        CameraIsRunning = False
        return Task.done
        '''
        isGoingBack = True
        counter-= .05
        base.camera.setX(counter)
        '''
    elif counter > -8:
        counter-= .08
        base.camera.setY(counter)
    else:
        counter -=.08
        base.camera.setY(counter)
    return Task.cont        
    
def sideScrollCameraTask(task):
    global counter
    global isGoingBack
    global CameraIsRunning
    CameraIsRunning = True
    if isGoingBack:
        if counter < -10:
            isGoingBack = False
        counter -=.08
        base.camera.setX(counter)
    elif counter > 15:
        counter = 0
        CameraIsRunning = False
        return Task.done
        '''
        isGoingBack = True
        counter-= .08
        base.camera.setX(counter)
        '''
    elif counter < -10:
        counter+= .08
        base.camera.setX(counter)
    else:
        counter +=.08
        base.camera.setX(counter)
    return Task.cont