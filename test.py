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
    tmp1 = test.splitlines()
    for line in tmp1[:len(tmp1)-1]:
        raw = re.split(r'\t', line)
        pointer = len(raw)
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
            confusion_matrix[i][j].append(0)

        


if __name__ == '__main__':
    test = crf_test()
    tmp = create_confusion_matrix(test)
    print(confusion_matrix)


