"""
Recall = TP/TP+FN = TP/TotalGoldLabel
Precision = TP/TP+FP = TP/TotalPredicted
F1 Score = 2*(Recall * Precision) / (Recall + Precision)
"""
import os
import re
import sys

model = sys.argv[1]
test_data = sys.argv[2]
confusion_matrix = []

def crf_test():
    cmd = os.popen(r'crf_test -m ' + model + ' ' + test_data)
    result = cmd.read()
    return result

def create_confusion_matrix(test):
    tmp1 = test.splitlines()
    tmp2 = []
    for line in tmp1[:len(tmp1)-1]:
        raw = re.split(r'\t', line)
        pointer = len(raw)
        tmp2.append([raw[pointer-2],raw[pointer-1]])
        if(len(confusion_matrix) == 0):
            confusion_matrix.append([raw[pointer-2]])
        else:
            count = 0
            for i in range(len(confusion_matrix)):
                if(raw[pointer-2] == confusion_matrix[i][0]):
                    count += 1
            if(count == 0):
                confusion_matrix.append([raw[pointer-2]])
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix)):
            confusion_matrix[i].append(0)
    for line in tmp2:
        pointer = 0
        for i in range(len(confusion_matrix)):
            if(line[0] == confusion_matrix[i][0]):
                pointer = i
                break
        for i in range(len(confusion_matrix)):
            if(line[1] == confusion_matrix[i][0]):
                confusion_matrix[pointer][i+1] += 1
                break

def recall():
    tmp = []
    for i in range(len(confusion_matrix)):
        TotalGoldLabel = 0
        for j in range(len(confusion_matrix)):
            TotalGoldLabel += confusion_matrix[j][i+1]
        if(TotalGoldLabel != 0):
            tmp.append(confusion_matrix[i][i+1] / TotalGoldLabel)
        else:
            tmp.append(0)
    return tmp

def precision():
    tmp = []
    for i in range(len(confusion_matrix)):
        TotalPredicted = 0
        for j in range(len(confusion_matrix)):
            TotalPredicted += confusion_matrix[i][j+1]
        if(TotalPredicted != 0):
            tmp.append(confusion_matrix[i][i+1] / TotalPredicted)
        else:
            tmp.append(0)
    return tmp

def rec_and_prec():
    temp = []
    rec = recall()
    prec = precision()
    for i in range(len(confusion_matrix)):
        temp.append([confusion_matrix[i][0],rec[i],prec[i]])
    return temp

if __name__ == '__main__':
    test = crf_test()
    create_confusion_matrix(test)
    measure = rec_and_prec()
    print(measure)
    for line in confusion_matrix:
        print(line)
