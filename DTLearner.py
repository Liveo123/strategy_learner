'''
ShuHo Chou: schou33
'''
import numpy as np
from collections import Counter
import time

class DTLearner():
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = []
        self.LEAF = -1;
        self.NA = -1;

    def author(self):
        return 'schou33'

    def addEvidence(self, Xtrain, Ytrain):
        Ytrain = np.array([Ytrain])
        data = np.concatenate((Xtrain, Ytrain.T), axis=1)

        tree = self.buildtree(data)
        self.tree = tree


    def buildtree(self, data):
        Xtrain = data[:, :-1]
        Ytrain = data[:, -1]
        if data.shape[0] <= self.leaf_size:
            return np.array([[self.LEAF, Counter(Ytrain).most_common(1)[0][0], self.NA, self.NA]])
        if np.std(Ytrain) == 0.0:
            return np.array([[self.LEAF, Counter(Ytrain).most_common(1)[0][0], self.NA, self.NA]])


        corrs = np.array([abs(np.corrcoef(Xtrain[:, x], Ytrain)[0][1]) for x in range(Xtrain.shape[1])])
        corrs[np.isnan(corrs)] = 0

        factor = np.argmax(corrs)
        median = np.median(Xtrain[:, factor])

        data_right = data[data[:, factor] > median]
        data_left = data[data[:, factor] <= median]

        # Here if all data goes to left, I first minus the median by a very small value
        # and see if it split well, if this time all the data go to the left side, then
        # I know that they all have the same values, so it should be a leaf.
        if data_right.shape[0] == 0:
            median -= 0.00001
            data_right = data[data[:, factor] > median]
            data_left = data[data[:, factor] <= median]
            if data_left.shape[0] == 0:
                return np.array([[self.LEAF, Counter(Ytrain).most_common(1)[0][0], self.NA, self.NA]])

        left = self.buildtree(data_left)
        right = self.buildtree(data_right)
        root = np.array([[factor, median, 1, left.shape[0] + 1]])
        root = np.concatenate((root, left, right))
        return root


    def query(self, Xtest):
        if self.verbose:
            print self.tree
        Y = []
        for x in Xtest:
            idx = 0
            while True:
                factor = int(self.tree[idx][0])
                # Reached Leaf
                if factor == self.LEAF:
                    Y.append(self.tree[idx][1])
                    break
                # Go left
                if x[factor] <= self.tree[idx][1]:
                    idx += int(self.tree[idx][2])
                else:
                    idx += int(self.tree[idx][3])
        return np.array(Y)
