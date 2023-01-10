import json
import numpy as np
import math
import random

def entropy(array):
    # calculate entropy for an array
    total = np.size(array,0)
    column = array[:, 0]
    if total>0:
        num_low = (column == 1).sum()
        first = num_low/total
        second = (total - num_low)/total
        if first > 0 and second > 0:
            entropy = - first * (math.log2(first)) - second * (math.log2(second))
        else:
            entropy = 0
    else:
        entropy = 0
        total = 0
    return [entropy,total]
    
def trim(array,i,j):
    # trim unwanted value from array
    todo = []
    for z in range(len(array)):
        if array[z][i] != j:
            todo.append(z)
    array = np.delete(array,todo,0)
    return array

def entropy_attr(array,i,total):
    #finds the entropy of each attribute
    sum = 0
    if i == 1 or i == 4:
        for j in [1,2,3]:
            new_arr = trim(array,i,j)
            result = entropy(new_arr)
            sum += (result[1]/total) * result[0]
    else:
        for j in [1,2]:
            new_arr = trim(array,i,j)
            result = entropy(new_arr)
            sum += (result[1]/total) * result[0]
    return sum

def check_leaf(array):
    #checks if the current database has found a risk conclusion
    todo = array.copy()[:,0]
    result = True
    for i in todo:
        if todo[0] != i:
            result = False
            break
    return [result,todo[0]]

def main():
    current = np.loadtxt("../data/train.txt", dtype=int)
    current = np.transpose(current)
    test_attribute = ""
    count = 0
    datacount = 0
    count = count
    children = 0
    attributes = [1,2,3,4,5]
    test_dict = {"AGE":1, "CRED_HIS":2, "INCOME":3, "RACE":4, "HEALTH":5}
    dict1 = {}
    gain_age = 0
    gain_cred = 0
    gain_income = 0
    gain_race = 0
    gain_health = 0
    gains = [gain_age,gain_cred,gain_income,gain_race,gain_health]
    current_dataset = {0: [current,gains]}
    alpha = "A"
    num1 = 0
    stop = False
    tree = []
    changes = ["A1"]

    while stop != True:
        # setting up root node
        if count == 0:
            current_copy = np.copy(current)
            entr = entropy(current_copy)
            for i in range(len(attributes)):
                entr_atrr = entropy_attr(current_copy,attributes[i],entr[1])
                gains[i] = entr[0] - entr_atrr
            maximum = max(gains)
            ind = gains.index(maximum)
            test_attribute = attributes[ind]
            gains[ind] = -1
            for i in test_dict:
                if test_attribute == test_dict[i]:
                    test_name = i
            tree.append([test_name])
            if test_attribute == 1 or test_attribute == 4:
                dict1 = dict.fromkeys(range(1,4))
            else:
                dict1 = dict.fromkeys(range(1,3))
            w = ord(alpha[0])
            w+=1
            alpha = chr(w)
            for i in dict1:
                num1 += 1
                dict1[i] = alpha + str(num1)
                changes.append(alpha+str(num1))
            tree[-1].append(dict1)
            num1 = 0    
        # all other nodes follows this
        else:
            if isinstance(tree[count-1][1],dict):
                for i,j in tree[count-1][1].items():
                    if j == alpha + str(1):
                        w = ord(alpha[0])
                        w+=1
                        alpha = chr(w)
                        num1 = 0
            for d in children:
                for i in test_dict:
                    if tree[count-1][0] == i:
                        trimmer = test_dict[i]
                if isinstance(tree[count-1][1][d],list) != True:
                    if d in current_dataset[count-1][0][:,trimmer]:
                        current_copy = trim(current_dataset[count-1][0],trimmer,d)
                        arrs = (current_dataset[count-1][1]).copy()
                        if check_leaf(current_copy)[0] != True:
                            entr = entropy(current_copy)
                            for i in range(len(attributes)):
                                if arrs[i] != -1:
                                    entr_atrr = entropy_attr(current_copy,attributes[i],entr[1])
                                    arrs[i] = entr[0] - entr_atrr
                            maximum = max(arrs)
                            ind = arrs.index(maximum)
                            test_attribute = attributes[ind]
                            arrs[ind] = -1
                            datacount +=1
                            current_dataset.update({datacount:[current_copy,arrs]})
                            for i in test_dict:
                                if test_attribute == test_dict[i]:
                                    test_name = i
                                    unique = np.unique(current_copy[:,test_dict[i]])
                                    unique = unique.tolist()
                            tree.append([test_name])
                            dict1 = dict.fromkeys(unique)
                            changecount = 0
                            for i in dict1:
                                num1 += 1
                                changecount += 1
                                dict1[i] = alpha + str(num1)
                                changes.append(alpha + str(num1))
                            tree[-1].append(dict1)
                            for i,j in tree[-1][1].items():
                                #where the test attribute couldn't be split further and could result in 1 or 2
                                if j[0] == "G":
                                    random1 = random.randint(1,2)
                                    tree[-1] = random1
                                    end = len(changes)
                                    changes = changes[0:end-changecount]
                                    break
                        else:
                            tree.append(int(check_leaf(current_copy)[1]))
                            datacount +=1
                            current_dataset.update({datacount:"skip"})
        count+=1
        check = False
        try:
            while check == False:
                if isinstance(tree[count-1],int) == True:
                    count+=1
                else:
                    continue_1 = True
                    for i in tree[count-1][1]:
                        if isinstance(tree[count-1][1][i],int) != True:
                            check = True
                            continue_1 = False
                    if continue_1 == True:
                        count += 1
        except:
            break
        children = list(tree[count-1][1].keys())
    actual_tree = tree[0]
    curr_children = []
    set_index = 0
    for i in tree:
    #converts the tree to specified format 
        if isinstance(i,int) != True:
            if isinstance(i[1],dict):
                curr_children = list(i[1].keys())
                for j in curr_children:
                    change = i[1][j]
                    set_index = changes.index(change)
                    #set each sublist to its matching children
                    i[1][j] = tree[set_index]
    print(actual_tree)
    with open ("../data/tree.txt", "w") as f:
        json.dump(actual_tree, f)  # stores the tree to the file
                           

main()
