# analyzes the data to determine the results

from statistics import median, stdev
from turtle import pd
import allocation.assignment_util
import allocation.onehot_allocation
from matplotlib import pyplot as plt
import seaborn
import numpy as np
import pandas as pd


# calculate the pairwise ranking, plot distribution of performance difference between actual scores and skill based

def plot_ranking_3c3(score_data, R=-1):
    print("---------- Plotting the histogram of IRA assignment's rank compared to all 6 possible assignments ----------")

    ranks_ira = []  # IRA performance rank compared to all assignments
    outperform = 0  # num outperform expected value

    # result: [best_value, pred_value, adjusted_pred_value, actual_value, worst_value, expected_value, [x for x in all_assignments]]
    for result in score_data:  # pull each possible team, in the form of indexes instead of IDs
        # determine the rank of the IRA predictions
        rank = list(reversed(sorted([round(x, 5) for x in result[-1]]))).index(round(result[3], 5)) + 1
        ranks_ira.append(rank)

        # determine if IRA outperformed average, if so increment the outperform count
        outperform = outperform + 1 if result[3] > sum(result[-1]) / len(result[-1]) else outperform

    # set up the rank bins
    r1 = 0
    r2 = 0 
    r3 = 0
    r4 = 0 
    r5 = 0
    r6 = 0

    # add values to the rank bins
    for x in ranks_ira:
        r1 += 1 if x == 1 else 0
        r2 += 1 if x == 2 else 0
        r3 += 1 if x == 3 else 0
        r4 += 1 if x == 4 else 0
        r5 += 1 if x == 5 else 0
        r6 += 1 if x == 6 else 0

    N = len(ranks_ira)
    print("3c3 Rank Distribution:", "#1:", r1, "(" + str(r1 / N) + ")", "#2:", r2, "(" + str(r2 / N) + ")", "#3:", r3, "(" + str(r3 / N) + ")", "#4:", r4, "(" + str(r4 / N) + ")", "#5:", r5, "(" + str(r5 / N) + ")", "#6:", r6, "(" + str(r6 / N) + ")", "Mean:", sum(ranks_ira) / len(ranks_ira), "Median:", median(ranks_ira), "Outperform:", outperform, "(" + str(outperform / N) + ")")
    
    # format into a data frame
    data = pd.DataFrame({"Rank": range(0, 7),
                        "Team Count": [0, r1, r2, r3, r4, r5, r6],
                        })

    plt.figure()  # create a new figure for this plot
    bar = seaborn.barplot(x="Rank", y="Team Count", data=data, palette="Blues", hue="Team Count", dodge=False)
    bar.set_label("_nolegend_")

    plt.plot([0.4, 6.4], [len(ranks_ira) / 6, len(ranks_ira) / 6], alpha=0.6, color="goldenrod", linewidth=8, label="Expected Value with Random Assignment")  # plot a yellow line at the expected value mark (# teams / 6, as random would by expected to evenly distribute teams)

    # set the plot settings
    axis_fontsize = 25
    plt.ylabel("Proportion of Teams", fontsize=axis_fontsize)
    plt.xlabel("Rank of Individualized Role Assignment Compared to All Possible Role Assignments", fontsize=axis_fontsize)
    axis = plt.gca()
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)
    plt.xticks(fontsize=axis_fontsize-5)
    y_labels = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    plt.yticks([N*x for x in y_labels], labels=[str(x) for x in y_labels], fontsize=axis_fontsize-5)
        
    plt.xlim([0.5,6.5])
    
    plt.legend(fontsize=axis_fontsize-5, frameon=False)






