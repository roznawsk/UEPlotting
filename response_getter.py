def get_values(answer):
    return [int(n.strip()) if n.strip() != 'inf' else 'inf' for n in answer.strip('/"').split(';')]


path = 'C:/Users/Przemek/Downloads/Discord UE.csv/Discord UE.csv'

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


