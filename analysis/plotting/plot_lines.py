from matplotlib import pyplot as plt
import scipy.stats
import itertools
import numpy
import allocation.assignment_util


# plots lines between actual user scores and predicted user scores
def plot_lines(user_scores):
    print("---------- Plotting the lines between predicted and actual scores for each user ----------")
    # create three plots
    _, (ax1, ax2, ax3) = plt.subplots(1, 3)  # get the plot axis
    axes = {"s1": ax1, "s2": ax2, "s3": ax3}

    # initialize the plots
    for stage in axes:
        axes[stage].set_title("[STAGE " + stage[-1] + "] Line Plot of Predicted Scores and Actual Scores")
        axes[stage].set_xlabel("Score Type")  # set x label
        axes[stage].set_xticks([1, 2])  # set locations of x ticks
        axes[stage].set_xticklabels(["Predicted", "Actual"])  # set labels of x ticks
        axes[stage].set_ylabel("Stage Scores")  # set y label
        axes[stage].set_ylim([-.5, 1.05])  # set the y axes points

    complete_users = allocation.assignment_util.filter_complete_users(user_scores, skills=["sa", "ni", "ot"], tasks=["s1", "s2", "s3"]).keys()

    # make the allocation matrix
    score_prediction_matrix = {}
    for p in user_scores:  # fit regressions to each user except the evaluated user, to remove bias
        training_user_scores = {user : user_scores[user] for user in user_scores if user != p}
        impact_matrix, yint_matrix, weight_matrix = allocation.assignment_util.generate_impact_matrix(user_scores=training_user_scores, skills=["sa", "ni", "ot"], tasks=["s1", "s2", "s3"])
        score_prediction_matrix[p] = allocation.assignment_util.predict_test_user_performance({p:user_scores[p]}, impact_matrix=impact_matrix, yint_matrix=yint_matrix, weight_matrix=weight_matrix, skills=["sa", "ni", "ot"], tasks=["s1", "s2", "s3"])[p]
        
    # format data into three lists of points (Stage 1, Stage 2, Stage 3)
    mean_pa = 0
    # for each of the 3 stages
    for stage in axes:
        print("Looking at Stage", stage)
        # for each person
        for p in score_prediction_matrix:
            # ignore if they did not complete all tasks
            if p not in complete_users:
                continue

            # plot their line
            x = [1, 2]  # 1 is the predicted score, 2 is the actual score
            y = [score_prediction_matrix[p][stage], user_scores[p][stage]]
            axes[stage].plot(x, y)  # plot a line from the predicted to actual score

        # calculate the ranking accuracy as the ratio of accurate pairwise comparisans
        num_correct = 0
        num_total = 0
        comparisons = []
        for p1 in score_prediction_matrix:
            for p2 in score_prediction_matrix:
                if p1 not in complete_users or p2 not in complete_users:  # discard incomplete users
                    continue
                if p2 == p1:  # discard comparing to oneself
                    continue
                if sorted([p1, p2]) in comparisons:  # discard already seen comparisons
                    continue
                # pairwise comparison
                if score_prediction_matrix[p1][stage] > score_prediction_matrix[p2][stage] and user_scores[p1][stage] > user_scores[p2][stage]:
                    num_correct += 1
                if score_prediction_matrix[p1][stage] < score_prediction_matrix[p2][stage] and user_scores[p1][stage] < user_scores[p2][stage]:
                    num_correct += 1
                if score_prediction_matrix[p1][stage] == score_prediction_matrix[p2][stage] and user_scores[p1][stage] == user_scores[p2][stage]:
                    num_correct += 1
                num_total += 1
                comparisons.append(sorted([p1, p2]))

        print("  Ranking Comparison: Stage", stage, "Num Correct", num_correct, "Total", num_total, "Ratio Correct", round(num_correct / num_total, 5))
        mean_pa += num_correct / num_total / 3

        axes[stage].text(1.8, .05, "PA:" + str(round(num_correct / num_total, 2)))
    print("Mean Pairwise Accurcay (PA):", mean_pa)
    print("Done with the line plot")