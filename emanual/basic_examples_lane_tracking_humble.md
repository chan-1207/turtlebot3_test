

{% capture notice_01 %}
**NOTE**: 
- This example is operated on `Ubuntu 22.04` and `ROS2 Humble Hawksbill`.  
- You should already have completed gazebo simulation before you start this
{% endcapture %}
<div class="notice--danger">{{ notice_01 | markdownify }}</div>

### Lane Tracking::Explain  

This is a example about lane tracking with turtlebot3 by camera in gazebo simulator.  
You can personally experience calibrating the camera parameters to operate the TurtleBot3 for lane tracking in the Gazebo simulator.
 

### Lane Tracking::Install for starting

1. Install turtlebot3_example package.
``` bash
$ cd ~/turtlebot3_ws/src        #turtlebot3_ws = your workspace for turtlebot. 
$ git clone https://github.com/GyuH13/turtlebot_example.git
$ cd ~/turtlebot3_ws/src/turtlebot_example/for_gazebo
$ mv lane_tracking_example turtlebot3_burger_cam ~/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/models
$ mv lane.world ~/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/worlds
$ mv lane_tracking_example.launch.py ~/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/launch
$ mv turtlebot3_burger_cam.urdf ~/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/urdf
$ cd ~/turtlebot3_ws && colcon build --symlink-install
```

2. Install dependent package.  
``` bash
$ sudo apt install ros-humble-cv-bridge ros-humble-vision-opencv python3-opencv libopencv-dev ros-humble-topic-tools ros-humble-image-proc ros-humble-image-transport ros-humble-image-transport-plugins
```

### Lane Tracking::Camera Calibration  

1. Launch the course in gazebo.
``` bash
$ export TURTLEBOT3_MODEL=burger_cam
$ ros2 launch turtlebot3_gazebo lane_tracking_example.launch.py
```  
2. Launch the instrinsic calibration node.
``` bash
$ ros2 launch turtlebot3_lane_tracking_camera instrinsic_camera_calibration.launch.py
```  

3. Launch the extrinsic calibration node as calibration mode.
``` bash
$ ros2 launch turtlebot3_lane_tracking_camera extinsic_camera_calibration.launch.py calibration_mode:=True
```  

4. Open the rqt.
``` bash
$ rqt
```  

5. In the top left corner,open **Plugins > visualization > Image view**. Create two view frames.  
  Set the topics to `/camera/image_extrinsic_calib/compressed` and `/camera/image_projected_compensated` for each frame.  
  ![](/assets/images/platform/turtlebot3/lane_tracking/camera_calibration_rqt.png)  
  Open **Plugins > Configuration > dynamic reconfigure**.  
  On the left side, select `/camera/image_compensation` and `/camera/image_projected`   
  Use this to configure the parameters and adjust the projection region.  
  Find and select the best-fit parameters.  
  ![](/assets/images/platform/turtlebot3/lane_tracking/rqt_configuration_calibration.png)  

6. Apply the parameters you selected to the YAML file. 
  It determines the default parameter values when launching without calibration_mode.
``` bash
$ cd ~/turtlebot3_ws/src/turtlebot3_example/turtlebot3_lane_tracking_camera/calibration/extrinsic_calibration
$ gedit projection.yaml
```  
![](/assets/images/platform/turtlebot3/lane_tracking/projection_yaml.png) 

### Lane Tracking::Detect Lane  

1. Launch the course in gazebo.
``` bash
$ ros2 launch turtlebot3_gazebo lane_tracking_example.launch.py
```  
2. Launch the instrinsic calibration node.
``` bash
$ ros2 launch turtlebot3_lane_tracking_camera instrinsic_camera_calibration.launch.py
```  

3. Launch the extrinsic calibration node as calibration mode.
``` bash
$ ros2 launch turtlebot3_lane_tracking_camera extinsic_camera_calibration.launch.py
```  

4. Launch the detect lane node  
``` bash
ros2 launch turtlebot3_lane_tracking_detect detect_lane.launch.py calibration_mode:=True
```  

5. Open the rqt.
``` bash
$ rqt
```  
Open three Image views and select `/detect/image_yellow_lane_marker/compressed`, `/camera/image_lane/compressed`, `/detect/image_white_lane_marker/compressed` 
![](/assets/images/platform/turtlebot3/lane_tracking/detect_lane.png)  
On the left side, select `/detect_lane`  
Use this for configuring parameters.  
![](/assets/images/platform/turtlebot3/lane_tracking/rqt_configuration_detect.png)  

6. Apply the parameters you selected to the YAML file.  
  It determines the default parameter values when launching without calibration_mode.  
``` bash
$ cd ~/turtlebot3_ws/src/turtlebot3_example/turtlebot3_lane_tracking_detect/param/lane
$ gedit lane.yaml
```  
![](/assets/images/platform/turtlebot3/lane_tracking/detect_yaml.png)  

### Lane Tracking::Driving  

1. Launch the course in **gazebo**.
``` bash
$ ros2 launch turtlebot3_gazebo lane_tracking_example.launch.py
```  
2. Launch the **instrinsic calibration node**.
``` bash
$ ros2 launch turtlebot3_lane_tracking_camera instrinsic_camera_calibration.launch.py
```  

3. Launch the **extrinsic calibration node** as calibration mode.
``` bash
$ ros2 launch turtlebot3_lane_tracking_camera extinsic_camera_calibration.launch.py
```  

4. Launch the **detect lane node**.  
``` bash
ros2 launch turtlebot3_lane_tracking_detect detect_lane.launch.py
``` 

5. Launch the **control node**.  
``` bash
ros2 launch turtlebot3_lane_tracking_drive control_lane.launch.py
```