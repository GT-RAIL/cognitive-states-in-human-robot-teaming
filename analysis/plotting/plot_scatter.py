from matplotlib import pyplot as plt
import scipy.stats

# plots the user scores as a 3x3 plot of skills and tasks
def plot_scatter(user_scores, weight_matrix, correlation="spearman"):
    s1 = []
    s2 = []
    s3 = []
    ot = []
    ni = []
    sa = []

    for p in user_scores:
        s1.append(user_scores[p]["s1"])
        s2.append(user_scores[p]["s2"])
        s3.append(user_scores[p]["s3"])
        ot.append(user_scores[p]["ot"])
        ni.append(user_scores[p]["ni"])
        sa.append(user_scores[p]["sa"])

    # scatterplot each relationship
    skills = ["Object Tracking", "Network Inference", "Situational Awareness"]
    skills_short = ["ot", "ni", "sa"]
    tasks = ["Task 1", "Task 2", "Task 3"]
    tasks_short = ["s1", "s2", "s3"]

    fig, axes = plt.subplots(nrows=3, ncols=3)

    ni = [x / 70 for x in ni]

    axes[0][0].scatter(ot, s1)
    axes[0][1].scatter(ni, s1)
    axes[0][2].scatter(sa, s1)
    axes[1][0].scatter(ot, s2)
    axes[1][1].scatter(ni, s2)
    axes[1][2].scatter(sa, s2)
    axes[2][0].scatter(ot, s3)
    axes[2][1].scatter(ni, s3)
    axes[2][2].scatter(sa, s3)

    # set the visuals for each plot
    for row in range(len(axes)):
        for col in range(len(axes[row])):
            if row == 2:
                axes[row][col].set_xlabel(skills[col], fontsize=15)
            if col == 0:
                axes[row][col].set_ylabel(tasks[row], fontsize=15)
    
            axes[row][col].set_xlim([0,1] if skills[col] != "Network Inference" else [0,1])  # commented this out because NI is no longer from 0 to 1
            axes[row][col].set_ylim([0,1])
            cs = axes[row][col].collections[0]
            data = cs.get_offsets()
            #axes[row][col].text(.8, .05, "R_" + (correlation[0]) + "=" + str(round(weight_matrix[skills_short[col]][tasks_short[row]], 3)))

    return fig
