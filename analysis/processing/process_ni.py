# process_ni.py: contains functions to retrieve the Network Inference scores for all users

import os

# generates the network inference scores from each user's logs
def get_ni_data(path, specific_users=[]):
    ni_scores = {}

    for p in os.listdir(path):
        # check specific users
        if specific_users != [] and sum([1 for x in specific_users if x in p]) == 0:
            continue

        # get the user's ID (file is of name "USERID.txt", so cut off the .txt ending)
        p = p[:-4]

        # open the log file and get the networks score
        with open(path + "/" + p + ".txt", "r") as f:
            ni_scores[p] = -1

            actions = f.readlines()

            for a in range(len(actions)):
                action = actions[a]
                if "networks" in action and "game complete" in action:
                    # calculate the score
                    score = sum([ int(x) for x in action.split(": ")[4].split("[")[1].split("]")[0].split(",") ])  # lower is better metric
                    ni_scores[p] = score
                    
    return ni_scores
