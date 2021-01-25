from matplotlib import pyplot as plt
import numpy as np

path = 'C:/Users/Przemek/Downloads/Discord UE.csv/Discord UE.csv'


def prepare_responses(path):
    with open(path, 'r', encoding='utf8') as raw:
        questions = [q.strip('/"\n') for q in raw.readline().split(sep=',')]
        print(questions)

        # print(len(questions))

        responses = []

        for line in raw:

            response = dict()
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
                        nums = [int(n.strip()) if n.strip() != 'inf' else 'inf' for n in stack.replace(',', ';').split(';')]
                        response[questions[i]] = {'clicks': nums[0], 'time': nums[1], 'hardness': nums[2]}
                    else:
                        response[questions[i]] = stack.strip('/"')

                    stack = ''
                    appending = False
                    i += 1
                else:
                    stack += char

            responses.append(response)

        print()
        for response in responses:
            print(list(response.values()))

    return questions, responses


def create_pie_chart(question, responses):
    answers = list(set(responses))

    # Make a fake dataset:
    height = [responses.count(answers[i]) for i in range(len(answers))]
    bars = list(set(responses))
    y_pos = np.arange(len(bars))

    # Create bars
    plt.bar(y_pos, height)

    # Create names on the x-axis
    plt.xticks(y_pos, bars)

    # Show graphic
    plt.show()


questions, responses = prepare_responses(path)

for i in range(2, 6):
    create_pie_chart(questions[i], [list(response.values())[i] for response in responses])