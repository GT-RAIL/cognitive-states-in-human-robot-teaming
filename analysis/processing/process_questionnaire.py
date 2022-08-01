# process_ot.py: contains functions for reading the user logs and extracting the OT skill test scores

import os


# reads all user logs and extracts their questionnaire answers
def get_questionnaire_data(path, specific_users=[]):
    questions = ["How familiar are you with robots", "What is your age", "What is your gender"]

    seen = {question : {} for question in questions}
    results = {question : {} for question in questions}
    for p in os.listdir(path):
        # check specific users
        if specific_users != [] and sum([1 for x in specific_users if x in p]) == 0:
            continue

        p = p[:-4]
        with open(path + "/" + p + ".txt", "r") as f:
            actions = f.readlines()

            for i in range(len(actions)):
                a = actions[i]

                for question in questions:
                    if question.replace(" ", "") in a and p not in seen[question]:
                        seen[question][p] = a.split(", ")[2][-1]
                        if a.split(", ")[2][-1] not in results[question]:
                            results[question][a.split(", ")[2][-1]] = 0
                        results[question][a.split(", ")[2][-1]] += 1
      
    return results
