import pandas as pd


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
    q = len(responses)
    answers = list(set(responses))

    index = [responses.count(answers[i]) for i in range(q)]

    # --- dataset 1: just 4 values for 4 groups:
    df = pd.DataFrame(responses, index=index, columns=['x'])

    # make the plot
    df.plot(kind='pie', subplots=True, figsize=(8, 8))


questions, responses = prepare_responses(path)

for i in range(2, 6):
    create_pie_chart(questions[i], [response[i] for response in responses])