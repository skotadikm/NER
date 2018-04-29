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
cmd = os.popen(r'crf_test -m ' + model + ' ' + test_data)
result = cmd.read()

print(result)