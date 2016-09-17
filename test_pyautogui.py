import pyautogui
import time
import os
import subprocess



def getBrightness():
    cmd = ['brightness -l']
    output = subprocess.Popen( cmd, shell = True, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    #print(output)
    #print(getBrightnessLevel(output[0]))
    return getBrightnessLevel(output)



def getBrightnessLevel(s):
    return(s.strip().split(' ')[-1])
    '''
    newString=""
    for index in (len(s)-11,len(s)-3):
        newString+=str(s[index])
    return newString
    '''

def setBrightness(s):
    os.system('brightness '+s)


globalBrightness = getBrightness()

def ourSleep(duration, checkFunction, args):
    checkInterval = 0.1
    timerCount = 0
    while (timerCount < duration):
        if (not checkFunction(*args)):
            return -1
        time.sleep(checkInterval)
        timerCount += checkInterval
    return 0

def smartIntervalExecute(longInterval, shortInterval, checkFunction, mainFunction, args = (), args2 = ()):
    interval = longInterval
    #print(args)
    while (checkFunction(*args)):
        mainFunction(*args2)
        code = ourSleep(interval, checkFunction, args)
        if (code == -1):
            return
        interval = shortInterval

def scroll(clicks,acceleration,checkFunction, arg = ()):
    if (acceleration==0):
        smartIntervalExecute(0.40,0.40,checkFunction,pyautogui.scroll, args = arg, args2 = (clicks,))
    else:
        smartIntervalExecute(0.25,0.10,checkFunction,pyautogui.scroll,args = arg, args2 = (clicks+acceleration,))

def leftTab(checkFunction, arg = ()):
    pyautogui.keyDown('command')
    pyautogui.press('tab')
    for i in range(0,2):
        pyautogui.press('left')
    smartIntervalExecute(2,0.75, checkFunction, pyautogui.press,args = arg, args2 = ('left',))
    pyautogui.keyUp('command')

def rightTab(checkFunction, arg = ()):
    pyautogui.keyDown('command')
    pyautogui.press('tab')
    smartIntervalExecute(2, 0.75, checkFunction, pyautogui.press, args = arg, args2 = ('right',))
    pyautogui.keyUp('command')

def screenshot():
    return pyautogui.screenshot()

def screenOff():
    global globalBrightness
    globalBrightness= getBrightness()
    os.system('brightness [-v]')

def screenOn():
    setBrightness(globalBrightness)

def zoomIn():
    pyautogui.keyDown('command')
    pyautogui.press('=')
    
#input("Waiting")
#os.system('say "hello world"')
#setBrightness(getBrightness())
    #jalkdsjfkl

    
#_thread.start_new_thread(test, ())

##now = int(time.time())
##
##def wait():
##    return (int(time.time()) - now) < 6
#asdf 
