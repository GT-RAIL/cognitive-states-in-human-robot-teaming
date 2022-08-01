# Leveraging Cognitive States in Human-Robot Teaming

*Maintained by Jack Kolb (kolb@gatech.edu)*

GitHub repository for our paper "Leveraging Cognitive States In Human-Robot Teaming", presented at RO-MAN 2022.

In this work, we investigate the question *"Can we improve 1-1 user-role allocations by considering the team's cognitive skills prior to assignment?"*.

We conducted a (virtual) user study where participants took three "cognitive skill" tests, and then performed three robot teleoperation tasks. We then created a model that uses cognitive skill scores to predict user performance at the robot teleoperation tasks. Lastly, we split users into teams and evaluated the impact of our model on informing role allocation of team members. We found that our *Individualized Role Assignment* (IRA) resulted in allocations that performed 20% superior to random allocation.

This repository contains the following modules:
1. The webserver code we used to conduct our online user study. Contains the cognitive skill tests and robot teleoperation portals.
2. The robot simulation files. We used the WeBots simulator, had scripts interface with the webserver, and had video feeds stream from the simulator to the webserver's teleoperation portals.
3. The analysis scripts. After conducting the user study, we ran an analysis script to process the webserver logs into cognitive skill test scores and robot teleoperation scores, calculate metrics, and generate plots.
4. User scores from our study. These scores were obtained using the analysis scripts provided, and then anonymized. They are useful as a verification of our results, and can potentially be used as a dataset. 

All code should work out of the box. While I do not have an anaconda environment set up for this project, `requirements.txt` details the Python 3 packages and versions used. Please email Jack Kolb if there are any issues!


### How to reproduce our numerical and visual results

A single script, `main.py`, runs all our user study data analysis and generates the plots seen in our paper.

`cd analysis`

`python3 main.py`


The script's output contains the metrics we presented in our paper, and will generate the figures we used in our paper. Note that we slightly edited several figures by removing/repositioning legends and adding additional text.


### Analysis Module

The Analysis Module runs linearly -- a single script (`main.py`) processes the data (calling various functions in other files), analyzes the possible user teams, and plots the results. Most of the heavy lifting is pushed to functions in files in the `/processing/`, `/allocation/`, and `/plotting/` folders.

**NOTE: If you make your own log files by running through the user study, create a `/logs/` folder in `/analysis/` and place the log .txt files there for analysis! You will also need to uncomment a line in `main.py`, see that file's comments for instructions.**

Below is an outline of what each file contains.

📂analysis
 ┣ 📂allocation
 ┃ ┗ 📜assignment_util.py  --  handles user logs processing, handles team generation, has utility functions for team processing.
 ┃ ┗ 📜onehot_allocation.py  --  manages team processing.
 ┣ 📂**logs** -- not included on the GitHub repository (empty), create this folder and place user log files from the webserver here.
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

Each file has numerous comments as documentation. However, to use this module you should not need to edit any files except `main.py`.

To replay a user's teleoperation, the `replay.py` script uses a user's log file and Selenium to reproduce the user's browser interactions. This can be useful for visualizing user runs (e.g., questionable runs) and for collecting new serverside or clientside metrics from old data. We found replays to be highly accurate on our hardware and network connection, so have included it in this release as an additional tool. If you intend to use the script, you will need to edit `replay.py` for each user you replay.
