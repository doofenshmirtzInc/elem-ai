# calculate the score of a given roll of dice.
# takes a list of tree dice and returns the score
#
def score(dice):
    return 25 if (dice[0] == dice[1] and dice[1] == dice[2]) else sum(dice)


# calculates the expected score over all successors.
# - roll: current roll
# - reroll: current re-roll strategy being considered (T, F, F)
#
def expectation_of_reroll(roll, reroll):
    #consider all possible outcomes under the given reroll strategy
    # e.g. if roll = (3,4,5), reroll=(T,F,F), consider outcomes 1, 4, 5 2, 4, 5 3, 4, 5 ... 6, 4, 5
    exp = 0
    outcome_count = 0
    # assigns outcome_a = roll[0] if reroll[0] is false else loops thru range(1,7)
    # same for all subsequent outcomes, indices merely change
    for outcome_a in ((roll[0],) if not reroll[0] else range(1,7)):
        for outcome_b in ((roll[1],) if not reroll[1] else range(1,7)):
            for outcome_c in ((roll[2],) if not reroll[2] else range(1,7)):
                exp += score( (outcome_a, outcome_b, outcome_c) )
                outcome_count += 1

    return exp * 1.0 / outcome_count






# calculates the maximum score over all its successors
#
#takes a roll (list of 3 dice) and figures the best strategy for rerolling.
#Returns: a tuple with two parts:
# - best re-roll (list of 3 boolean values -- e.g. [true, false, false])
#   means: re-roll first die, but not the second of third
# - expected score for this re-roll strategy
#
def max_layer(roll):
    max_so_far = (0, 0)
    #consider all possible combos of re-rolls: (f,f,f), (t,f,f), ...
    for roll_a in (True, False):
        for roll_b in (True, False):
            for roll_c in (True, False):
                #compute expected score over all possible re-rolls
                exp_score = expectation_of_reroll(roll, (roll_a, roll_b, roll_c))
                print((exp_score, (roll_a, roll_b, roll_c)))
                if exp_score > max_so_far[1]:
                    max_so_far = ((roll_a, roll_b, roll_c), exp_score)

    return max_so_far



# main program

roll = [6,6,5]
(best_reroll, score) = max_layer(roll)
print("I recommend you reroll the following dice: ", best_reroll, "which has expected score of ", score)
