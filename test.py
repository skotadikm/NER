"""
Recall = TP/TP+FN = TP/TotalGoldLabel
Precision = TP/TP+FP = TP/TotalPredicted
F1 Score = 2*(Recall * Precision) / (Recall + Precision)
"""
import os
import re
import sys
import numpy as np

model = sys.argv[1]
test_data = sys.argv[2]
confusion_matrix = []
label = []

def crf_test():
    cmd = os.popen(r'crf_test -m ' + model + ' ' + test_data)
    result = cmd.read()
    return result

def creat_final_result(test):
    tmp1 = test.splitlines()
    tmp2 = []
    final = []
    for line in tmp1[:len(tmp1)-1]:
        raw = re.split(r'\t', line)
        pointer = len(raw)
        tmp2.append([raw[pointer-2],raw[pointer-1]])
        tag = raw[pointer-2].replace("_start", "")
        tag = tag.replace("_cont", "")
        tag = tag.replace("_end", "")
        if(tag not in label):
            label.append(tag)
    ans_class = []
    for i in range(len(tag)):
        ans_class.append(0)
    label_pointer = 0
    ans_pointer = 0
    ans = ans_class
    for i in range(len(tmp2)):
        if("start" in tmp2[i][0] or "cont" in tmp2[i][0]):
            label_pointer += 1
            if(tmp2[i][0] == tmp2[i][1]):
                ans_pointer +=1
        elif("end" in tmp2[i][0]):
            if(tmp2[i][0] == tmp2[i][1] and label_pointer == ans_pointer):
                final.append([tmp2[i][0].replace("_end", ""),tmp2[i][0].replace("_end", "")])
            else:
                for j in range(label_pointer):
                    for index, tag in enumerate(label):
                        if(tag in tmp2[i-j]):
                            ans[index] += 1
                ind = np.argmax(ans)
                final.append([tmp2[i][0].replace("_end", ""),label[ind]])
        else:
            if("start" in tmp2[i][1] or "cont" in tmp2[i][1] or "end" in tmp2[i][1]):
                tag = tmp2[i][1].replace("_start", "")
                tag = tag.replace("_cont", "")
                tag = tag.replace("_end", "")
                if(tag == tmp2[i][0]):
                    final.append([tmp2[i][0],"(other)"])
                else:
                    final.append([tmp2[i][0],tag])
            else:
                final.append([tmp2[i][0],tmp2[i][1]])
        label_pointer = 0
        ans_pointer = 0
        ans = ans_class
    return final

def create_confusion_matrix(test):
    temp = creat_final_result(test)
    for tag in label:
        confusion_matrix.append([tag])
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix)):
            confusion_matrix[i].append(0)
    for line in temp:
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

def F_measure(rec, prec):
    tmp = []
    for i in range(len(confusion_matrix)):
        if(rec[i] + prec[i] != 0):
            f = 2 * (rec[i] * prec[i]) / (rec[i] + prec[i])
            tmp.append(f)
        else:
            tmp.append(0)
    return tmp

def measure():
    temp = []
    rec = recall()
    prec = precision()
    f = F_measure(rec, prec)
    for i in range(len(confusion_matrix)):
        temp.append([confusion_matrix[i][0],rec[i],prec[i],f[i]])
    return temp

if __name__ == '__main__':
    test = crf_test()
    create_confusion_matrix(test)
    score = measure()
    print("class"+"\t"+"Recall"+"\t"+"Precision"+"\t"+"F1-measure")
    length = len(score[0])
    for line in score:
        print(line[0]+"\t")
        for word in line[1:length-1]:
            tmp = round(word, 3)
            print(tmp)
            print("\t")
        tmp = round(line[length-1])
        print(tmp)
        print("\n")    