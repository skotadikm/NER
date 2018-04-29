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

def crf_test(model, test_data):
    cmd = os.popen(r'crf_test -m ' + model + ' ' + test_data)
    result = cmd.read()
    return result

def create_confusion_matrix(test):
    tmp1 = test.splitlines()
    for line in tmp1:
        tmp2 = []
        i = re.split(r'\t', line)
        tmp2.append(i[len[i]-1])
        tmp2.append(i[len[i]])
    return tmp2


if __name__ == '__main__':
    test = crf_test(model, test_data)
    print(create_confusion_matrix(test))