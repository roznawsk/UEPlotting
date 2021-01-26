from matplotlib import pyplot as plt
import numpy as np
import random
import textwrap

path = 'C:/Users/Przemek/Downloads/Discord UE.csv/Discord UE.csv'
theme_colors = ['#FFFFFF', '#9FFFF5', '#E6E6E6']
# graph_colors_table = ['#FF5A5F', '#54494B', '#7C9299', '#543438', '#DC832C', '#0E6267', '#1C5A71',
#                       '#1C5A71', '#7EC199', '#CD413B', '#39224B']

graph_colors_table = ['#2F3340', '#E3C15B']


def graph_colors(q):
    return random.sample(graph_colors_table, q)


def prepare_responses(path):
    with open(path, 'r', encoding='utf8') as raw:
        questions = [q.strip('/"\n') for q in raw.readline().split(sep=',')]

        # print(len(questions))

        responses = []

        for line in raw:

            response = []
            stack = ''
            appending = False
            i = 0
            for char in line:
                if not appending and char == '\"':
                    appending = True
                elif not stack and char == ',':
                    continue
                elif appending and char == '\"':
                    if ',' in stack or ';' in stack:
                        nums = [int(n.strip()) if n.strip() != 'inf' else 'inf' for n in
                                stack.replace(',', ';').split(';')]
                        response.append({'clicks': nums[0], 'time': nums[1], 'hardness': nums[2]})
                    else:
                        response.append(stack.strip('/"'))

                    stack = ''
                    appending = False
                    i += 1
                else:
                    stack += char

            responses.append(response)

    return questions, responses


def create_bar_chart(groups, values, title, ylabel='', scale='absolute'):
    n = len(groups['names'])

    if scale == 'absolute':
        mult = 1
    elif scale == 'percent':
        mult = 100 / len(values)

    height = [sum([1 for v in values if v in groups['content'][i]]) * mult for i in range(n)]
    bars = [textwrap.fill(name, 18) for name in groups['names']]
    y_pos = np.arange(len(bars))

    fig, ax = plt.subplots(nrows=1, ncols=1)

    ax.bar(y_pos, height, color=graph_colors(n))
    plt.ylabel(ylabel)
    plt.xticks(y_pos, bars)
    plt.title(title)

    ax.set_facecolor(theme_colors[2])
    fig.set_facecolor(theme_colors[0])

    # Show graphic
    plt.show()


def create_bar_chart_v2(groups, values, title, limits, labels, xlabel='', ylabel='', colors='blue'):
    n = len(groups['names'])

    bar_width = 0.75 / len(values)
    bar_shift = 1.1

    x_labels = [textwrap.fill(name, 18) for name in groups['names']]

    fig, ax = plt.subplots(nrows=1, ncols=1)
    y_pos = [np.arange(len(x_labels))]

    for i in range(1, len(values)):
        y_pos.append([y_pos[i - 1][j] + bar_width * bar_shift for j in range(len(y_pos[i - 1]))])

    for i, v in enumerate(values):
        ax.bar(y_pos[i], v, color=colors[i], width=bar_width, label=labels[i])

    y_mid = [y + bar_width * bar_shift * ((len(y_pos) - 1) / 2) for y in y_pos[0]]

    plt.ylim(limits)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(y_mid, x_labels)
    plt.title(title)

    ax.set_facecolor(theme_colors[2])
    fig.set_facecolor(theme_colors[0])

    # Show graphic
    plt.legend()
    plt.show()


def get_average_values(q_indices, p_indices, data_type):
    groups = {'names': []}
    values = []

    for i in q_indices:
        groups['names'].append(str(i))

        data = [responses[j][i][data_type] for j in p_indices
                  if (responses[j][i] and responses[j][i][data_type] != 'inf')]

        avg = sum(data) / len(data)

        values.append(avg)
    return groups, values


# task group names
# total = 32 tasks

admin = [7, 12, 13, 14, 15, 16, 17, 20, 23, 26, 27]  # 11
friend = [6, 8, 10, 28]  # 4
communication = [9, 11, 18, 21, 22, 24, 25, 36]  # 8
settings = [19, 29, 30, 31, 32, 33, 34, 35, 37]  # 9


''' Here begins the graph drawing '''

questions, responses = prepare_responses(path)

# people

noobs = [i for i in range(len(responses)) if responses[i][5] in
         ['Jest to moje pierwsze zetknięcie z tym programem', 'Zdarzyło mi się kiedyś korzystać']]

pros = [i for i in range(len(responses)) if responses[i][5] == 'Korzystam praktycznie codziennie']

print(noobs)
print(pros)

print(questions)
print()
for response in responses:
    print(response)

# #sex
# groups = {'names': ['Women', 'Men'], 'content': ['Kobieta', 'Mężczyzna']}
# create_bar_chart(groups, [r[3] for r in responses], 'Sex', 'Count')

#
# #age
# groups = {'names': ['<=18', '19-22', '>22'], 'content': [range(0, 19), range(19, 23), range(23, 100)]}
# create_bar_chart(groups, [int(r[2]) for r in responses], 'Age', 'Count')
#
# #time on computer
# groups = {'names': ['<1', '1 - 2', '2 - 3', '3 - 5', '>5'], 'content': ['< 1', '1 - 2', '2 - 3', '3 - 5', '> 5']}
# create_bar_chart(groups, [r[4] for r in responses], 'Time spent using computer daily', 'Count')
#
# #familiarity
# groups = {'names': ['It\'s my first encounter with Discord', 'I have used it a few times',
#                     'I use it from time to time', 'I use Discord practically every day'],
#           'content': ['Jest to moje pierwsze zetknięcie z tym programem', 'Zdarzyło mi się kiedyś korzystać',
#                       'Korzystam sporadycznie', 'Korzystam praktycznie codziennie']}
# create_bar_chart(groups, [r[5] for r in responses], 'Familiarity with discord', 'Count')


for i in friend:
    print(questions[i])

names = ['Server administration tasks', 'Friends related tasks', 'Communication tasks', 'User settings tasks']

limits = {'clicks': (0, 25), 'time': (0, 210), 'hardness': (0.8, 5)}
labels = ['New users', 'Long time users']
xlabel = 'task number'

colors = graph_colors(2)
for category, name in zip([admin, friend, communication, settings], names):

    for data_type in ['clicks', 'time', 'hardness']:
        # averages for everybody
        p_indices = noobs + pros
        groups, values = get_average_values(category, p_indices, data_type)
        create_bar_chart_v2(groups, [values], name, limits[data_type], ['All users'], xlabel, data_type, [colors[0]])

        # averages by group
        _, values_n = get_average_values(category, noobs, data_type)
        groups, values_p = get_average_values(category, pros, data_type)
        create_bar_chart_v2(groups, [values_n, values_p], name, limits[data_type], labels, xlabel, data_type, colors[0:2])
