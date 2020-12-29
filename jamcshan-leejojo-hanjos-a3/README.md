# A3
#### by: Josep Han (hanjos), Jack McShane (jamcshan)
#### 11/29/2020

### Part 1: Part of Speech Solver; done by Josep Han
We started to approach this problem by thinking of how to train the emission, initial, and transition probabilities given the train file that was given by the assignment.\
* Each word in the document was paired with a part of speech. If we assume that these words are not related to its position, it becomes a simple emission calculation: we count how often the word gives a certain part of speech, and then divide it over the total number of words in the document. 
* The training data is split by sentences, so the first pair gives the first part of speech; we count up the first part of speech, and then divide all of them by the total number of sentences. 
* The training data is compiled in order, so we take account of the previous part of speech and then calculate the number of times that part of speech moves to a different part of speech. Then, for each part of transition section, we divide each section by the sum of that section's count, e.g. transition(noun->all of the parts of speeches it goes to) / sum of transition(noun)
Simple calculation only looks at the emission probability of how often a word returns a certain part of speech, so for each word in the sentence, we look up the probability of that word being a certain part of speech.

For the HMM section, we need to consider the MAP label for the given sentence, where the word and part of speech do matter. So we use the Viterbi algorithm.

It turns out that calculating the posterior probabilty is a little different from Viterbi, and that Variable Elimination is a more suitable method for calculating the posteriors for every method, especially since Viterbi only keeps track of the most likely probability for each successive state. In addition, different part of speech configurations meant a different HMM posteriors, so it was important to calculate for each label method from the beginning.
#### Problems Faced/Solutions
One of the earliest problems we faced was that the part of speech solver was contained in a class.
* Keeping track of the emission, transition and initial probabilities required us to declare them in an __init__ space. 
Another problem we faced was the times where the certain words in the training set were not in the training set, or certain parts of speeches were not counted in the training set.
* We got around the first problem by adding that missing word into the probability dictionaries before running the calculations. For the second problem, before we return the probability tables, during the normalization phase we add a less than 1 occurance probability for the parts of speeches that were not detected in the training data.


### Part 2: Code Breaking; done by Jack McShane
The biggest part of the formulation for this problem was the paradigm to be used for the transition probabilities
In this program, the trasition probabilities from one letter to another are modeled using a Markov Chain class
* This Markov Chain models not only the trasitions between letters, but as you will see also model transitions between letters and *spaces*
* These transitions between spaces and letters and letters and spaces represent the probability of a letter initializing or starting a word, and a letter ending a word respectively
The second aspect of this problem was the implementation of the Metropolis-Hastings Algorithm
* the metro-hastings algorithm is a rather straightforward algorithm and is implemented as it was shown in the pdf for the assignment, however
* this algorithm required that the probability whether a given document was constructed in English be calculated.
* for this, the transition probabilities represented in the Markov Chain were a good start, but because of how small they were, could not be used outright to calculate that probability.
* for that, the logarithm of the transition probabilities were taken so as to take advantage of logarithmic properties.
* This allowed for a transformation of the values as well a change from multiplying the probabilities to adding them.

#### Problems Faced/Solutions
The way in which to represent the document was an issue faced.  The first implementation rendered the document per word.
* Once a better understanding of the translation portion of the encoding algorithm was developed, the design decision to treat the entire document as one word and model the transitions to and from spaces was implemented.
Another problem that currently ails the program is the calculation of P(D')/P(D)
* for a reason that has not yet become apparent, the ratio seems to be incredibly small pointing to a large difference in likelihood between T and T'
* However, I do not think that it comes from the calculation of the logarithmic probabilities as they are calculated the same way for each of the tables
* that would point to the difference being between the performance of the tables or possibly an error in modeling the transition probabilities
The third issue that was had with the program was the building of the substitution table(s)
* for quite a while, the replacement tables included whitespace as part of the mapping, drastically changing the number of spaces in a document
* this has since been changed such that spaces are not getting replaced by other characters/letters




### Part 3: Reading text; done by Josep Han
We determined these probabilities quickly when beginning this assignment: 
* Transition probability: probability of a given character going to a certain character. This is done by calculating character by character in a given corpus. (For our code, we used A Tale of Two Cities by Charles Dickens.)
* Initial probability: probability of the first character. We exclude the space, so it becomes clear that we can calculate the first character of non-space characters. 

This problem was similar in the algorithms deployed, but we realized that the emission probabilities were much different: we were to calculate the probability of a classification of the letter given the pixels of the testing data. In addition, we were to consider the possibility of noise corruption.\
The formula of considering the fact of noise corruption: if m = % of noise expected in the test data:
* (100%-m%)^(number of matched pixels in the given scan letter) * (m% ^ (number of mismatched pixels))

For our code, setting the noise level to 41% generally led us to a better predition of the scan than the simple model (which just returns the highest matching character value for each scan state without order considered). 

#### Problems Faced/Solutions
One of the more unique problems we faced here is that the code broke after a few words.
* We determined that it is because we did not use the logarithmic probability transformation to prevent a probability underflow given that it will approach a float number approaching zero as we compute for the later scan states. 


