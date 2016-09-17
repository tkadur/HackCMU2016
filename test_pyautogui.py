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
    print(s)
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

def ourSleep(duration, checkFunction):
    checkInterval = 0.1
    timerCount = 0
    while (timerCount < duration):
        if (not checkFunction()):
            return -1
        time.sleep(checkInterval)
        timerCount += checkInterval
    return 0

def smartIntervalExecute(longInterval, shortInterval, checkFunction, mainFunction, args = ()):
    interval = longInterval
    while (checkFunction()):
        mainFunction(*args)
        code = ourSleep(interval, checkFunction)
        if (code == -1):
            return
        interval = shortInterval

def scroll(clicks,acceleration,checkFunction):
    if (acceleration==0):
        smartIntervalExecute(0.40,0.40,checkFunction,pyautogui.scroll,(clicks,))
    else:
        smartIntervalExecute(0.25,0.10,checkFunction,pyautogui.scroll,(clicks+acceleration,))

def leftTab(checkFunction):
    pyautogui.keyDown('command')
    pyautogui.press('tab')
    for i in range(0,2):
        pyautogui.press('left')
    smartIntervalExecute(2,0.75, checkFunction, pyautogui.press,('left',))
    pyautogui.keyUp('command')

def rightTab(checkFunction):
    pyautogui.keyDown('command')
    pyautogui.press('tab')
    smartIntervalExecute(2, 0.75, checkFunction, pyautogui.press, ('right',))
    pyautogui.keyUp('command')

def screenshot():
    return pyautogui.screenshot()

def screenOff():
    global globalBrightness
    globalBrightness= getBrightness()
    os.system('brightness [-v]')

def screenOn():
    setBrightness(globalBrightness)

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
