# Leveraging Cognitive States in Human-Robot Teaming

*Maintained by Jack Kolb (kolb@gatech.edu)*

### Overview

GitHub repository for our paper "Leveraging Cognitive States In Human-Robot Teaming", presented at RO-MAN 2022.

In this work, we investigated the question *"Can we leverage a team's cognitive state to improve the team's role assignments?"*. Put simply, if we have three people to assign to three different roles, can we use measurements of different cognitive skills to decide who to assign to each role?

We conducted a (virtual) user study where participants took three "cognitive skill" tests, and then performed three robot teleoperation tasks. We then created a model that uses cognitive skill scores to predict user performance at the robot teleoperation tasks. Lastly, we split users into teams and evaluated the impact of our model on informing role allocation of team members. We found that our *Individualized Role Assignment* (IRA) resulted in allocations that performed ~20% superior to random allocation.

This repository contains the following modules:
1. The webserver code we used to conduct our online user study. Contains the cognitive skill tests and robot teleoperation tasks.
2. The robot 3D simulation environments. We used the Webots simulator, and had the robot video feeds stream from the simulator to the participant's browser.
3. The data analysis scripts. After conducting the user study, we ran an analysis script to process the webserver logs into cognitive skill test scores and robot teleoperation scores, calculate metrics, and generate plots.
4. User scores from our study. These scores were obtained using the analysis scripts provided, and then anonymized. They are useful as a verification of our results, and can potentially be used as a dataset.

All code should work out of the box. While we do not have an anaconda environment set up for this project, `requirements.txt` details the Python 3 packages needed. Please email Jack Kolb if there are any issues!

___

### Getting Started: Reproduce our Results

A single script, `main.py`, runs our user study data analysis and generates the plots seen in our paper. Open a terminal and run:

`$ cd analysis`

`$ python3 main.py`


The script's output contains the metrics and figures we presented in our paper. We slightly edited several figures by removing/repositioning legends and adding additional text.

___

### Analysis Module

The Analysis Module is packaged as a single script (`main.py`) that processes the data, analyzes the possible user teams, and plots the results. Most of the heavy lifting is pushed to functions in Python scripts in the `/processing/`, `/allocation/`, and `/plotting/` folders.

As shown in the *Getting Started* section, the terminal command `$ python3 main.py` will run the analysis module.

Below is an outline of what each file contains.

```
📂analysis
 ┣ 📂allocation
 ┃ ┗ 📜assignment_util.py  --  handles user logs processing, handles team generation, has utility functions for team processing.
 ┃ ┗ 📜onehot_allocation.py  --  manages team processing.
 ┣ 📂logs -- place user log files from the webserver here.
 ┣ 📂plotting
 ┃ ┗ 📜plot_histogram.py  --  generates histogram distributions of team scores using several allocation mechanisms (in paper).
 ┃ ┗ 📜plot_lines.py  --  generates a line plot of the predicted scores and actual scores of all users (**not** in paper).
 ┃ ┗ 📜plot_nc3.py  --  generates box plots of the IRA and random allocation scores of various team sizes (in paper).
 ┃ ┗ 📜plot_ranking.py  --  generates a histogram of IRA allocations ranked against all (6) possible allocations (in paper).
 ┃ ┗ 📜plot_scatter.py  --  generates a scatter plot of user scores in each skill/task pairing (**not** in paper).
 ┃ ┗ 📜plot_whiskers.py  --  generates a box plot of the difference between IRA and random team scores (**not** in paper).
 ┣ 📂processing
 ┃ ┗ 📜process_ni.py  --  processes user logs to get their Network Inference cognitive skill test scores.
 ┃ ┗ 📜process_ot.py  --  processes user logs to get their Object Tracking cognitive skill test scores.
 ┃ ┗ 📜process_questionnaire.py  --  processes user logs to get their questionnaire responses.
 ┃ ┗ 📜process_s1.py  --  processes user logs to get their Stage 1 teleoperation task scores.
 ┃ ┗ 📜process_s2.py  --  processes user logs to get their Stage 2 teleoperation task scores.
 ┃ ┗ 📜process_s3.py  --  processes user logs to get their Stage 3 teleoperation task scores.
 ┃ ┗ 📜process_sa.py  --  processes user logs to get their Situational Awareness cognitive skill test scores.
 ┣ 📜main.py  --  runs functions from other files to process user logs, analyze teams, and generate plots.
 ┣ 📜replay.py  --  enables replaying a user's teleoperation.
 ┣ 📜score_data_3c3.pkl  --  processed user data from the "3 choose 3" team size condition, generated by main.py.
 ┗ 📜score_data_4c3.pkl  --  processed user data from the "4 choose 3" team size condition, generated by main.py, included here because 4c3, 5c3, 6c3, and 7c3 take a long time to generate.
```

Each file has numerous comments as documentation. However, to use this module you should not need to edit any files except `main.py`.

