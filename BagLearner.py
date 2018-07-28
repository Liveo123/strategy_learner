"""
A Bag Learner wrapper.  (c) 2017 Paul Livesey
"""

import numpy as np

class BagLearner(object):

    def __init__(self, 
                 learner, 
                 kwargs,
                 bags = 20,
                 boost = False,
                 verbose = False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.results = np.array([])

    def author(self):
        return 'plivesey3' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        #if self.verbose:
            #mu.printVerbose("dataX", dataX)
            #mu.printVerbose("dataY", dataY)
        
        # For each bag, build a random group of data from 
        # dataX.  This should use the first 60% of the 
        # data and should allow the same data to be used more
        # than once.
        # Once the bags is created, run it against the learner 
        # and store the result

        self.results = {}   #np.empty((0, 4), float)
        for bag in range(self.bags):
            built_bag = np.empty((0, dataX.shape[1]), float)
            built_bag_res = np.empty((0), float)
            for row_cnt in range(int(0.6 * dataX.shape[0]) ):
                rnd_choice = np.random.randint(int(0.6 * dataX.shape[0]))
                rnd_item = np.array([dataX[rnd_choice]])
                rnd_res = dataY[rnd_choice]
                built_bag = np.vstack((built_bag, rnd_item))
                built_bag_res = np.append(built_bag_res, rnd_res) 
                #if self.verbose:
                    #mu.printVerbose("built bag", built_bag)
                    #mu.printVerbose("built bag result", built_bag_res)

            # Now run the learner on this randomised selection
            # and add the results to the end.
            new_learner = self.learner(**self.kwargs)
            new_learner.addEvidence(built_bag, built_bag_res)    
            self.results[bag] = new_learner 
                
            #if self.verbose:
                #mu.printVerbose("self.results", self.results)

    def query(self,points):
        """
        
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a 
        specific query.
        @returns the estimated values according to the saved model.
        """
        #if self.verbose:
            #mu.printVerbose("self.results", self.results)
        
        # Go through all of the results and find their mean.  This is our
        # main result
        results = np.empty(points.shape[0])
        cnt = 0.0
        for key, dec_table in self.results.items():
            results += (dec_table.query(points))
            cnt = cnt + 1.0
        
        return results / cnt



if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
