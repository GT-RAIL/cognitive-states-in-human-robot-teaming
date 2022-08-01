# assignment_util.py: the main data processing code, contains functions for conducting assignment and processing logs

import numpy as np
import pickle
import random
from scipy.linalg import cholesky

# process the data logs into a user score matrix
#    input: log file path
#    output: dict{dict{}}, N x (T + J) matrix, N is number of participants, T is number of skills, J is number of tasks
def process_logs(path="logs", specific_users=[]):
    # process the text files to get user scores
    import processing.process_ot
    import processing.process_sa
    import processing.process_ni
    import processing.process_s1
    import processing.process_s2
    import processing.process_s3

    ot_data = processing.process_ot.get_ot_data(path, specific_users=specific_users)
    sa_data = processing.process_sa.get_sa_data(path, specific_users=specific_users)
    ni_data = processing.process_ni.get_ni_data(path, specific_users=specific_users)
    s1_data = processing.process_s1.get_s1_data(path, specific_users=specific_users, metric="distance progress")
    s2_data = processing.process_s2.get_s2_data(path, specific_users=specific_users, metric="time to complete / max caches connected")
    s3_data = processing.process_s3.get_s3_data(path, specific_users=specific_users, metric="distance progress / duration")

    # combine into a dictionary format
    user_scores = {}
    for p in {**sa_data, **ni_data, **ot_data, **s1_data, **s2_data, **s3_data}:
        if "email" in p or p == "0" or "none" in p:  # ignore non-user data
            continue
        if p not in user_scores:  # add user to user scores if applicable
            user_scores[p] = {}
        # add scores to the user
        user_scores[p]["sa"] = sa_data[p] if p in sa_data else -1
        user_scores[p]["ni"] = ni_data[p] if p in ni_data else -1
        user_scores[p]["ot"] = ot_data[p] if p in ot_data else -1
        user_scores[p]["s1"] = s1_data[p] if p in s1_data else -1
        user_scores[p]["s2"] = s2_data[p] if p in s2_data else -1
        user_scores[p]["s3"] = s3_data[p] if p in s3_data else -1
    
    return user_scores


