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
counter = 0

def crf_test():
    cmd = os.popen(r'crf_test -m ' + model + ' ' + test_data)
    result = cmd.read()
    return result

def create_confusion_matrix(test):
    tmp1 = test.splitlines()
    tag = []
    for line in tmp1:
        tmp2 = []
        i = re.split(r'\t', line)
        pointer = len(i)
        tmp2.append(i[pointer-2])
        tmp2.append(i[pointer-1])
        if(i[pointer-2] != i[pointer-1]):
            counter += 1
        tag.append(tmp2)
    return tag


if __name__ == '__main__':
    test = crf_test()
    tmp = create_confusion_matrix(test)
    print(tmp)
    print(counter)