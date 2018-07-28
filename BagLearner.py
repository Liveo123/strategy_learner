'''
ShuHo Chou: schou33
'''
from  collections import Counter
import numpy as np
class BagLearner():
    def __init__(self, learner, kwargs={}, bags=20, boost=False, verbose=False):
        self.learners = []
        for i in range(bags):
            self.learners.append(learner(**kwargs))
        self.bags = bags
        self.kwargs = kwargs
        self.boost = boost
        self.verbose = verbose
        np.random.seed(seed=0)
    def author(self):
        return 'schou33'
    def addEvidence(self, Xtrain, Ytrain):
        for learner in self.learners:
            indices = np.random.randint(Xtrain.shape[0], size=Xtrain.shape[0])
            learner.addEvidence(Xtrain[indices], Ytrain[indices])
    def query(self, Xtest):
        res = []
        for learner in self.learners:
            res.append(learner.query(Xtest))

        res = np.transpose(res)
        ret = [max(Counter(x).iteritems(), key = lambda x : x[1])[0] for x in res]
        return np.array(ret)
