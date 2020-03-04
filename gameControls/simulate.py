import controls,random,time

control_types={ 1:controls.accelerate , 2:controls.stop, 3:controls.move_right, 4:controls.move_left   }

'''
Simulate the controls for game
'''
while True:
    controls.move_forward()
    rand= random.randint(3,4);
    selected_function = control_types[rand];
    selected_function();
    time.sleep(1);
