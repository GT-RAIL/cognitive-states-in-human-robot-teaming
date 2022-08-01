from matplotlib import pyplot as plt
import scipy.stats
import itertools
import numpy
import seaborn

# plots the histograms of team assignment scores
def plot_histogram(iteration_scores, R=-1, split=False):
    print("---------- Plotting the score distribution histograms ----------")
    # format data into histogram distributions
    data = [[x[i] for x in iteration_scores] for i in range(len(iteration_scores[0])-1)]  # -1 to not consider the last (all possibilities)
    all_assignments = sorted(list(itertools.chain.from_iterable([x[-1] for x in iteration_scores])))
    data[3] = sorted(data[3])
    data[0] = sorted(data[0])
    data[4] = sorted(data[4])

    # as an aside, determine how skill-based compares to all-assignments within a 3-user group
    ira_wins = 0  # count of skill-based wins
    all_wins = 0  # count of all-assignment wins
    tie = 0  # count of ties
    todos = [x[-1] for x in iteration_scores]  # all possible assignments for each set of 3 users (6)
    for d in range(len(data[0])):  # for each set of 3 users
        ira = data[3][d]  # pull their skill-based score
        for all in todos[d]:  # for each possible score for that set
            if ira > all:  # if skill-based wins
                ira_wins += 1
            if ira == all:  # if they tie (should be >= num of 3 user sets, 3276)
                tie += 1
            if ira < all:  # if all-assignment wins
                all_wins += 1

    print("Winnings: ira", ira_wins, "ALL", all_wins, "TIE", tie, "%tile", round(ira_wins / (ira_wins + all_wins), 4))
    print("Averages: M_all", sum(all_assignments) / len(all_assignments), "M_ira", sum(data[3]) / len(data[3]))

    bins = 50  # number of bins
    alpha = 0.5  # transparency (for when the "split" parameter is FALSE -- plots are overlayed)

    (_, bins) = numpy.histogram(all_assignments, bins=bins)  # create a numpy histogram from the scores

    # generate the subplots -- 4 if we are splitting, 1 if we are not
    fig, axes = plt.subplots(nrows=4 if split else 1, ncols=1)
    if not isinstance(axes, numpy.ndarray):
        axes = [axes, axes, axes, axes]  # when not splitting, still split the axes so the below code is compatible for both split and unsplit

    # create the plots
    seaborn.histplot(ax=axes[0], data=all_assignments, bins=bins, alpha=alpha, color="orange", linewidth=0, label="Random Assignment")
    seaborn.histplot(ax=axes[1], data=data[4], bins=bins, alpha=alpha, color="red", linewidth=0, edgecolor="red", label="Observed Worst Assignment")
    seaborn.histplot(ax=axes[2], data=data[0], bins=bins, alpha=alpha, color="green", linewidth=0, edgecolor="green", label="Observed Best Assignment")  # histogram for best scores
    seaborn.histplot(ax=axes[3], data=data[3], bins=bins, alpha=alpha, color="blue", linewidth=0, edgecolor="blue", label="Individualized Role Assignment")  # histogram for predicted actual

    # calculate the median values
    medians =   [all_assignments[len(all_assignments) // 2] if len(all_assignments) % 2 == 0 else (all_assignments[len(all_assignments) // 2] + all_assignments[len(all_assignments) // 2 + 1]) / 2,
                 data[4][len(data[4]) // 2] if len(data[4]) % 2 == 0 else (data[4][len(data[4]) // 2] + data[4][len(data[4]) // 2 + 1]) / 2,
                 data[0][len(data[0]) // 2] if len(data[0]) % 2 == 0 else (data[0][len(data[0]) // 2] + data[0][len(data[0]) // 2 + 1]) / 2,
                 data[3][len(data[3]) // 2] if len(data[3]) % 2 == 0 else (data[3][len(data[3]) // 2] + data[3][len(data[3]) // 2 + 1]) / 2]

    # set the y limit 
    ymax_normal = 548.10  # desired ymax
    ymax_all = ymax_normal * 6  # since the all_assignments (random) has 6 times more items than the others, normalize it to the desired ymax

    # plot details
    plot_labels = ["A", "B", "C", "D"]
    axis_fontsize = 15
    plt.xticks(fontsize=axis_fontsize-5)
    plt.yticks(fontsize=axis_fontsize-5)
    plt.legend(fontsize=axis_fontsize-5)

    # format each of the plots (or axes)
    for ax in range(len(axes)):
        axis = axes[ax]
        axis.spines['right'].set_visible(False)  # remove the right box line
        axis.spines['top'].set_visible(False)  # remove the left box line
        axis.legend(frameon=False, fontsize=axis_fontsize)  # create the legend
        median = medians[ax]  # note the median line
        
        # if splitting the plots, set the median marks and tick labels
        if split:
            if ax == 3:  # place text on the skill-based plot
                axis.set_xlabel("Cumulative Performance Score")

            if ax == 0:  # scale the y axis of the all assignments plot to maintain constant volume 
                axis.set_ylim([0, ymax_all])
                axis.set_yticks([600, 1800, 3000])
                # plot the median
                median_y = [0, 2400]
                axis.text(median + 0.05, 350 * 6, "median: " + str(round(median, 2)), fontsize=axis_fontsize-5)
                text_height = 400 * 6
            else:
                axis.set_ylim([0, ymax_normal])
                axis.set_yticks([100, 300, 500])
                # plot the median
                median_y = [0, 400]
                axis.text(median + 0.05, 350, "median: " + str(round(median, 2)), fontsize=axis_fontsize-5)
                text_height = 400

            axis.set_yticklabels([0.03, 0.09, .15])
            axis.plot([median, median], median_y, color="grey", marker = '')  # plot the median line

            if R != -1:
                axis.set_xlabel("[Assigning 3 Generated Users" + (", target r^2 of " + str(R) if R != -1 else "") + "]Team Assignment Scores of " + ("Known Worst" if ax == 0 else "Known Best" if ax == 1 else "All Possible" if ax == 2 else "Skill-Based") + " Assignment")  # set x label
            else:
                pass

            axis.set_xlim([0, 3])  # set locations of x ticks
            axis.set_ylabel("Proportion of Teams", fontsize=axis_fontsize)  # set y label
            axis.text(0.1, text_height, plot_labels[ax], fontsize=25)
            

        # when not splitting plots, only need to set info for the first plot
        else:
            if ax > 0:  # only need to set plot info for the first
                continue
            if R != -1:
                axis.set_title("[Assigning 3 Generated Users" + (", target r^2 of " + str(R) if R != -1 else "") + "] Histogram of Scores via Assignment Methods with all Skills Applied, N=" + str(len(data[0])))
            else:
                axis.set_title("[Assigning 3 Users] Histogram of Scores with all Skills Applied, N=" + str(len(data[0])))
            axis.set_xlabel("Team Assignment Score")  # set x label
            axis.set_xlim([0.01, 3])  # set locations of x ticks
            axis.set_ylabel("Number of Teams")  # set y label
        
    return fig

