import pyautogui,time 

# time in seconds between keydown and key up
timer = .1


def accelerate():
    '''
    press the up button of the keybord till the given time
    '''
    pyautogui.keyDown("up");
    time.sleep(timer)
    pyautogui.keyUp("up");

def move_left():
    '''
    press the left button of the keybord till the given time
    '''
    pyautogui.keyDown("left");
    time.sleep(timer)
    pyautogui.keyUp("left");

def move_right():
    '''
    press the right button of the keybord till the given time
    '''
    pyautogui.keyDown("right");
    time.sleep(timer)
    pyautogui.keyUp("right");

def accelerate_and_left():
    '''
    press the up and left button of the keybord till the given time
    '''
    pyautogui.keyDown("up");
    pyautogui.keyDown("left");
    time.sleep(timer)
    pyautogui.keyUp("up");
    pyautogui.keyUp("left");

def accelerate_and_right():
    '''
    press the up and right button of the keybord till the given time
    '''
    pyautogui.keyDown("up");
    pyautogui.keyDown("right");
    time.sleep(timer)
    pyautogui.keyUp("up");
    pyautogui.keyUp("right");

def stop():
    '''
    press the down button of the keybord till the given time
    '''   
    pyautogui.keyDown("down");
    time.sleep(timer)
    pyautogui.keyUp("down");

def reverse_and_left():
    '''
    press the up and left button of the keybord till the given time
    '''
    pyautogui.keyDown("down");
    pyautogui.keyDown("left");
    time.sleep(timer)
    pyautogui.keyUp("down");
    pyautogui.keyUp("left");

def reverse_and_right():
    '''
    press the up and right button of the keybord till the given time
    '''
    pyautogui.keyDown("down");
    pyautogui.keyDown("right");
    time.sleep(timer)
    pyautogui.keyUp("down");
    pyautogui.keyUp("right");

def move_vehicle(control_queue):
    '''
    Call the appropriate method using given data from another process

    Indide the infinite while loop get the controls from the queue.
    using this data call the appropriate function to press the corresponding keys

    Parameters
    ----------
    control_queue : Queue
        To get control data from another process

    '''
    while True:
        control = control_queue.get()
        if(len(control) > 1):
            if control[0] == "Accelerate":
                if control[1] == "Left":
                    accelerate_and_left()
                elif control[1] == "Right":
                    accelerate_and_right()
            else:
                if control[1] == "Left":
                    reverse_and_left()
                elif control[1] == "Right":
                    reverse_and_right()

        elif(len(control) > 0) :
            if control[0] == "Accelerate":
                accelerate()
            elif control[0] == "Stop":
                stop()



