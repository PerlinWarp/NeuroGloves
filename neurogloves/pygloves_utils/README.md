# pygloves-utils  
![Demo showing hand and finger movement](https://media2.giphy.com/media/4P8L3HQAg5qEDBmffP/giphy.gif?cid=790b7611cd5a3029ab0414bbdc674fb1a19867a290c3426a&rid=giphy.gif&ct=g)

It would be nice to see if [LucidGloves](https://github.com/LucidVR/lucidgloves) work without having to start SteamVR.
This repo attempts to plot glb files in the same was as Steam, so that you can test out experimental designs, such as gloves with potentiometers per finger joint, without having to get it working with Steam, etc    

```
pip install numpy
pip install matplotlib
pip install pyserial

# Test using Arduino over Serial (check comport and left/right handedness)
python lerp_finger_from_serial.py
# Test using GUI
python lerp_finger_slider.py
```

#### lerp_finger_from_serial.py  
Reads serial values then plots the hand live using multithreading.  
In order to work, you need to define the COM port that the Arduino is using and make sure no other program is using it. E.g. SteamVR    

#### lerp_finger_slider.py  
Features 6 sliders, one for overall curl and one for each finger.   
Moving these sliders will generate plots of the hand using those curl values.  

#### bone.py  
Attempts to plot the OpenGloves glb file.   
The glb file is hierarchical, so the end of the finger cannot just be plotted, it has to be calculated by considering the other points in the finger. Relative positions have to be built into global positons.

#### Useful links  
[glb/gltf2.0 refrence guide](https://www.khronos.org/files/gltf20-reference-guide.pdf)  
[glb Nodes Tutorial](https://github.com/KhronosGroup/glTF-Tutorials/blob/master/gltfTutorial/gltfTutorial_004_ScenesNodes.md)    
[OpenVR Hand Skeleton Docs](https://github.com/ValveSoftware/openvr/wiki/Hand-Skeleton)  
[3Blue1Brown, Visualizing quaternions](https://www.youtube.com/watch?v=d4EgbgTm0Bg)  
[Implimenting Forward Kinematics](https://www.alanzucconi.com/2017/04/06/implementing-forward-kinematics/)  