# use the (anonymized) scores from our user study, generated from process_logs()
def retrieve_paper_user_scores():
    user_scores = {
        '8943': {'sa': 0.93, 'ni': 34, 'ot': 0.52, 's1': 0.41379310344827586, 's2': 1.0, 's3': 0.3161340438895029},
        '1770': {'sa': 0.98, 'ni': 59, 'ot': 0.78, 's1': 0.34056761268781305, 's2': 1.0, 's3': 0.38594337022379477}, 
        '6423': {'sa': 0.93, 'ni': 16, 'ot': 0.74, 's1': 1.0, 's2': 0.06171428571428572, 's3': 0.4331180018496568}, 
        '9705': {'sa': 0.88, 'ni': 28, 'ot': 0.59, 's1': 0.43776824034334766, 's2': 0.21428571428571427, 's3': 0.6130627279044976}, 
        '8997': {'sa': 0.84, 'ni': 31, 'ot': 0.78, 's1': 0.3493150684931507, 's2': 0.134, 's3': 0.6577352589968243}, 
        '9489': {'sa': 0.67, 'ni': 23, 'ot': 0.59, 's1': 0.34056761268781305, 's2': 0.21428571428571427, 's3': 0.5870777434741943}, 
        '1162': {'sa': 0.91, 'ni': 33, 'ot': 0.78, 's1': 0.32299849650891727, 's2': 0.11771428571428572, 's3': 0.29235272501091597}, 
        '7054': {'sa': 0.98, 'ni': 17, 'ot': 0.63, 's1': 0.5573770491803278, 's2': 0.8585714285714285, 's3': 0.47191975559447374}, 
        '8466': {'sa': 0.76, 'ni': 36, 'ot': 0.48, 's1': 0.546916890080429, 's2': 0.2861904761904762, 's3': 0.3268649289319447},
        '6600': {'sa': 0.81, 'ni': 19, 'ot': 0.67, 's1': 0.3428571428571429, 's2': 0.21464285714285714, 's3': 0.1344622036978622},
        '4855': {'sa': 0.91, 'ni': 32, 'ot': 0.59, 's1': 0.5811965811965812, 's2': 1.0, 's3': 0.582916657513748}, 
        '9025': {'sa': 0.91, 'ni': 36, 'ot': 0.7, 's1': 0.44541484716157204, 's2': 0.07542857142857143, 's3': 0.8718668977101399}, 
        '5997': {'sa': 0.67, 'ni': 34, 'ot': 0.52, 's1': 0.8717948717948718, 's2': 1.0, 's3': 0.7774149820639231}, 
        '4122': {'sa': 0.81, 'ni': 42, 'ot': 0.67, 's1': 0.4573991031390135, 's2': 1.0, 's3': 0.5272866641144949}, 
        '9633': {'sa': 0.74, 'ni': 48, 'ot': 0.7, 's1': 0.31880369475183035, 's2': 1.0, 's3': 0.08340683743926837}, 
        '3462': {'sa': 0.65, 'ni': 29, 'ot': 0.59, 's1': 0.2821416076148231, 's2': 0.21428571428571427, 's3': 0.7149911474176187}, 
        '3414': {'sa': 0.79, 'ni': 29, 'ot': 0.7, 's1': 0.4104627766599598, 's2': 0.13228571428571428, 's3': 0.18967466295160795}, 
        '8032': {'sa': 0.98, 'ni': 23, 'ot': 0.78, 's1': 0.27607665375488677, 's2': 0.07914285714285714, 's3': 0.48270411690516285}, 
        '9925': {'sa': 0.76, 'ni': 16, 'ot': 0.63, 's1': 0.4031620553359684, 's2': 0.21428571428571427, 's3': 1.0}, 
        '6007': {'sa': 0.67, 'ni': 14, 'ot': 0.74, 's1': 0.3417085427135678, 's2': 0.13742857142857143, 's3': 0.22559117512979282}, 
        '2579': {'sa': 0.79, 'ni': 52, 'ot': 0.48, 's1': 0.2789623759112831, 's2': 1.0, 's3': 0.23715481048201734}, 
        '4142': {'sa': 1.0, 'ni': 23, 'ot': 0.7, 's1': 0.46788990825688076, 's2': 1.0, 's3': 0.1834974332280541}, 
        '3403': {'sa': 0.86, 'ni': 12, 'ot': 0.67, 's1': 0.5964912280701755, 's2': 0.21464285714285714, 's3': 0.7123556507591585}, 
        '7310': {'sa': 0.95, 'ni': 19, 'ot': 0.78, 's1': 0.3493150684931507, 's2': 0.2857142857142857, 's3': 0.4524932299409081}, 
        '5500': {'sa': 0.96, 'ni': 41, 'ot': -1, 's1': 0.21593038934304004, 's2': 0.42642857142857143, 's3': 0.14522943976767916}, 
        '9115': {'sa': 0.72, 'ni': -1, 'ot': 0.56, 's1': 0.34113712374581945, 's2': 0.42928571428571427, 's3': 0.964144916210581}, 
        '9253': {'sa': 0.6, 'ni': 38, 'ot': 0.52, 's1': 0.3417085427135678, 's2': 0.21392857142857144, 's3': 0.30536891209368666}, 
        '8813': {'sa': 0.74, 'ni': 36, 'ot': 0.67, 's1': 0.18325790161139466, 's2': 0.42857142857142855, 's3': 0.5177523890229148},
        '5292': {'sa': 0.91, 'ni': 33, 'ot': 0.74, 's1': 0.3968871595330739, 's2': 0.42928571428571427, 's3': 0.3299667234631283}
    }

    return user_scores

# force a task/skill relationship to have a perfect ranking, used to debug and verify the code works
def oracle_task(user_scores, task, skill):
    for p in user_scores:
        if skill == "ni":
            user_scores[p][skill] = user_scores[p][task]
        else:
            user_scores[p][skill] = user_scores[p][task]

    return user_scores

