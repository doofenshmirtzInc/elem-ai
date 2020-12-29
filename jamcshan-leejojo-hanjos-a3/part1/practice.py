
import sys
# from label import read_data
from pos_scorer import Score
from pos_solver import *
import sys

def read_data(fname):
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = tuple([w.lower() for w in line.split()])
        exemplars += [ (data[0::2], data[1::2]), ]

    return exemplars

aaa = read_data('bc.test')
(train_file, test_file) = 'bc.train', 'bc.test.tiny'

solver = Solver()
train_data = read_data(train_file)
solver.train(train_data)

print("Loading test data...")
test_data = read_data(test_file)
# print(solver.word_dict)
print(solver.word_dict['produced']['noun'] / sum(solver.word_dict['produced'].values()))
