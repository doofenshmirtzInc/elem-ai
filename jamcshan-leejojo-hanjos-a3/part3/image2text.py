#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png

# (Note: in our implementation, we used: python3 ./image2text.py courier-train.png dickens.txt <test image file to use> )
# Authors: Josep Han (hanjos)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math
CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

# ## Below is just some sample code to show you how the functions above work. 
# # You can delete this and put your own code here!


# # Each training letter is now stored as a list of characters, where black
# #  dots are represented by *'s and white dots are spaces. For example,
# #  here's what "a" looks like:
# print("\n".join([ r for r in train_letters['a'] ]))

# # Same with test letters. Here's what the third letter of the test data
# #  looks like:
# print("\n".join([ r for r in test_letters[2] ]))



# # The final two lines of your output should look something like this:
# print("Simple: " + "Sample s1mple resu1t")
# print("   HMM: " + "Sample simple result") 

### MY CODE 
# given a text file, set each line as a string element in the final list; newline stripped of course.
def readfile(file):
    final_list = []
    with open(file,'rt', encoding = 'utf-8') as this_file:
        for line in this_file:
            # print(line)
            if len(line) >1:
                final_list.append(line.rstrip())
        # contents = this_file.read()
    # print(contents)
    return final_list
rfile = readfile(train_txt_fname)
# Given a training text file, return the initial letter probabilities and the transition probabilities. 
def train2(data):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    init_prob = {l : 0 for l in TRAIN_LETTERS}
    trans_prob = {l:{l2:0 for l2 in TRAIN_LETTERS} for l in TRAIN_LETTERS}
    total_sentences = len(data)
    prev = data[0][0]
    for line in data:
        # for initial probability, remove each space, and then calculate the probability of a word being a certain letter.
        for word in line.split():
            try:
                init_prob[word[0]] += 1
            except:
                pass         
        for letter in line:
            if prev != None:
                try:
                    trans_prob[prev][letter] += 1
                    prev = letter
                except:
                    prev = letter
            else:
                prev = letter
            
   
    # normalize the transition probability by each transition.
    for start_letter in trans_prob:
        trans_sum = sum(trans_prob[start_letter].values())
        if trans_sum == 0:
            trans_sum =1
        for transition in trans_prob[start_letter]:
            if trans_prob[start_letter][transition] == 0:
                trans_prob[start_letter][transition] = 0.5/ trans_sum
            else:
                trans_prob[start_letter][transition] =trans_prob[start_letter][transition]/ trans_sum

    # normalize the initial probability by the number of words in the training document.            
    total_letters = sum(init_prob.values())
    for letter in init_prob:
        if init_prob[letter] == 0:
            init_prob[letter]= 0.1 / total_letters
        else:
            init_prob[letter] = init_prob[letter] / total_letters
    return init_prob, trans_prob
init_prob,trans_prob = train2(rfile)

# one of testing_letters's matched dots with one of the train_letters. 
def matched_dots(test, train):
    output= []
    for i in range(0, len(test)):
        test_line = test[i]
        train_line = train[i]
        new_line = ''.join('*' if test_line[r] == train_line[r] else ' ' for r in range(0, len(test_line)))
        output.append(new_line)
    return output


# count how many dots are shown on the letter, 
# usually after calculating the xor between these two. 
def count_dots(letter):
    total = 0
    for line in letter:
        for dot in line:
            if dot =='*':
                total += 1
        # total += 1 if dot == '*' else 0 for dot in line
    return total

# given a letter, return the max probability of it being a certain training letter as well as the compiled letter dictionary probabilities for each traning letter.
def simple_letter(letter, noise_level):
    # print(remaining_dots(letter))
    maxval = 0
    likely_letter = ''
    letter_dict = {}
    for l, v in train_letters.items():
        xord = matched_dots(letter, v)
        matched = count_dots(xord)
        letter_dict[l] = math.pow(noise_level,(14*25)-matched) *math.pow(1-noise_level,matched)
    
        if maxval < count_dots(xord):
            maxval = count_dots(xord)
            likely_letter = l
    # for letter in letter_dict:
        # letter_dict[letter] = letter_dict[letter] / sum(letter_dict.values())
    return likely_letter,letter_dict

# Given a scanned word and the command, return the most likely letter for each scan; if HMM, run the Viterbi algorithm given the dictionary of each state's probability of being a certain letter.
def decipher(scan, command):
    output_simple = ''
    scan_prob = []
    for letter in scan:
        scan_prob.append(simple_letter(letter,0.41))
    if command == 'simple':
        # return ''.join([max(e[1], key =e[1].get) for e in scan_prob])
        return ''.join([e[0] for e in scan_prob])
    if command == 'HMM':
        return ''.join(viterbi([e[1] for e in scan_prob]))
        # return [max(e[1], key =e[1].get) for e in scan_prob]
        # return scan_prob

# given an ordered dictionary of scans and its respective probabilities to be a certain letter, run the Viterbi in order to determine the most likely letter.
def viterbi(scan_prob):
    keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    V= [{}]
    for st in keys:
        first_letter = scan_prob[0]
        V[0][st] = {'prob':math.log(init_prob[st]) + math.log(first_letter[st]), 'prev' : None}
    for t in range(1, len(scan_prob)):
        V.append({})
        for st in keys:
            max_tr_prob = V[t-1][keys[0]]['prob'] + math.log(trans_prob[keys[0]][st])
            prev_st_selected = keys[0]
            for prev_st in keys[1:]:
                tr_prob = V[t-1][prev_st]['prob'] + math.log(trans_prob[prev_st][st])
                if tr_prob > max_tr_prob:
                    max_tr_prob= tr_prob
                    prev_st_selected = prev_st
            max_prob = max_tr_prob + math.log(scan_prob[t][st])
            V[t][st] = {'prob': max_prob, 'prev': prev_st_selected}
    
    opt_prob = []
    opt = []
    max_prob = 0.0
    previous = None
    total_prob = 0
    for st, data in V[-1].items():
        best_st = st
        total_prob += data['prob']
        if data['prob']> max_prob:
            max_prob = data['prob']
            best_st = st
    opt.append(best_st)
    try:    
        opt_prob.append(max_prob/total_prob)
    except:
        opt_prob.append(0)
    previous = best_st

    for t in range(len(V) - 2, -1, -1):
        total_prob = 0
        opt.insert(0, V[t+1][previous]['prev'])
        for st, data in V[t+1].items():
            total_prob += data['prob']
        try:
            opt_prob.insert(0, V[t+1][previous]['prob']/total_prob)
        except:
            opt_prob.insert(0,0)
        previous = V[t+1][previous]['prev']
    return opt

print("Simple:", decipher(test_letters, 'simple'))
# print(test_letters)
# print(trans_prob['T'])
# print(init_prob)
print('HMM:', decipher(test_letters, 'HMM'))
# print(sum(trans_prob['T'].values()))
# (train_image, train_test, test_image) = sys.argv[1:3]



# y = decipher(test_letters, 'HMM')
# print(y)