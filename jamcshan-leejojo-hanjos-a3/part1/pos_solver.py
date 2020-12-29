###################################
# CS B551 Fall 2020, Assignment #3
#
# Your names and user ids: Josep Han (hanjos)
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
from math import log


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#

# Helper functions in Viterbi; helps modularize the algorithm.

# update prev -> current pos part of a given transition probability dictionary by updating by 1; if a certain POS not found, create a new POS.
def update_trans_prob(current_pos, prev_pos, trans_prob):
    # print(prev_pos)
    if prev_pos!= None:
        # print('done')
        try:
            trans_prob[prev_pos][current_pos] += 1
        except:
            trans_prob[prev_pos][current_pos] = 1

    prev_pos = current_pos
    # print(prev_pos)
    return prev_pos, trans_prob

# finalize, aka normalize the transition probabilities
def finalize_trans_dict(trans_prob, total_trans):
    for pos, trans in trans_prob.items():
        # each transition has a different sum of total transition occurrances, so declare a new one each loop here
        total_trans = sum(trans.values())
        for value in trans:
            if trans[value] != 0:
                trans[value] = trans[value] / total_trans
                # log translation
                # trans[value] = log(trans[value])
            else:
                # pass
                # log translation
                # trans[value] = -100 
                trans[value] = 0.01 / total_trans
                
    return trans_prob

# similar methods done here as update_trans_prob
def update_word_prob(word,pos,word_dict):
    try:
        word_dict[str(word)][pos] += 1
    except:
        try:
            word_dict[str(word)][pos] = 1
        except:
            word_dict[str(word)] = {}
            word_dict[str(word)][pos] = 1
    return word_dict
def finalize_word_dict(word_dict,total_word):
    
    keys = ["ADJ","ADV","ADP","CONJ","DET","NOUN","NUM","PRON","PRT","VERB","X","."]
    keys = [s.lower() for s in keys]
    for word, pos_dict in word_dict.items():
        for key in keys:
            try:
                pos_dict[key] = pos_dict[key] / total_word
            except:
                pos_dict[key] = 0.0001 / total_word

            
    return word_dict
def finalize_init_dict(init_dict, total_sentences):
    for pos in init_dict:
        if init_dict[pos] != 0:
            init_dict[pos] = init_dict[pos] / total_sentences
        else:
            init_dict[pos] = 0.1/ total_sentences
    return init_dict
def fix_missing(word_dict, sentence, total_word):
    keys = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
    for word in sentence:
        try:
            word_dict[word]
        except:
            word_dict[word] = {key:.9/total_word for key in keys}

    return word_dict