# generates fake data to a given R correlation value
def generate_fake_bivariate_user_scores(N=30, R=1, slope_range=[0,1]):
    # uses a correlation matrix to determine bivariate data, from (https://quantcorner.wordpress.com/2018/02/09/generation-of-correlated-random-numbers-using-python/)

    # initialize the users and slopes
    user_scores = {}
    all_data = {}

    tasks = ["s1", "s2", "s3"]
    skills = ["ot", "ni", "sa"]

    # generate the user ID, ensure it's not already used
    for i in range(N):
        while True:
            p = random.randint(1000, 9999)  # user ID
            if p not in user_scores:
                break
        
        user_scores[p] = {}
    
    for i in range(len(tasks)):
        # specify the correlation matrix
        corr_mat= np.array([[1.0, R], [R, 1.0]])

        # compute the (upper) Cholesky decomposition matrix
        upper_chol = cholesky(corr_mat)

        # generate 2 series of normally distributed (Gaussian) numbers (for a diagonal skill-task relationship)
        rnd = np.zeros((30, 2))
        counter = 0
        while rnd[29,0] == 0:  # while not filled
            sample = np.random.normal(0.5, .2, size=(2))
            # reject samples outside the bounds
            if sample[0] < 0 or sample[0] > 1 or sample[1] < 0 or sample[1] > 1:
                continue

            rnd[counter,:] = sample
            counter += 1
        
        # finally, compute the inner product of upper_chol and rnd
        result = rnd @ upper_chol

        # assign the results to users
        user_ids = list(user_scores.keys())
        for j in range(len(user_ids)):
            user_scores[user_ids[j]][tasks[i]] = result[j][0]
            user_scores[user_ids[j]][skills[i]] = result[j][1]

        all_data[tasks[i]] = result[:,0]
        all_data[skills[i]] = result[:,1]
        
        
    return user_scores



# generate random users to test the allocation algorithms
#    input: N (number of users), skill_noise (standard deviation of user skill scores, on the scale of %), task_noise (standard deviation of user task scores, on the scale of %)
#    output: dict{dict{}}, N x (T + J) matrix, N is number of participants, T is number of skills, J is number of tasks
def generate_fake_user_scores(N=30, skill_noise=0, task_noise=0):
    user_scores = {}

    tasks = ["s1", "s2", "s3"]
    skills = ["ot", "ni", "sa"]

    # generate the slopes for each skill/task relationship
    slopes = {}
    y_ints = {}
    for task in tasks:
        slopes[task] = {}
        y_ints[task] = {}
        for skill in skills:
            slopes[task][skill] = random.random() / 2  # scale from 0 to .5
            y_ints[task][skill] = random.gauss(.5, .2)
            y_ints[task][skill] -= max(0, slopes[task][skill] + y_ints[task][skill] - 1)  # correct the y intercept so no scores are above 1

    # for each user, generate fake scores
    for i in range(N):
        # generate the user ID, ensure it's not already used
        while True:
            p = random.randint(1000, 9999)  # user ID
            if p not in user_scores:
                break
        
        user_scores[p] = {}

        # for each task
        for t in range(len(tasks)):
            # generate the skill score
            user_scores[p][skills[t]] = 1.1
            while user_scores[p][skills[t]] > 1 or user_scores[p][skills[t]] < 0:
                user_scores[p][skills[t]] = random.gauss(.5, skill_noise)

            # generate diagonal task scores
            user_scores[p][tasks[t]] = 1.1
            while user_scores[p][tasks[t]] > 1 or user_scores[p][tasks[t]] < 0:
                user_scores[p][tasks[t]] = slopes[tasks[t]][skills[t]] * user_scores[p][skills[t]] + (2 * random.random() - 1) * task_noise + y_ints[tasks[t]][skills[t]]  # theoretical + noise + y_int

    p = list(user_scores.keys())[0]
    
    # return the user scores
    return user_scores, slopes


# pulls every human subset
#   input: N (number of rows), J (number of assignments))
#   output: subsets (N^(J-1)xJ)
import itertools
def pullSubsets(N, J, subsets=[], subset=[], slot=-1, all=False):
    if not all:
        subsets = [list(x) for x in itertools.combinations(range(N), J)]
    if all:
        subsets = [list(x) for x in itertools.permutations(range(N), J)]
    return subsets


