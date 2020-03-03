# autogame
Control computer car games with your palm

Palm images are used to extract the HOG features. Then SVM is used to train those features.
If palm is found in the boxes,appropriate command was sent to game using pyautogui.


Use the config.json file in detector/configuration to configure input/output paths and SVM, HOG parameters.

Run detector/train.py to train the model. Run control_game.py to start the application. In the mean time open the game you want and configure the following in the game,<br> <ul>
                   <li> up arrow button - accelarate</li>
                    <li> down arrow button - stop/reverse</li>
                    <li> left arrow button - move left</li>
                    <li> right arrow button -move right </li>
                    </ul>
                   

# Demo video 

![autogame demo](demo/demo.gif)
