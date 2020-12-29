# calculate the score of a given roll of dice.
# takes a list of tree dice and returns the score
#
def score(dice):
    return 25 if (dice[0] == dice[1] and dice[1] == dice[2]) else sum(dice)


# compute "cartesian product" of 3 lists
# - list should be a list of 3 lists
#
def combos3(lists):
    return [ (e1, e2, e3) for e1 in lists[0] for e2 in lists[1] for e3 in lists[2] ]



# calculates the expected score over all successors.
# - roll: current roll
# - reroll: current re-roll strategy being considered (T, F, F)
#
def expectation_of_reroll(roll, reroll):
    #consider all possible outcomes under the given reroll strategy
    # e.g. if roll = (3,4,5), reroll=(T,F,F), consider outcomes 1, 4, 5 2, 4, 5 3, 4, 5 ... 6, 4, 5
    outcomes = combos3( [ ((roll[die],) if not reroll[die] else range(1,7)) for die in range(0,3) ] )
    return sum( [score(outcome) for outcome in outcomes] ) * 1.0 / len(outcomes)


# calculates the maximum score over all its successors
#
#takes a roll (list of 3 dice) and figures the best strategy for rerolling.
#Returns: a tuple with two parts:
# - best re-roll (list of 3 boolean values -- e.g. [true, false, false])
#   means: re-roll first die, but not the second of third
# - expected score for this re-roll strategy
#
def max_layer(roll):
    #consider all possible combinations of rerolls: (fff), (tff), ...
    reroll_scores = [(reroll, expectation_of_reroll(roll, reroll)) for reroll in combos3( ((True, False), )*3 )]

    #find the reroll in reroll_scores with maximum score
    #using a lambda function above, replaces get_second() helper funct
    #lambda essentially serves as name tho technically func is nameless
    #the func gets passed item
    #returns item[1] i.e. second element in the iterable
    return max(reroll_scores, key=lambda item: item[1])


def get_second(item):
    return item[1]

# main program

roll = [1, 2, 6]
(best_reroll, score) = max_layer(roll)
print("I recommend you reroll the following dice: ", best_reroll, "which has expected score of ", score)
