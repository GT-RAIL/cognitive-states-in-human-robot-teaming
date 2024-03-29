# process_sa.py: contains functions for reading the user logs and extracting the SA skill test scores

import os

def get_sa_data(path, specific_users=[]):
    sa_scores = {}
    for p in os.listdir(path):
        # check specific users
        if specific_users != [] and sum([1 for x in specific_users if x in p]) == 0:
            continue

        p = p[:-4]
        sa_scores[p] = -1
        with open(path + "/" + p + ".txt", "r") as f:
            actions = f.readlines()

            for i in range(len(actions)):
                a = actions[i]

                # if completed the SAGAT, print the score
                if "SAGAT" in a and "'complete'" in a:
                    sa_scores[p] = round(int(a[:-1].split(", ")[2].split(": ")[1]) / 85, 2)  # 85 is the highest score possible
    return sa_scores
