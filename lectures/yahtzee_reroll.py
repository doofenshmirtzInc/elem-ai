#author: jack mcshane
#class: Elements of Artificial Intelligence
"""
Description:
This program is meant to determine the number of dice (out of 3) that should be rerolled after a particular
yahtzee roll.
"""




#definitions
#determines the most promising reroll for given roll
def choose_reroll(roll):
    if eval(roll) == 25:
        return None

    poss_reroll = [[], [0], [1], [2], [0,1], [0,2], [1,2], [0,1,2]]
    #poss_reroll = [tuple(), tuple(0), tuple(1), tuple(2), tuple(0,1), tuple(0,2), tuple(1,2), tuple(0,1,2)]
    #poss_reroll = [tuple(), tuple(0), (1), (2), (0,1), (0,2), (1,2), (0,1,2)]
    exp_values = []
    for reroll in poss_reroll:
        exp_values.append(expected_value(roll, reroll))

    print(exp_values)
    winner = max(exp_values)
    print(winner)
    winner_index = exp_values.index(winner)
    print(winner_index)

    return (poss_reroll[winner_index], winner)


##evaluate score of the role
def eval(roll):
    yahtzee = 25
    if all(elem == roll[0] for elem in roll):
        return yahtzee

    return sum(roll)



#calc expected val of a reroll given the roll
def expected_value(roll, reroll):
    #if reroll == None:
        #return eval(roll)

    exval = 0
    num_rerolls = len(reroll)
    new_roll = roll.copy()
    poss_rolls = [i for i in range(1,7)]
    prob = [(1/6)**0, (1/6)**1, (1/6)**2, (1/6)**3]

    print(f'roll:{roll}')
    print('possible rerolls:')
    if num_rerolls == 0:
        #print('None')
        return eval(new_roll)

    if num_rerolls == 1:
        for first_roll in poss_rolls:
            new_roll[reroll[0]] = first_roll
            print(new_roll)
            exval += eval(new_roll) * prob[num_rerolls]

    elif num_rerolls == 2:
        d1, d2 = reroll
        for first_roll in poss_rolls:
            new_roll[d1] = first_roll
            for sec_roll in poss_rolls:
                new_roll[d2] = sec_roll
                #print(roll)
                exval += eval(new_roll) * prob[num_rerolls]

    else:
        d1, d2, d3 = reroll
        for first_roll in poss_rolls:
            new_roll[d1] = first_roll
            for sec_roll in poss_rolls:
                new_roll[d2] = sec_roll
                for third_roll in poss_rolls:
                    new_roll[d3] = third_roll
                    #print(roll)
                    exval += eval(new_roll) * prob[num_rerolls]

    return exval









#driver code
roll_str = input('Enter the value of each die separated by a space: ')
#convert input string to list of integer values for processing
roll = [int(num) for num in roll_str.split()]
die, exval = choose_reroll(roll)
print(f'You should reroll die:{die}')
print(f'Rerolling gives and expected value of: {exval}')