class Solver:
    def __init__(self):
        self.keys = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        keys= self.keys
        self.trans_prob = {key:{key2:0 for key2 in keys} for key in keys}
        
        self.init_prob = {key: 0 for key in keys}
        self.word_dict= {}
        self.total_word = 0
        self.opt_prob = []
        self.V = [{}]
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        score = 0
        if model == "Simple":
            for i in range(0, len(sentence)):
                word = sentence[i]
                pos = label[i]
                # print(self.word_dict[word])
                try:
                    # print(log(self.word_dict[word][pos]/ sum(self.word_dict[word].values())))
                    score += log(self.word_dict[word][pos])
                    # print(score)
                except:
                    score += 0
            return score

            # return -999
        # run through viterbi algorithm for each successive label given the sentence given.
        elif model == "HMM":
            score = 0
            tau = {}
            for M in range(1, len(label) - 1):
                N = len(label)
                for i in range(0, M):
                    tau[i+1] = {s:0 for s in self.keys}
                for s in self.keys:
                    for s2 in self.keys:
                        try:
                            tau[i+1][s] += (tau[i][s2] if i>0 else self.init_prob[s2]) * self.word_dict[sentence[i]][s2] * self.trans_prob[s2][s]
                        except:
                            tau[i+1][s] += self.init_prob[s2] * self.word_dict[sentence[i]][s2] * self.trans_prob[s2][s]
                for i in range(N-1, M, -1):
                    tau[i] = {s:0 for s in self.keys}
                    for s in self.keys:
                        for s2 in self.keys:
                            try:
                                tau[i][s] += (tau[i+1][s2] if i +1 < N else 1) * self.word_dict[sentence[i]][s2] * self.trans_prob[s][s2]
                            except:
                                tau[i][s] += 1 * self.word_dict[sentence[i]][s2] * self.trans_prob[s][s2]
                joint = {}
                for s in self.keys:
                    # print(tau[M][s], M)
                    joint[s] = tau[M][s] * tau[M+1][s] * self.word_dict[sentence[M]][s]
                j_sum = sum(joint.values())
                try:
                    score += log(joint[label[i]]/j_sum)
                except:
                    score += log(0.001)
                # this_word = sentence[M]
                # this_joint = ve(self.keys, self.trans_prob, self.word_dict, self.init_prob,sentence, M+ 1)
                # this_sum = sum(this_joint.values())
                # this_score = this_joint[this_word]/this_sum
                # score += log(this_score)
            return score

        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
        total_word = 0
        total_sentences=  len(data)
        for spair in data:
            prev_pos = None 
            total_word += len(spair[0])
            # for each new sentence, check which pos is used at the beginning of the sentence.
            self.init_prob[spair[1][0]] += 1
            for i in range(0, len(spair[0])):
                word = str(spair[0][i])
                pos = spair[1][i]
                update_word_prob(word,pos,self.word_dict)
                prev_pos,self.trans_prob= update_trans_prob(pos, prev_pos, self.trans_prob)
        self.word_dict =finalize_word_dict(self.word_dict, total_word)
        self.total_word = total_word
        total_trans = total_word - total_sentences
        self.trans_prob = finalize_trans_dict(self.trans_prob, total_trans)
        finalize_init_dict(self.init_prob, total_sentences)



    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        return_list = []
        for item in sentence:
            # print(item)
            # print(max(self.word_dict[item], key = self.word_dict[item].get))
            try:
                return_list.append(max(self.word_dict[item], key = self.word_dict[item].get))
            except:
                print(item)
                return_list.append('noun')
        # return max(self.word_dict, key = self.word_dict.get)
        # print(return_list)
        return return_list

    def hmm_viterbi(self, sentence):
        self.word_dict = fix_missing(self.word_dict, sentence,self.total_word)
        V = [{}]
        for st in self.keys:
            first_word = sentence[0]
            V[0][st] = {"prob": self.init_prob[st] * self.word_dict[first_word][st], "prev" : None}
        # print(V)
        for t in range(1, len(sentence)):
            V.append({})
            for st in self.keys:
                max_tr_prob = V[t-1][self.keys[0]]['prob'] * self.trans_prob[self.keys[0]][st]
                prev_st_selected = self.keys[0]
                for prev_st in self.keys[1:]:
                    tr_prob = V[t - 1][prev_st]['prob'] * self.trans_prob[prev_st][st]
                    if tr_prob > max_tr_prob:
                        max_tr_prob = tr_prob
                        prev_st_selected = prev_st
                max_prob = max_tr_prob * self.word_dict[sentence[t]][st]
                V[t][st] = {'prob': max_prob, 'prev' : prev_st_selected}
        
        opt_prob = []
        opt = []
        max_prob = 0.0
        previous = None
        total_prob = 0
        for st, data in V[-1].items():
            best_st = st
            total_prob += data['prob']
            if data['prob'] > max_prob:
                max_prob = data['prob']
                best_st = st
        opt.append(best_st)
        # print(total_prob)
        try:
            opt_prob.append(max_prob / total_prob)
        except:
            opt_prob.append(max_prob)

        previous = best_st


        for t in range(len(V) - 2, -1 , -1):
            total_prob = 0
            opt.insert(0, V[t + 1][previous]['prev'])
            for st, data in V[t+1].items():
                # max_prob = V[t+1][previous]['prob']
                total_prob += data['prob']
            try:            
                opt_prob.insert(0, V[t+1][previous]['prob']/total_prob)
            except:
                opt_prob.insert(0, V[t+1][previous]['prob'])
            previous = V[t+ 1 ][previous]['prev']
            # opt_prob.insert(0, V[t+1][previous]['prob'])
        
        self.opt_prob = opt_prob
        self.V = V
        return opt
        # return [ "noun" ] * len(sentence)

    def confidence(self, sentence, answer):
        newresult = []
        for item in self.opt_prob:
            item = round(item, 3)
            if item == 1:
                item -= 0.001
            newresult.append(item)
        return newresult


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")

