#!/usr/local/bin/python3

# put your group assignment program here!
import sys
import os
import random

def evaluate_groups(groups, k, m, n, preferences):
    set_of_groups = set()
    score = 0
    for person in groups:
        person_group_string = '-'.join(groups[person])
        if person_group_string not in set_of_groups:
            set_of_groups.add(person_group_string)
        if len(groups[person]) > len(preferences[person]):
            score += 1
        for member in preferences[person][0]:
            if member not in groups[person]:
                score += n
        for member in preferences[person][1]:
            if member in groups[person]:
                score += m
    score += k * len(set_of_groups)
    return score, set_of_groups


def parse_file(input_file):

    with open(input_file) as f:
        lines = f.readlines()

    input_data = {line.split()[0]: [line.split()[1].split('-'),
                                    line.split()[2].split(',')]
                  for line in lines}

    return input_data


def random_group(people):
    random.shuffle(people)
    number_of_groups = int(len(people) / 3) + 1
    groupings = []
    for i in range(number_of_groups-1):
        groupings.append(people[3*i:3*(i+1)])
    groupings.append(people[3*(number_of_groups-1):])
    groups = {}
    for group in groupings:
        for person in group:
            groups[person] = set(group)
    return groups


def generate_groups(people):
    random.shuffle(people)
    groupings = []
    while people:
        group_size = min(random.randint(1,3), len(people))
        groupings.append(people[0:group_size])
        people = people[group_size:]
    groups = {}
    for group in groupings:
        for person in group:
            groups[person] = set(group)
    return groups


def max_time(people):
    length = len(people)
    times = length
    while length > 1:
        length -= 1
        times = times * length
    return times


def main(input_file, k, m, n):
    preferences = parse_file(input_file)
    people = [person for person in preferences]
    max_tries = max_time(people)
    print(people)
    #visited = {}
    fringe = [random_group(people)]
    best_set_of_groups = fringe[0]
    best_score, best_set_of_groups = evaluate_groups(best_set_of_groups,
                                                     k, m, n,
                                                     preferences)
    print('\n'.join(best_set_of_groups))
    print(best_score)

    # Go through loop
    count = 0
    while True and count < max_tries:
        count += 1
        groups = generate_groups(people)
        score, set_of_groups = evaluate_groups(groups, k, m, n, preferences)
        if score < best_score:
            best_score = score
            best_set_of_groups = set_of_groups
            print()
            print('\n'.join(best_set_of_groups))
            print(best_score)

    return


if __name__ == '__main__':

    input_file, k, m, n = sys.argv[1:]

    try:
        # Minutes per Team
        k = int(k)
        # Minutes per student who is with someone they requested to not be with
        m = int(m)
        # Minutes per student who is not with someone they requested
        n = int(n)
    except:
        print('k, m, and n must be integer values.')

    if not os.path.exists(input_file):
        print(f'{input_file} does not exist. Please select an input file.')
        raise Exception(f'''file '{input_file}' not found.''')

    main(input_file, k, m, n)
