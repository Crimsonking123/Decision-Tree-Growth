import json
import numpy as np

def predict(tr, r, li):
        if type(tr) != list:
            return tr
        # make copy tree for later editing
        a = tr.copy()
        # calculate prediction
        while type(a) == list:
            for i in range(len(li)):
                if a[0] == li[i][0]:
                    break
            # error here from tree format
            a = a[1][str(r[i-1])]
        return a

def accuracy(tr, m, li):
        # accuracy is the number of correct predictions made...
        c = 0   # correct predictions starts at 0
        for i in range(np.size(m,axis=1)):
            if predict(tr, m[1:,i], li) == m[0,i]:
                       c += 1
        # ...divided by the total number of predictions made
        return c/np.size(m,axis=1)

def main(fname):
    # get tree from file
    with open('../data/'+fname) as f:
        tree = json.load(f)
    # get the data descriptions from file
    with open('../data/dataDesc.txt') as f:
        desc = json.load(f)
    # test set
    train = np.loadtxt('../data/train.txt', dtype=int)
    # evaluate accuracy
    evaluate = accuracy(tree, train, desc)
    print("The tree has an accuracy of: " + str(evaluate))

main("tree.txt")
