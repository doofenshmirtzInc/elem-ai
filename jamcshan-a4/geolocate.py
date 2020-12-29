import sys
import numpy as np


class DecisionTree:

    def fit(self, data):
        pass


    def predict(self):
        pass


class NaiveBayes:

    # in this function, build:
        # classes
        # words
        # table
        # calculate important value
    def fit(self, data):
        self.classes, self.words = (list(), list())
        for line in data:
            if line[0] not in self.classes:
                self.classes.append(line[0])
            for i in range(1, len(line)):
                if line[i] not in self.words:
                    self.words.append(line[i])

        X = np.array( [[1 if word in tweet else 0 for word in self.words] for tweet in data] )
        print(type(X))
        for entry in X:
            print(entry)


    def predict(self):
        pass

######END NAIVE BAYES DEF



def read_file(filename):
    with open(filename, 'r') as file:
        return [[token for token in line.split()] for line in file]
        #return np.array( [np.array( [token for token in line.split()], dtype=object) for line in file], dtype=object )


def write_file(filename):
    pass


def main():

    # numpy not best idea for uneven data sizes

    # read in training file as list of lists
    # each internal list contains the contents of the tweet
    data = read_file(sys.argv[1])
    nb = NaiveBayes()
    nb.fit(data)
    #nb.fit(X, y)




if __name__ == '__main__':

    if ( len(sys.argv) != 3 ):
        raise Exception('usage: ./file.py training-input-file bayes-model-output-file')


    main()