# function for calculating best fit line, from (https://stackoverflow.com/questions/10048571)
def best_fit_slope(score_pairing):
    xs = [x[0] for x in score_pairing]
    ys = [x[1] for x in score_pairing]
    N = len(xs)
    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in zip(xs, ys):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    if det == 0:
        return 0, 0
    return (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det
    
# function for removing outliers (1.5x IQR)
def remove_outliers(scores):
    # if empty list, return
    if len(scores) == 0:
        return []
    
    # remove the outlier scores for each dimension
    for index in range(len(scores[0])):
        Q1 = sorted([x[index] for x in scores])[len(scores) // 4]
        Q3 = sorted([x[index] for x in scores])[int(len(scores) // 1.25)]
        IQR = Q3 - Q1
        outlier_min = Q1 - IQR * 1.5
        outlier_max = Q3 + IQR * 1.5
        scores = [x for x in scores if x[index] > outlier_min and x[index] < outlier_max]
    return scores


# function for generating the impact matrix from user scores
import scipy.stats
def generate_impact_matrix(user_scores, skills, tasks, correlation="spearman"):
    impact_matrix = {}
    yint_matrix = {}  # while not necessary, including the y intercept matrix so we can play with absolute predicted scores (not just relative scores)
    weight_matrix = {}

    # generate the impact matrix: slope for each skill/task pairing
    for skill in skills:
        for task in tasks:
            # get the skill/task scores
            pairing = [[user_scores[p][skill], user_scores[p][task]] for p in user_scores if user_scores[p][skill] != -1 and user_scores[p][task] not in [-1, 0]]

            # remove outliers
            pairing = remove_outliers(pairing)

            # determine the slopes of each best fit line
            m, y = best_fit_slope(pairing)
            
            # store the slopes in the impact matrix
            if skill not in impact_matrix:
                impact_matrix[skill] = {}
                yint_matrix[skill] = {}
                weight_matrix[skill] = {}
            impact_matrix[skill][task] = m
            yint_matrix[skill][task] = y
            if correlation == "spearman":
                weight_matrix[skill][task] = abs(scipy.stats.spearmanr([x[0] for x in pairing], [x[1] for x in pairing])[0])
            if correlation == "pearson":
                weight_matrix[skill][task] = abs(scipy.stats.pearsonr([x[0] for x in pairing], [x[1] for x in pairing])[0])
        
        # normalize the weight matrix
        for task in tasks:
            weight_matrix[skill][task] /= sum([abs(x) for x in weight_matrix[skill].values()])
            #weight_matrix[skill][task] = 0.333
    
    return impact_matrix, yint_matrix, weight_matrix


# function for predicting a user's score given the impact matrix and the user test scores
def predict_test_user_performance(test_user_scores, impact_matrix={}, yint_matrix={}, weight_matrix={}, skills=[], tasks=[]):
    score_predictions = {p : {} for p in test_user_scores}
    for p in test_user_scores:
        for task in tasks:
            if yint_matrix == {}:
                #print("NOTE: No y-int matrix provided to assignment_util.predict_test_user_performance()")
                score_predictions[p][task] = sum([weight_matrix[skill][task] * impact_matrix[skill][task] * test_user_scores[p][skill] for skill in skills])  # sum of weight * slope * skill
            else:
                score_predictions[p][task] = sum([weight_matrix[skill][task] * (impact_matrix[skill][task] * test_user_scores[p][skill] + yint_matrix[skill][task]) for skill in skills])
        
        # if some stages are ignored, fill their values with 0
        if "s1" not in tasks:
            score_predictions[p]["s1"] = 0
        if "s2" not in tasks:
            score_predictions[p]["s2"] = 0
        if "s3" not in tasks:
            score_predictions[p]["s3"] = 0
    
    return score_predictions


# optimally assigns each human worker to each job 
#   input: S (NxJ matrix of human job cost)
#   output: bool (whether a solution was found), a (job assignment of each worker)
from munkres import Munkres
def hungarian(S, maximize=True):
    # if maximizing the score, multiply everything by -1 (finding min of negation finds the max)
    if maximize:
        S_final = [[x * -1 for x in y] for y in S]
    else:
        S_final = S

    # relies on the Munkres library (via Pip)
    m = Munkres()
    indexes = m.compute(S_final)
    
    a = [col for row, col in indexes]  # [user1 task idx, user2 task idx, user3 task idx]
    return a


# function for filtering out users who do not have complete data
def filter_complete_users(user_scores, skills=["ot", "ni", "sa"], tasks=["s1", "s2", "s3"]):
    # ignores users with a -1 skill (incomplete data), -1 task (incomplete data), or a 0 task (did not complete any base objectives)
    filtered_scores = {p : user_scores[p] for p in user_scores if -1 not in [user_scores[p][skill] for skill in skills] and -1 not in [user_scores[p][task] for task in tasks] and 0 not in [user_scores[p][task] for task in tasks]}
    return filtered_scores


# processes a set of user scores into the skill-based team assignments for all 3-user teams, and do onehot allocation
import allocation.onehot_allocation
import random
def process_users(user_scores, complete_user_scores, skills=[], tasks=[], team_size=3, sample_size=None):
    # define the skill and tasks
    prediction_tasks = tasks

    # generate the one hot of test and skill data
    num_train = len(user_scores) - len(tasks)  # the number of items to train on
    num_test = len(tasks)  # the number of items to test on

    complete_user_scores_ids = list(complete_user_scores.keys())  # pull the IDs of the users who completed all stages

    # if the sample size is less than or equal to the team size, effectively no point in specifying it
    if sample_size is not None and sample_size <= team_size:
        sample_size = None

    score_data = []  # holds the data for each team combination
    counter = 0
    used_ids = {}

    # if the sample size is None, using 3c3, iterate through all 3 sets
    if sample_size is None:
        team_indexes = pullSubsets(len(complete_user_scores_ids), team_size)  # pull each possible team, in the form of indexes instead of IDs

        # train and evaluate on each fold
        num_teams = len(team_indexes)

        print("Processing", num_teams, "teams")
        for team in team_indexes:
            if counter % 100 == 0:
                print("% complete", round(100 * counter / num_teams, 2))
            # extract the test/train user IDs from the team indexes
            test_ids = [complete_user_scores_ids[i] for i in team]  # convert the team indexes to user IDs

            for idd in test_ids:
                if idd not in used_ids:
                    used_ids[idd] = 0
                used_ids[idd] += 1
            
            score_data.append(allocation.onehot_allocation.onehot_allocation(complete_user_scores, test_ids, skills, tasks, prediction_tasks))  # record the score data
            counter += 1
        
        pickle.dump(score_data, open("./score_data_3c3.pkl", "wb"))

    # if the sample size is not None, using 3c3, iterate through all 3 sets
    if sample_size is not None:
        print("Sample Size", sample_size)
        sample_indexes = pullSubsets(len(complete_user_scores_ids), sample_size)  # pull each possible 6-user set

        # train and evaluate on each fold
        num_samples = len(sample_indexes)
        print("Processing", num_samples, "samples")
        for sample in sample_indexes:
            if counter % 1000 == 0:
                print("% complete", round(100 * counter / (num_samples), 2))
                pickle.dump(score_data, open("./score_data_" + str(sample_size) + "c" + str(team_size) + ".pkl", "wb"))
            # extract the test/train user IDs from the team indexes
            test_ids = [complete_user_scores_ids[i] for i in sample]  # convert the team indexes to user IDs

            for idd in test_ids:
                if idd not in used_ids:
                    used_ids[idd] = 0
                used_ids[idd] += 1

            score_data.append(allocation.onehot_allocation.onehot_allocation(complete_user_scores, test_ids, skills, tasks, prediction_tasks, team_size=team_size))  # record the score data
            counter += 1

        print("ID Count", used_ids)
        pickle.dump(score_data, open("./score_data_" + str(sample_size) + "c" + str(team_size) + ".pkl", "wb"))


    return score_data
