# replays Stage 3 from the log file of user actions; set the REPLAY PARAMETERS section configuration to replay a specific user

import requests
import ast
import datetime
import time
from selenium import webdriver

# REPLAY
DOMAIN = "35b4-143-215-178-206"  # ngrok ID from running the server (e.g., "35b4-143-215-178-206" represents "35b4-143-215-178-206.ngrok.io"), the replay system will connect to that server
STAGE = 2  # the stage we are replaying
USER = "5997"  # the user ID we are replacing
BROWSER = None  # the browser instance, keep this as None (it will be assigned to the selenium browser)

# open the stage in a new browser instance
def open_stage():
    global BROWSER
    # construct the URL
    url = "http://" + DOMAIN + ".ngrok.io/stage?stage=" + str(STAGE) + "&workerId=" + str(USER) + "-replay-S" + str(STAGE)
    BROWSER = webdriver.Firefox()
    BROWSER.get(url)

# clicks all the collect cache buttons
def collect_cache():
    cam1 = BROWSER.find_element_by_id("cam1_button")
    cam2 = BROWSER.find_element_by_id("cam2_button")
    cam3 = BROWSER.find_element_by_id("cam3_button")
    cam4 = BROWSER.find_element_by_id("cam4_button")

    cam1.click()
    cam2.click()
    cam3.click()
    cam4.click()
    return

# network command to add a waypoint
def add_waypoint(robot, x, y):
    requests.get("http://" + DOMAIN + ".ngrok.io/add-waypoint?id=" + robot + "&x=" + str(x) + "&y=" + str(y))
    return

# network command to remove a waypoint
def remove_waypoint(robot):
    requests.get("http://" + DOMAIN + ".ngrok.io/remove-waypoint?id=" + robot)
    return

# main loop to replay the stage
def replay_stage(worker_id):
    start_time = float("inf")
    diff_time = 0
    cacheCollectCount = 0  # number of caches that have been collected
    running = False
    open_stage()  # the browser that we are emulating
    time.sleep(10)  # wait 10 secs

    with open("./logs/" + str(worker_id) + ".txt", "r") as f:
        print("found log")
        lines = f.readlines()
        lines = [x[:-1] for x in lines]  # remove the trailing \n

        # for each action in the log
        for action in lines:
            # skip blank lines
            if action == "":
                continue

            # ignore if not the correct stage
            if "'stage': " + str(STAGE) not in action:
                continue

            # parse the action and set the current and listed time delay
            comma = action.find(",")
            this_time = float(action[:comma])
            curr_time = datetime.datetime.now().timestamp() - diff_time

            # if the stage is not running yet (it starts on user action), and we have an action that would start the clock, start the stage
            if not running and ("add-valid-waypoint" in action or "select-vehicle" in action) and "'stage': " + str(STAGE) in action:
                start_time = float(action.split(",")[0])
                diff_time = datetime.datetime.now().timestamp() - start_time
                running = True
                BROWSER.execute_script("startStage();")
                print("starting run", action)
            
            # ignore actions that are from before the start time (this will also be TRUE if the stage has not started yet, as start_time will be infinity)
            if this_time < start_time:
                continue
                    
            # check if adding or removing a waypoint
            if running and "select-vehicle" not in action and "deselect-vehicle" not in action and "add-valid-waypoint" not in action and "remove-waypoint" not in action and "cache" not in action.lower() and "stage-complete" not in action:
                print("    ", action)
                continue

            # get the execution time offset, this is to account for network/server latency, which affects these actions in particular
            time_offset = 0
            if "add-valid-waypoint" in action and STAGE == 2:
                time_offset = .365
            if "remove-waypoint" in action:
                time_offset = .006

            # if an offset was added then wait until it is time to execute
            while curr_time < this_time - time_offset:
                curr_time = datetime.datetime.now().timestamp() - diff_time

            # user selected a robot
            if "select-vehicle" in action:
                target_robot = action.split("'")[7]
                if STAGE == 1:
                    target_robot_dict = {"UAV1": 6 + cacheCollectCount, "UAV2": 7 + cacheCollectCount, "UAV3": 8 + cacheCollectCount, "UAV4": 9 + cacheCollectCount}
                if STAGE == 2:
                    target_robot_dict = {"UGV1": 5, "UGV2": 6, "UGV3": 7, "UGV4": 8, "UAV1": 1, "UAV2": 2, "UAV3": 3, "UAV4": 4}
                if STAGE == 3:
                    target_robot_dict = {"UGV1": 14, "UGV2": 15, "UGV3": 16, "UGV4": 17}
                target_robot_index = target_robot_dict[target_robot]
                BROWSER.execute_script("uiMap.selectedObject = uiMap.uiObjects[" + str(target_robot_index) + "];")
                print("selected vehicle", target_robot)

            # user deselected a vehicle
            if "deselect-vehicle" in action:
                act = webdriver.common.action_chains.ActionChains(BROWSER)
                act.send_keys("q")
                act.perform()
                print("deselected waypoint")
                
            # user added a waypoint
            if "add-valid-waypoint" in action:
                entry = ast.literal_eval(action[comma + len(worker_id) + 2:])
                location = ast.literal_eval(entry["location"])
                if STAGE == 1 or STAGE == 3:
                    add_waypoint(entry["target"], location[0], location[1])
                if STAGE == 2:
                    stage = BROWSER.find_element_by_id("uimap-canvas")
                    act = webdriver.common.action_chains.ActionChains(BROWSER)
                    act.move_to_element_with_offset(stage, 700 * location[0], 700 * location[1])
                    act.click().perform()
                print("added waypoint", action)
                
            # user removed a waypoint
            if "remove-waypoint" in action:
                entry = ast.literal_eval(action[comma + len(worker_id) + 2:])
                if STAGE == 1 or STAGE == 3:
                    remove_waypoint(entry["target"])
                if STAGE == 2:
                    act = webdriver.common.action_chains.ActionChains(BROWSER)
                    act.send_keys("r")
                    act.perform()
                print("removed waypoint", action)
            
            # if user collected a cache
            if "cache" in action.lower() and "cache connected" not in action.lower() and "states" not in action.lower():
                collect_cache()
                cacheCollectCount += 1
                print("collected cache")

            # completed stage, exit sim
            if "stage-complete" in action:
                print("ending stage")
                BROWSER.quit()
                break

    print("done!")


# replay the stage
if __name__ == "__main__":
    replay_stage(USER)
