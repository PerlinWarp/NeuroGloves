# Basics   

## Getting a demo using SteamVR

The demo works using the [OpenGloves driver](https://github.com/LucidVR/opengloves-driver), the driver expects to take in serial values representing the curl of each finger. 
For each finger, 0 represents fully closed and 1023 represents fully open.
A simple demo can be made by wiring one potentiometer to an Arduino Nano, loading the Lucid Gloves Arduino firmware then watching the values in the Arduino Serial Monitor change as you open and close the potentiometer.

The OpenGloves driver listens to these values and then uses them to construct a glove in SteamVR. SteamVR takes a value (0.0-1.0) for each finger and also one number representing the splay. More info [here](https://github.com/ValveSoftware/openvr/wiki/Creating-a-Skeletal-Input-Driver).

In Windows a serial port can only be read by one process at a time.
An algorithm could be trained to predict LucidGlove output 0-1023 from Myo input. Visualising data collection helps with errors, but OpenGloves and my program cannot read the Arduino input at the same time. 
To send curl values from my program to OpenGloves requires a way to emulate a serial port, this is done by [com0com](http://com0com.sourceforge.net/).
`Neuro/passthrough.py` is a testing script. It reads data from the Arduino (COM8) then passes it to OpenGloves (COM6).    
Before any demo, passthrough.py should be run, if it doesn't display correctly in SteamVR then something is wrong:

* Check if the ports in the code match those sent by the Arduino and expected by the LucidGloves driver. 
* Check the device ports are what you think they are in Windows Device Manager. 
* Check no other programs are using those ports. e.g. did you leave the Arduino IDE serial monitor open? 
* It's also good to check for errors in the SteamVR webconsole.

Setup Steps:

1. Connect the Arduino
2. Start SteamVR and a game with finger tracking, e.g. Half Life Alyx
3. Make sure the OpenGloves plugin is enabled and running.
4. `python passthrough.py`
5. Move the potentiometer backwards and forwards and see the fingers moving
6. Press Ctrl+C or Ctrl + Break to stop the process

If that works:  
7. Connect the Myo, put it on and let it warm up.  
8. Run `python plot_emgs.py` to confirm the Myo is working.  
9. `python .\predictor_basic.py`  



Known problems:

For predictor_basic, only class 2 seems to work, which should move the index finger but seems to close the whole hand.  While this isn't completely solved, opening com0com and resetting the comports seems to often fix this.

### plot_emgs.py  
Plots EMG signals (line graphs for each channel) coming from the Myo using pygame.   

### myo_multithreading_examp.py
Shows an example of how to use this library to get data from the Myo.  

### simple_classifier.py 
Runs a KNN on the data coming from the EMG, label them into different groups by pressing the 0-9 keys.  
Data from training is stored in data/  

