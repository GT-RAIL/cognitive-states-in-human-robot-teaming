# main.py: manages the data processing, analysis, and results display.

import allocation.assignment_util  # utility functions for the project
import processing.process_questionnaire  # utility functions for the preliminary questionnaire
import plotting.plot_scatter  # functions for plotting the scatter plot of user scores as a skill/task matrix
import plotting.plot_histogram  # functions for plotting the histogram of user scores for each assignment conditions (shown in paper)
import plotting.plot_lines  # functions for plotting lines from the predicted and actual scores
import plotting.plot_nc3  # functions for plotting boxplots of the different score data comparisans
import plotting.plot_ranking  # functions for plotting the ranking bar chart (shown in paper)
import plotting.plot_whiskers  # functions for plotting a box and whisker plot of the predicted vs. actual score difference

from matplotlib import pyplot as plt  # library for plotting


## get the questionnaire results
print("Questionnaire results:", processing.process_questionnaire.get_questionnaire_data("logs"))

## load user data from the user study

# load the user data we used in the study; of the form:
#   { user_id : { "ot": ot_score, "ni": ni_score, "sa": sa_score, "s1": s1_score, "s2": s2_score, "s3": s3_score} }
user_scores = allocation.assignment_util.retrieve_paper_user_scores()

## instead of using the default form presented in the paper (using all tasks, and score data from a user study), 
## you can uncomment one of the below lines to adapt the dataset

# uncomment the below line to use your own user data (by default, in the logs/ directory)
#user_scores = allocation.assignment_util.process_logs()

# uncomment the below line to generate random users instead of the user study collection
#user_scores = allocation.assignment_util.generate_fake_bivariate_user_scores(N=30, R=.0)

# uncomment the below line to zero out the Stage 3 results, since the "stage 3" scenario had only a small correlation
#user_scores = allocation.onehot_allocation.cut_task(user_scores, "s3")

# uncomment the below lines to "oracle" a task/skill pairing, giving the pairing a perfect correlation, we used this to
#   verify the code works as intended
#user_scores = allocation.assignment_util.oracle_task(user_scores, "s1", "ot")
#user_scores = allocation.assignment_util.oracle_task(user_scores, "s2", "ni")
#user_scores = allocation.assignment_util.oracle_task(user_scores, "s3", "sa")


## process the dataset to get the prediction parameters

# from the raw user scores, filter in users who completed all tasks and skills
complete_user_scores = allocation.assignment_util.filter_complete_users(user_scores=user_scores)

# select the correlation coefficient, options are "spearman" and "pearson"
correlation = "spearman"

# the below line is an example of calculating the linear regression slopes (what we termed an "impact matrix"), y-intercepts, and correlation weights
#   the function calculates these prediction parameters for all complete users, but for the paper, we one-hot each possible 3-person team. As
#   such, the below line of code is only useful for debugging and as an example for you, the reader, to understand our process.
impact_matrix, yint_matrix, weight_matrix = allocation.assignment_util.generate_impact_matrix(complete_user_scores, skills=["sa", "ni", "ot"], tasks=["s1", "s2", "s3"], correlation=correlation)

# plot the scatter plot of raw user scores (cognitive skill and task performance), as a 3 x 3 grid of plots
#   by looking at this plot you will notice that the signal is fairly weak, our goal is to extract as much use as possible out of the correlations.
fig_scatter = plotting.plot_scatter.plot_scatter(complete_user_scores, weight_matrix, correlation=correlation)  # correlation variable is only for text

# plot the lines of predicted scores to actual scores, on the bottom right of each plot is a "PA: #.##" note, PA means the pairwise ranking accuracy, a
#   PA of 1.0 means the score is equivalent in both reality and prediction; a PA of 0.0 is a perfectly reversed ordering. This plot shows a number of
#   criss-crossed lines, one per user.
plotting.plot_lines.plot_lines(complete_user_scores)

# generate the scores for each subset of 3 users (one hot teams): this function breaks the complete user set into subsets of 3, and for each team,
#   calculates the impact matrix, yint matrix, and weight matrix, predicts user scores, conducts the role assignment; returns the scores of each possible
#   role allocation of the team, and the predicted best allocation. 
#
#   To generate nC3 results (3c3, 4c3, 5c3), change the sample_size parameter (n); a higher sample_size requires *much* longer processing times, the results are stored into "score_data_{sample_size}c3.pkl"
#
#   parameters:
#       user_scores: all user scores, even those who did not complete all rounds, as they can be used to supplement the dataset (e.g., if a user only did the OT and S1 tests, they are ineligible
#                    for the teams but their data can still be used for modeling the OT/S1 relationship).
#       complete_user_scores: only the users who completed all cognitive skill tests and all robot operation tasks
#       team_size: the number of users from the complete_user_scores pool to pull for each team
#       sample_size: the number of users from the team_size to assign, this allows trialing of "from 3 choose 3" (all users assigned), "from 4 choose 3" (top 3 users assigned from 4 candidates),
#                    "from 5 choose 3" (top 3 users assigned from 5 candidates), and so on.
score_data = allocation.assignment_util.process_users(user_scores=user_scores, complete_user_scores=user_scores, skills=["ot", "ni", "sa"], tasks=["s1", "s2", "s3"], team_size=3, sample_size=3)

# plot the onehot histograms of the known best scores, the known worst scores, the individualized role assignment scores, and the random distribution.
#   setting the parameter split=False will overlay the histograms onto each other, which while more difficult to read, makes for a useful comparison.
fig_histogram = plotting.plot_histogram.plot_histogram(score_data, R=-1, split=True)

# plot the 3c3 (3 choose 3 -- from samples of 3 users, choose 3 to assign) ranking of the individualized role assignment scores compared to all possible allocations; of the six possible assignments (3! = 6), where did our Individualized Role Assignment rank for each team
fig_ranking3c3 = plotting.plot_ranking.plot_ranking_3c3(score_data=score_data, R=-1)

# plot the 3c3 box and whisker plot of the score difference; the score of the IRA allocation compared to the average score of all (3! = 6) possible assignments for the team
fig_whiskers3c3 = plotting.plot_whiskers.plot_whiskers_3c3(score_data=score_data, R=-1)

# plot the nc3 box plots, comparing different sample sizes to each other and to random assignment, note that this requires score_data_{n}c3.pkl files to be generated (see the score_data variable above)
fig_boxplotsnc3 = plotting.plot_nc3.plot_nc3()

print("Done loading plots, now showing.")

# show the plots
plt.show()
