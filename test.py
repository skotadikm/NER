"""
Recall = TP/TP+FN
Precision = TP/TP+FP
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
    counter = 0
    counter2 = 0
    

    tmp1 = test.splitlines()
    tmp2 = []
    for line in tmp1[:len(tmp1)-1]:
        raw = re.split(r'\t', line)
        pointer = len(raw)


        if(raw[pointer-2] != raw[pointer-1]):
            counter += 1


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
        for i in range(len(confusion_matrix)):
            if(line[1] == confusion_matrix[i][0]):
                confusion_matrix[pointer][i+1] += 1
    

    for i in range(len(confusion_matrix)):
        for j in range(2,len(confusion_matrix)):
            counter2 += confusion_matrix[i][j]
    print(counter)
    print(counter2)
    print(len(tmp2))
        


if __name__ == '__main__':
    test = crf_test()
    tmp = create_confusion_matrix(test)
    print(confusion_matrix)


