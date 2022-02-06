# FollowCam
A servo gimbal that allows a webcam to follow a face around the room. It can also follow an Aruco marker, if you want to use the aruco marker as a tool to direct your camera around.

Youtube Demo: https://youtu.be/1L1MOE9W7iE

## Installation/Prerequisites
* Designed for use with a Logitech C270 webcam (720p)
* Written in Python 3.8.9
* Uses OpenCV
  * Run pip install pip install opencv-contrib-python
* Uses pyserial 
  * Run pip install pyserial
* Uses numpy
  * Included in OpenCV
* Requires Arduino IDE and arduino Nano
* Uses [pyvirtualcam](https://github.com/letmaik/pyvirtualcam)
  * Run pip install pyvirtualcam
  * Requires the installation of [OBS (Open Broadcaster Software)](https://obsproject.com/), which is free. There may be a way to install just the virtual cam portion, but I have not figured it out.
* If you want Aruco Marker tracking, go [here](https://chev.me/arucogen/)

## License
Created by Mark Gilliland, 2020. No reuse without permission except for hobby/entheusiast purposes.
