# ---------------------------------------------------------------------------------------------------------------------#
# Author: Sailesh Acharya
# Data: 2023-03-09
# Project name: Ranked choice analysis between human-driven vehicles (hv),
# autonomous vehicles (av), and teleportation (tp).

# This script compares the travel time usefulness and travel-based activities
# in the HV and AV travel. The data is # collected from a survey of US national 
# park visitors.
# ---------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#
# import modules
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mtick
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import ttest_rel


# import data
df = pd.read_pickle("../data/processed/prepared_data.pkl")
df = df.drop_duplicates(subset=['id'], keep='first')
df.describe
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
## chi-square tests of travel based activities
# list of activity columns
activities = [
    "tba_g1",
    "tba_g2",
    "tba_g3",
    "tba_g4",
    "tba_g5",
    "tba_g6",
    "tba_g7"
]

# significance level
alpha = 0.05  

# chi-square test
for activity in activities:
    # columns for AV and HV preferences
    av_column = f"{activity}_av_d"
    hv_column = f"{activity}_hv_d"

    # create contingency table
    contingency_table = pd.crosstab(df[av_column], df[hv_column])

    # perform chi-squared test
    chi2, p, _, _ = chi2_contingency(contingency_table)

    print(f"Activity: {activity}")
    print(f"Chi-squared statistic: {chi2}")
    print(f"P-value: {p}")

    if p < alpha:
        print("Reject the null hypothesis: Preference is different between AV and HV.")
    else:
        print("Fail to reject the null hypothesis: Preference is similar between AV and HV.")

    print("\n")
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
## plot of travel based activities
# prepare data
columns = [
    "tba_g1_av_d", "tba_g2_av_d", "tba_g3_av_d",
    "tba_g4_av_d", "tba_g5_av_d", "tba_g6_av_d",
    "tba_g7_av_d", "tba_g1_hv_d", "tba_g2_hv_d",
    "tba_g3_hv_d", "tba_g4_hv_d", "tba_g5_hv_d",
    "tba_g6_hv_d", "tba_g7_hv_d"
]
tba = (
    pd.DataFrame(
        {
            "mode": [col.split('_')[2] for col in columns],
            "activity": [col.split('_')[1] for col in columns],
            "percentage": (df[columns].sum() / len(df)) * 100,
            "count": df[columns].sum(),
        }
    )
)

# sort the activites 
tba['activity'] = pd.Categorical(tba['activity'], categories=['g3','g6', 'g7', 'g5', 'g4', 'g2', 'g1'], ordered=True)
tba = tba.sort_values('activity')
print(tba)

# set the font properties
font_path = fm.findfont(fm.FontProperties(family='Times New Roman'))
font_prop = fm.FontProperties(fname=font_path, size=10)

# define new x-axis labels
x_labels = {
    'g1': 'Use social \nmedia',
    'g2': 'Work/study/\nread',
    'g3': 'Interact',
    'g4': 'Entertain',
    'g5': 'Eat/care',
    'g6': 'Relax',
    'g7': 'Watch road'
}

# pivot
pivot_tba = tba.pivot(index='activity', columns='mode', values='percentage')
ax = pivot_tba.plot(kind='bar', figsize=(6.27, 4))

# modify legend labels
legend = ax.legend(title='Mode')
legend.set_title("", prop=font_prop)
legend.set_frame_on(False)

# rename legend labels
legend_labels = ['AV', 'HV']
for text, label in zip(legend.get_texts(), legend_labels):
    text.set_text(label)
    text.set_fontproperties(font_prop)

# add black boxes around legend keys
for handle in legend.legendHandles:
    handle.set_edgecolor('black')
plt.setp(legend.get_texts(), color='black')

# add data labels to the bars
for p in ax.patches:
    value = p.get_height()
    new_label = f'{int(696/100 * value)}'
    ax.annotate(new_label, (p.get_x() + p.get_width() / 2., value),
                ha='center', va='center', fontsize=10, fontproperties=font_prop,
                color='black', xytext=(0, 5), textcoords='offset points')

# make x-axis labels horizontal and set the new labels
ax.set_xticklabels([x_labels[label.get_text()] for label in ax.get_xticklabels()], rotation=0, fontproperties=font_prop)
ax.tick_params(axis='x', which='both', length=0)
ax.set_xlabel(None)

# add percentage sign to y-axis labels
ax.yaxis.set_major_formatter(mtick.PercentFormatter())

# save the plot
plt.tight_layout()
plt.savefig('../outputs/TBA_plot.png', dpi=3000, bbox_inches='tight')
plt.show()
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
## t-test of travel time usefulness

# paired sample t-test
t_statistic, p_value = ttest_rel(df['tu_av'], df['tu_hv'])

# significance level
alpha = 0.05  

# result
print(f"T-Statistic: {t_statistic}")
print(f"P-Value: {p_value}")
if p_value < alpha:
    print("Reject the null hypothesis: Travel time usefulness is different between AV and HV.")
else:
    print("Fail to reject the null hypothesis: Travel time usefulness is similar between AV and HV.")
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
## plot of travel time usefulness

# set the font
font_path = fm.findfont(fm.FontProperties(family="Times New Roman"))
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10

# prepare data
ttu = df[["tu_hv", "tu_av"]]
category_counts_hv = ttu['tu_hv'].value_counts()
category_percentages_hv = category_counts_hv / len(ttu) * 100
category_counts_av = ttu['tu_av'].value_counts()
category_percentages_av = category_counts_av / len(ttu) * 100
colors = ['#0571b0', '#92c5de', '#f7f7f7', '#f4a582', '#ca0020']

# set up figure and axis with margins
fig, ax = plt.subplots(figsize=(6.27, 1.43))  
left_hv, left_av = 0, 0
for i, (category_hv, percentage_hv) in enumerate(category_percentages_hv.items()):
    label_value_hv = 696 * percentage_hv / 100
    ax.barh(0, percentage_hv, color=colors[i], left=left_hv)
    left_hv += percentage_hv
    ax.text(left_hv - percentage_hv / 2, 0, f'{int(label_value_hv)}', ha='center', va='center', color='black')

for i, (category_av, percentage_av) in enumerate(category_percentages_av.items()):
    label_value_av = 696 * percentage_av / 100
    ax.barh(1, percentage_av, color=colors[i], left=left_av)
    left_av += percentage_av
    ax.text(left_av - percentage_av / 2, 1, f'{int(label_value_av)}', ha='center', va='center', color='black')
ax.set_yticks([0, 1])
ax.set_yticklabels(['TTU in HV travel', 'TTU in AV travel'])
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
ax.set_xlim(0, 100)
ax.invert_yaxis()
ax.tick_params(axis='y', which='both', length=0)

# adjust legend position
legend = ax.legend(labels=['Mostly \nuseful', 'Somewhat \nuseful', 'Neither', 'Somewhat \nwasted', 'Mostly \nwasted'],
                    bbox_to_anchor=(0.45, -0.15),
                    loc='upper center',
                    ncol=5,
                    frameon=False,
                    edgecolor='black')

# add black boxes around legend keys
for handle in legend.legendHandles:
    handle.set_edgecolor('black')
plt.setp(legend.get_texts(), color='black')

# Save the figure with proper DPI
plt.savefig('../outputs/TTU_plot.png', dpi=3000, bbox_inches='tight')
plt.show()
# ---------------------------------------------------------------------------------------------------------------------#





