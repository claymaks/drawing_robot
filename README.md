# Drawing Robot
2-link drawing robot rendered with forward kinematics using translation/rotation matrices and homogenous coordinates.  Closed form inverse kinematics are used to move arm to desired point and images are converted to paths using [linedraw](https://github.com/LingDong-/linedraw).

To convert images into drawings, use
```
python3 draw.py --image {image path}
```

![](/media/face.gif)
![](/media/random_lines.gif)
![](/media/mouse.gif)

## Controls (keyboard, `demo_controller.py`):
 - Q/E: rotate base joint 
 - A/D: rotate middle joint
 - U/E: rotate base joint (high speed)
 - J/L: rotate middle joint (high speed)
 - Space: toggle pen

## Controls (mouse, `demo_mouse.py`):
 - Click: toggle pen


## Demos (`demo.py`):
 Contains a few examples of how to interface with the robot to create several different drawings.