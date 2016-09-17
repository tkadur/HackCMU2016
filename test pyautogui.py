import pyautogui
import time

def scroll(clicks):
    pyautogui.scroll(clicks)

def leftClick():
    pyautogui.click()

def rightClick():
    pyautogui.click(button = 'right')

def press(function):
    pyautogui.press(function)

def leftTab():
    pyautogui.keyDown('command')
    pyautogui.press('tab')
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.keyUp('command')
    
