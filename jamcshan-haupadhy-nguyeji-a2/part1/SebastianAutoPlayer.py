# Automatic Sebastian game player
# B551 Fall 2020
# Jack McShane (jamcshan@iu.edu)
#
# Based on skeleton code by D. Crandall
#
#
# This is the file you should modify to create your new smart player.
# The main program calls this program three times for each turn.
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list
#      of dice indices that should be re-rolled.
#
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from SebastianState import Dice
from SebastianState import Scorecard
import random

class SebastianAutoPlayer:

      def __init__(self):
          self.poss_rerolls = self.gen_possible_rerolls( ((True,False),)*5 )

      def first_roll(self, roll, scorecard):

          self.avail_categories = self.get_possible_categories(scorecard)
          self.first_reroll = max( [(self.calc_expected_val(roll.dice, reroll, scorecard), reroll) for reroll in self.poss_rerolls] )
          #convert true falses to list of dice dice to be rerolled
          die = []
          for i in range(0,len(self.first_reroll[1])):
              if self.first_reroll[1][i]:
                  die.append(i)
          return die


      def second_roll(self, roll, scorecard):
          if not self.first_reroll:
              return self.first_reroll

          self.second_reroll = max( [(self.calc_expected_val(roll.dice, reroll, scorecard), reroll) for reroll in self.poss_rerolls] )
          #convert true falses to list of dice dice to be rerolled
          die = []
          for i in range(0,len(self.second_reroll[1])):
              if self.second_reroll[1][i]:
                  die.append(i)
          return die


      def third_roll(self, roll, scorecard):
            return max( [(self.score(roll.dice, cat, scorecard), cat) for cat in self.avail_categories] )[1]


      # Calculate the expected value of a reroll
      # -input: dice object, reroll combination
      # -ouput: expected value of a given reroll
      #
      def calc_expected_val(self, dice, reroll, scorecard):
          outcome_scores = [max( [self.score(outcome, cat, scorecard) for cat in self.avail_categories] ) for outcome in self.gen_possible_rerolls( [ ((dice[die],) if not reroll[die] else range(1,7)) for die in range(0,5) ] )]
          return sum( outcome_scores ) * 1.0 / len(outcome_scores)





      # Generates the possible categories that the current roll could be classified under.
      # This includes categories for which it would score 0
      # -input: scorecard object
      # -output: list of possible categories to score the current roll under
      #
      def get_possible_categories(self, scorecard):
            return list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))




      # Calculates the score of a given roll based on the selected category
      # -input: dice object, category string
      # -output: score of given role for given category
      #
      def score(self, dice, category, scorecard):
        #dice = roll.dice
        counts = [dice.count(i) for i in range(1,7)]

        if category in Scorecard.Numbers:
            score = counts[Scorecard.Numbers[category]-1] * Scorecard.Numbers[category]
        elif category == "company":
            score = 40 if sorted(dice) == [1,2,3,4,5] or sorted(dice) == [2,3,4,5,6] else 0
        elif category == "prattle":
            score = 30 if (len(set([1,2,3,4]) - set(dice)) == 0 or len(set([2,3,4,5]) - set(dice)) == 0 or len(set([3,4,5,6]) - set(dice)) == 0) else 0
        elif category == "squadron":
            score = 25 if (2 in counts) and (3 in counts) else 0
        elif category == "triplex":
            score = sum(dice) if max(counts) >= 3 else 0
        elif category == "quadrupla":
            score = sum(dice) if max(counts) >= 4 else 0
        elif category == "quintuplicatam":
            score = 50 if max(counts) == 5 else 0
        elif category == "pandemonium":
            score = sum(dice)
        else:
            print("Error: unknown category")
        return score


      # Generates all possible reroll combinations out of the options given for each die
      # -input: 2d tuple
      # -- each tuple within the overarching 2d tuple should contain the possible boolean reroll
      #    options for each die
      # -- for each option for each die, the function generates a list of tuples with one tuple for each
      #    possible reroll option of 5 die
      # -returns: list of tuples, each tuple is a singular reroll option for the 5 die
      #
      def gen_possible_rerolls(self, die_options):
            return [ (d1, d2, d3, d4, d5) for d1 in die_options[0] for d2 in die_options[1] for d3 in die_options[2] for d4 in die_options[3] for d5 in die_options[4] ]