To replay a user's teleoperation, the `replay.py` script uses a user's log file and Selenium to reproduce the user's browser interactions. This can be useful for visualizing user runs and for collecting new serverside or clientside metrics from old runs. We found replays to be highly accurate on our hardware and network connection, however you may need to tune the delays to fit your connection. To use the replay script, edit `replay.py` to set your user parameters, open a terminal, and run:

`$ cd analysis`

`$ python3 replay.py`

___

### Webserver Module

The Webserver Module is a Python webserver built on Flask and ROS1, and the code is contained in the `/server/` folder. The webserver is the interface between study participants and the Webots simulator. Since we want to pass information between the participant's browser and the Webots simulator (which is ROS-based), we ran the webserver on the same computer as the simulator run both a ROS node to interact with the simulator, and a webserver to deliver web and ROS content to users over the internet. You can also run the simulator and webserver on seperate computers connected to the same ROS master node.

To start the webserver, open a terminal and run:

`$ cd server`

`$ python3 app.py`

By default the webserver binds to port 5000, this is specified by the `port=5000` parameter at the bottom of `app.py`, and can be changed to whatever port you wish to use. Using port 80 is common as it is the default http port, other ports will require specifying the port in the URL, `http://(address):(port)`, for example `http://1.2.3.4:5000`. Sometimes Flask or Python will fail to unbind from a port when the webserver is restarted, giving a "Address already in use" error when running the webserver. In that event, it is easiest to just change the port in `app.py` and start the webserver again.

To give our server a public web address without the hassle of port forwarding (which can be challenging over a university network), we used [ngrok](https://ngrok.com). If you plan to only use the webserver locally (i.e., connect to it only with devices on your personal or university's network, such as an in-person user study), there is no need to run ngrok, and you can use your webserver computer's IP address.

After installing ngrok, to create an HTTP tunnel to a specified port, open a terminal and run:

`$ ngrok http 5000`

The `5000` is the port to bind ngrok's URL to, so if you change the port in `app.py`, also change it in the above command.

The `xxxx-xxx-xxx-xxx-xxx.ngrok.io` URL shown in ngrok's output is the URL that will connect to the webserver. To try it out, open that URL in your web browser. If you get a 404 error, make sure ngrok is running, the webserver is running, and ngrok is using the port specified in `app.py`.

The webserver covers:

* Showing users an overview of what the user study entails, and obtaining consent.
* Conducting a preliminary demographics questionnaire.
* Conducting the Network Inference, Object Tracking, and Situation Awareness cognitive skill tests.
* Conducting a short training course on robot teleoperation.
* Conducting the Stage 1, Stage 2, and Stage 3 robot teleoperation tasks.
* Recording user responses and test/task interactions to a user-specific log file.

Additionally, the webserver:

* Uses ROS to interface with the Webots simulator to set/remove waypoints for each robot.
* Converts video feeds from simulator robots into browser-compatible messages, used for the teleoperation tasks.
* Maintains teleoperation task states and syncs task states between the Webots simulator and the user's browser.

The webserver's files contain detailed comments on the implementation.

The best way to see how we used the webserver (and to try it out yourself) is by checking out [our study script (Google Docs)](https://docs.google.com/document/d/1y-0var-6Ltc6vcixZux_ZgciKB3cbiNUhBCvaw7DXXA). As a note, the `workerId` URL parameter is the participant's ID. 

___

### Simulation Module

Our simulation is built using Webots ROS, where we implemented custom controllers for several mobile robots to enable waypoint navigation.

Webots ROS can be installed through apt:

`$ sudo apt-get install ros-melodic-webots-ros`

To launch Webots ROS, run the following:

`$ roslaunch webots_ros webots_ros_python.launch`

Our environment is built upon https://github.com/chungshan/formation_uavs. We have two world files, `experiment_world_uavs.wbt` and `experiment_world_ugvs.wbt`. As denoted by the file names, the former has four UAVs (DGI Mavic drones) for Stage 1, and the later has four UGVs (Clearpath Moose robots) for Stage 3. Our Stage 2, where the participant controls four UAVs and four UGVs, does not need a 3D simulation as there are no visual feeds presented to the user.

To run a world, simply open the `.wbt` file and press the play button in the simulator. To improve the simulation framerate we disabled the renderer during our studies (button above the view window).

___

### Citing Our Paper

If you use our work, please cite us!

BibTex:

```
@inproceedings{kolb2022leveraging,
  title={Leveraging Cognitive States In Human-Robot Teaming},
  author={Kolb, Jack and Ravichandar, Harish and Chernova, Sonia},
  booktitle={2022 31st IEEE International Conference on Robot \& Human Interactive Communication (RO-MAN)},
  year={2022},
  organization={IEEE}
}
```


MLA:

```
Kolb, Jack, et al. "Leveraging Cognitive States In Human-Robot Teaming." 2022 31st IEEE International Conference on Robot & Human Interactive Communication (RO-MAN). IEEE, 2022.
```

