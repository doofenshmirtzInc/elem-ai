import numpy as np
import sys
import geolocate
import pickle



def read_file(filename):
    with open(filename, 'r') as file:
        return [line.split() for line in file]


def write_data(filename, obj):
    with open(filename, 'w') as file:
        for line in obj:
            file.write( ' '.join( line ) )

def write_classes(filename, obj):
    with open(filename, 'w') as file:
        file.write( ' '.join(obj) )


def get_classes(file):
    classes = list()
    y = list()
    for line in file:
        loc = line.pop(0)
        y.append(loc)
        if loc not in classes:
            classes.append(loc)

    return (classes, y)



def get_words(file):
    words = list()
    for line in file:
        for word in line:
            if word not in words:
                words.append(word)

    return words




def convert_to_binary(words, tweets):
    for tweet in tweets:
        for word in words:
            if word in tweet:
                something.append(1)
    return [[1 if word in tweet else 0 for word in words] for tweet in tweets]


def pickle_obj(obj, file):
    pickle_out = open(file, 'wb')
    pickle.dump(obj, pickle_out)
    pickle_out.close()


def read_pickled(file):
    pickle_in = open(file, 'rb')
    data = pickle.load(pickle_in)
    pickle_in.close()
    return data


def main():
    pass


if __name__ == '__main__':

    if( len(sys.argv) != 5 ):
        raise Exception('usage: ./tester.py input-file class-file y-data-file x-data-file')

    file = read_file( sys.argv[1] )
    #pickle_obj(get_classes( file )[0], sys.argv[2])
    #words = get_words( file )
    #pickle_obj(words, 'words.pickle')
    #get_classes( file )
    #X = [[1 if( word in tweet ) else 0 for word in words] for tweet in file]
    #pickle_obj(X, sys.argv[4])


    classes = read_pickled(sys.argv[2])
    words = read_pickled( 'words.pickle' )
    X = read_pickled( sys.argv[4] )
    for line in X:
        print(line)




    #X = list()
    #for tweet in file:
        #line = list()
        #for word in words:
            #if word in tweet:
                #line.append(1)
            #else:
                #line.append(0)
        #X.append(tweet)
#
    #for line in X:
        #print(line)

    #data = read_pickled( sys.argv[3] )
