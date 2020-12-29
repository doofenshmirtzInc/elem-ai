
import random as r


#############MCMC
##type of samples that i want
# C is set (True/on-time)

##form of a sample
# [R T C]


##want to find: P(R=True|C=True)
#have to gen samples that have C=True
# have to gen samples over R and T

####Gibbs sampling algo
# gen init sample (random)
# for each sample in t = 1 to T
#   let x[t] = x[t-1] --> new sample is old sample
#   for each unobserved var Xi
#       sample a val for Xi given vals for all other vars in x[t] --> gen val for single var based on P(Xi|X-i)
# put new sample in sample matrix


##gen 3 markov chains
#get three lists of samples going
# make a comparison after each new sample is generated
##  this will involve keeping a tally of all the samples that have R=true, form of sample: [R T C]
# compare the P(R=true|C=true) values and use the threshold of .05 as the stopping point
# once all three P(R=true|C=true) values are within .05, print one as the value
##  while (within 2k iterations) and ( max( [abs(p1-p2), abs(p1-p3), abs(p2-p3)] ) > .05 ):
##      add a new sample to each list
##      update_count counts
##      calc p values

######steps
#gen samples
#tally values
    #use counts() method
#calc desired prob: P(R=true|C=true)



def gen_rand_sample():
    return [r.choice([True,False]), r.choice([True,False]), True]


def gen_sample(data, observed):
    probs = [.05325, .03743, .3913, .3077]
    new = data.copy()
    #change first var
    if data[1]:
        new[0] = True if r.random() < probs[0] else False
    else:
        new[0] = True if r.random() < probs[1] else False
    #change second var
    if data[0]:
        new[1] = True if r.random() < probs[2] else False
    else:
        new[1] = True if r.random() < probs[3] else False

    return new



def max_diff(p_rain):
    return max( [ abs(p_rain[0] - p_rain[1]), abs(p_rain[0] - p_rain[2]), abs(p_rain[1] - p_rain[2]) ] )



def update_count(data, count):
    return (count[0], count[1]+1) if not data[0] else (count[0]+1, count[1]+1)

############DRIVER
threshold = .05
num_chains = 3
chains = [[gen_rand_sample()] for i in range(num_chains) ]
counts = [update_count(chain, (0,0)) for chain in chains]
p_rain = [ ( count[0]/count[1] ) for count in counts ]

itr = 0
while itr < 2000:
    for i in range( len(chains) ):
        chains[i].append( gen_sample( chains[i][-1], 2 ) )
        counts[i] = update_count(chains[i][-1], counts[i])
        p_rain = [ ( count[0]/count[1] ) for count in counts ]
    itr += 1


avg = sum(p_rain) / len(p_rain)
print(f'The average amongst the {num_chains}: P(R=True|C=True) = {avg}')
