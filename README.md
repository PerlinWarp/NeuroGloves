# NeuroGloves  
  
<p align="center">
<img src="https://media0.giphy.com/media/zKslp7Cgrf56l3poxq/giphy.gif" alt="SteamVR finger tracking" width="800"/>
</p>
  
See [Getting Started with NeuroGloves](https://github.com/PerlinWarp/NeuroGloves/wiki/Getting-started) in the Wiki.  
  
NeuroGloves works using the [OpenGloves driver](https://github.com/LucidVR/opengloves-driver), the driver expects to take in serial values representing the curl of each finger. 
For each finger, 0 represents fully closed and 1023 represents fully open.
A simple demo can be made by wiring one potentiometer to an Arduino Nano, loading the Lucid Gloves Arduino firmware then watching the values in the Arduino Serial Monitor change as you open and close the potentiometer.

The OpenGloves driver listens to these values and then uses them to construct a glove in SteamVR. SteamVR takes a value (0.0-1.0) for each finger and also one number representing the splay. More info [here](https://github.com/ValveSoftware/openvr/wiki/Creating-a-Skeletal-Input-Driver).

NeuroGloves uses a Named Pipe to send these values to OpenGloves.
