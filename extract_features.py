#vocab is list of word features
#word feature = [original word,word counter,w0,w-1,w-2,w-3,w-4,w-5,w+1,w+2,w+3,w+4,w+5,alphanum(w0),Num(w0),special_char(w0),English(w0),blank_front(w0),blank_behind(w0),class]
#if it has dicts,dict will be appended in the end of feature list.

#define
#alphanum = contained with num and anylangauge alphabets (it can contrain special char)
#num = contained with only numberic
#special_char = atleast it has to contain special char
#English = contained with only english alphabet

# sum of corpus for filename

#####################################################################################
import re
import sys

filename = sys.argv[1]
vocab = []
corpus_text = ""
front_space = 0
vocab_count = 0

#original dictionary
dic_list = [["common"],["loc_name"],["loc_clue"],["org_name"],["org_clue"],["per_clue"],["per_first"],["per_last"]]

def create_dic(i):
    #แก้ไขpath dic
    filenames = dic_list[i][0]
    txt_file = open(filenames+".txt","r",encoding="utf-8-sig")
    text = txt_file.read()
    txt_file.close()
    raw = re.split(r'\n', text)
    for comp in raw:
        dic_list[i].append(comp)

def read_txt(filenames):
    global corpus_text
    txt_file = open(filenames,"r",encoding="utf-8-sig")
    corpus_text = txt_file.read()
    txt_file.close()

def create_vocab(corpus_text):
    global front_space
    global vocab_count
    global vocab
    raw = re.split(r'\|', corpus_text)
    init = 0
    for comp in raw:
        if(init == 0):
            init = 1
        else:
            tmp = []
            space_tag = re.findall(r"\s",comp)
            if(comp != " " and comp != "\n" and space_tag == []):
                vocab_count += 1
                tag = re.findall(r"\(+\w+\)",comp)
                tag1 = re.findall(r"\(+\(+\w+\)",comp)
                if(tag1 != []):
                    word = "("
                    temp = tag[0]
                    tag[0] = temp[1:]
                elif(tag == []):
                    tag.append("(other)")
                    word = comp
                else:
                    if(tag[0] == comp):
                        word = tag[0]
                        tag[0] = "(other)" 
                    else:
                        word =  comp.replace(tag[0], "")
                label = tag[0]
                tmp = [word,0,"wait","ool","ool","ool","ool","ool","ool","ool","ool","ool","ool"]
                tmp.append(alphanum(word))
                tmp.append(Num(word))
                tmp.append(special_char(word))
                tmp.append(English(word))
                if(front_space != 0):
                    tmp.append("True")
                    front_space = 0
                else:
                    tmp.append("False")
                tmp.append("False")


                #add dic feature n dic
                feature_extend = 8*11
                for i in range(feature_extend):
                    tmp.append("False")
                ######################

                tmp.append(label)
                vocab.append(tmp)
                tune = 0
                for i in range(vocab_count):	
                    if(vocab[i][0] == word):
                        vocab[i][1] += 1
                        if(vocab[i][1] > tune):
                            tune = vocab[i][1]
                        else:
                            vocab[i][1] = tune
            else:
                if(vocab != []):
                    i = vocab_count-1
                    vocab[i][18] = "True"
                    front_space = 1

def vocab_check():
    global vocab
    global vocab_count
    for i in range(vocab_count):
        if(vocab[i][1] >=3 ):
            vocab[i][2] = vocab[i][0]
        else:
            vocab[i][2] = "unknown"
    for i in range(vocab_count):
        f = 3
        e = 8
        for j in range(1,6):
            if(i-j >= 0):
                vocab[i][f] = vocab[i-j][2]
                f += 1
            if(i+j < vocab_count-1):
                vocab[i][e] = vocab[i+j][2]
                e += 1

def alphanum(word):
    tmp = ""
    count = 0
    for char in word:
        if(Num(char)):
            count += 1
        if(not Num(char) or not special_char(char)):
            tmp += char
    if(tmp != "" and count > 0):
        return True
    else :
        return False

def Num(word):
    return word.isdigit()

def special_char(word):
    special_chars = "!#$%&'*+-.^_`|~:"
    tmp = ""
    for sym in special_chars:
        for char in word:
            if(sym == char):
                tmp += char
    if(tmp == ""):
        return False
    else :
        return True

def English(word):
    return word.isalpha()

def dic_check():
    temp = ["ool","ool","ool","ool","ool","ool","ool","ool","ool","ool","ool"]
    for i in range(vocab_count):
        temp[5] = vocab[i][0]
        for j in range(6):
            if(i-j >= 0):
                temp[5-j] = vocab[i-j][0]
            if(i+j < vocab_count):
                temp[5+j] = vocab[i+j][0]
        ########ได้list w ที่มาเช็ค
        init = 19
        for k in range(dic_list):
            new_temp = temp    
            new_temp = match_11(dic_list[k],new_temp)
            for l in range(len(temp)):
                vocab[i][init+l] = new_temp[l]
            init += 11

def match_11(dic, temp):
    word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5] + temp[i+6] + temp[i+7] + temp[i+8] + temp[i+9] + temp[i+10]
    result = dic_compare(dic, word)
    if(result == dic[0]):
                temp[i] = dic[0] + "_start"
                temp[i+1] = dic[0] + "_cont"
                temp[i+2] = dic[0] + "_cont"
                temp[i+3] = dic[0] + "_cont"
                temp[i+4] = dic[0] + "_cont"
                temp[i+5] = dic[0] + "_cont"
                temp[i+6] = dic[0] + "_cont"
                temp[i+7] = dic[0] + "_cont"
                temp[i+8] = dic[0] + "_cont"
                temp[i+9] = dic[0] + "_cont"
                temp[i+10] = dic[0] + "_end"
    else:
        temp = match_10(dic, temp)
    return temp

def match_10(dic, temp):
    new_temp = []
    pointer = 12
    for i in range(len(temp)):
        if(temp[i] == "False" and i+9 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5] + temp[i+6] + temp[i+7] + temp[i+8] + temp[i+9]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                temp[i] = dic[0] + "_start"
                temp[i+1] = dic[0] + "_cont"
                temp[i+2] = dic[0] + "_cont"
                temp[i+3] = dic[0] + "_cont"
                temp[i+4] = dic[0] + "_cont"
                temp[i+5] = dic[0] + "_cont"
                temp[i+6] = dic[0] + "_cont"
                temp[i+7] = dic[0] + "_cont"
                temp[i+8] = dic[0] + "_cont"
                temp[i+9] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_9(dic, new_temp)
                    for j in range(len(new_temp)):
                        temp[pointer+j] = new_temp[j]
                new_temp = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
        elif(temp[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
    if(new_temp != []):
        new_temp = match_9(dic, new_temp)
        for i in range(len(new_temp)):
            temp[pointer+i] = new_temp[i]
    return temp

def match_9(dic, temp):
    new_temp = []
    pointer = 12
    for i in range(len(temp)):
        if(temp[i] == "False" and i+8 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5] + temp[i+6] + temp[i+7] + temp[i+8]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                temp[i] = dic[0] + "_start"
                temp[i+1] = dic[0] + "_cont"
                temp[i+2] = dic[0] + "_cont"
                temp[i+3] = dic[0] + "_cont"
                temp[i+4] = dic[0] + "_cont"
                temp[i+5] = dic[0] + "_cont"
                temp[i+6] = dic[0] + "_cont"
                temp[i+7] = dic[0] + "_cont"
                temp[i+8] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_8(dic, new_temp)
                    for j in range(len(new_temp)):
                        temp[pointer+j] = new_temp[j]
                new_temp = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
        elif(temp[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
    if(new_temp != []):
        new_temp = match_8(dic, new_temp)
        for i in range(len(new_temp)):
            temp[pointer+i] = new_temp[i]
    return temp

def match_8(dic, temp):
    new_temp = []
    pointer = 12
    for i in range(len(temp)):
        if(temp[i] == "False" and i+7 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5] + temp[i+6] + temp[i+7]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                temp[i] = dic[0] + "_start"
                temp[i+1] = dic[0] + "_cont"
                temp[i+2] = dic[0] + "_cont"
                temp[i+3] = dic[0] + "_cont"
                temp[i+4] = dic[0] + "_cont"
                temp[i+5] = dic[0] + "_cont"
                temp[i+6] = dic[0] + "_cont"
                temp[i+7] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_7(dic, new_temp)
                    for j in range(len(new_temp)):
                        temp[pointer+j] = new_temp[j]
                new_temp = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
        elif(temp[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
    if(new_temp != []):
        new_temp = match_7(dic, new_temp)
        for i in range(len(new_temp)):
            temp[pointer+i] = new_temp[i]
    return temp

def match_7(dic, temp):
    new_temp = []
    pointer = 12
    for i in range(len(temp)):
        if(temp[i] == "False" and i+6 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5] + temp[i+6]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                temp[i] = dic[0] + "_start"
                temp[i+1] = dic[0] + "_cont"
                temp[i+2] = dic[0] + "_cont"
                temp[i+3] = dic[0] + "_cont"
                temp[i+4] = dic[0] + "_cont"
                temp[i+5] = dic[0] + "_cont"
                temp[i+6] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_6(dic, new_temp)
                    for j in range(len(new_temp)):
                        temp[pointer+j] = new_temp[j]
                new_temp = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
        elif(temp[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
    if(new_temp != []):
        new_temp = match_6(dic, new_temp)
        for i in range(len(new_temp)):
            temp[pointer+i] = new_temp[i]
    return temp

def match_6(dic, temp):
    new_temp = []
    pointer = 12
    for i in range(len(temp)):
        if(temp[i] == "False" and i+5 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                temp[i] = dic[0] + "_start"
                temp[i+1] = dic[0] + "_cont"
                temp[i+2] = dic[0] + "_cont"
                temp[i+3] = dic[0] + "_cont"
                temp[i+4] = dic[0] + "_cont"
                temp[i+5] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_5(dic, new_temp)
                    for j in range(len(new_temp)):
                        temp[pointer+j] = new_temp[j]
                new_temp = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
        elif(temp[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
    if(new_temp != []):
        new_temp = match_5(dic, new_temp)
        for i in range(len(new_temp)):
            temp[pointer+i] = new_temp[i]
    return temp

def match_5(dic, temp):
    new_temp = []
    pointer = 12
    for i in range(len(temp)):
        if(temp[i] == "False" and i+4 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                temp[i] = dic[0] + "_start"
                temp[i+1] = dic[0] + "_cont"
                temp[i+2] = dic[0] + "_cont"
                temp[i+3] = dic[0] + "_cont"
                temp[i+4] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_4(dic, new_temp)
                    for j in range(len(new_temp)):
                        temp[pointer+j] = new_temp[j]
                new_temp = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
        elif(temp[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
    if(new_temp != []):
        new_temp = match_4(dic, new_temp)
        for i in range(len(new_temp)):
            temp[pointer+i] = new_temp[i]
    return temp

def match_4(dic, temp):
    new_temp = []
    pointer = 12
    for i in range(len(temp)):
        if(temp[i] == "False" and i+3 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                temp[i] = dic[0] + "_start"
                temp[i+1] = dic[0] + "_cont"
                temp[i+2] = dic[0] + "_cont"
                temp[i+3] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_3(dic, new_temp)
                    for j in range(len(new_temp)):
                        temp[pointer+j] = new_temp[j]
                new_temp = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
        elif(temp[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
    if(new_temp != []):
        new_temp = match_3(dic, new_temp)
        for i in range(len(new_temp)):
            temp[pointer+i] = new_temp[i]
    return temp

def match_3(dic, temp):
    new_temp = []
    pointer = 12
    for i in range(len(temp)):
        if(temp[i] == "False" and i+2 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                temp[i] = dic[0] + "_start"
                temp[i+1] = dic[0] + "_cont"
                temp[i+2] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_2(dic, new_temp)
                    for j in range(len(new_temp)):
                        temp[pointer+j] = new_temp[j]
                new_temp = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
        elif(temp[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
    if(new_temp != []):
        new_temp = match_2(dic, new_temp)
        for i in range(len(new_temp)):
            temp[pointer+i] = new_temp[i]
    return temp

def match_2(dic, temp):
    for i in range(len(temp)):
        if(temp[i] == "False" and i+1 < len(temp)):
            word = temp[i] + temp[i+1]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                temp[i] = dic[0] + "_start"
                temp[i+1] = dic[0] + "_end"
            else:
                temp[i] = dic_compare(dic,temp[0])
        elif(temp[i] == "False"):
            temp[i] = dic_compare(dic,temp[0])
    return temp

def dic_compare(dic, test):
    for word in dic[1:]:
        if(test = word):
            test = dic[0]
            return test

if __name__ == '__main__':
    read_txt(filename)
    for i in range(len(dic_list)):
        create_dic(i)
    create_vocab(corpus_text)
    vocab_check()
    dic_check()
    print(corpus_text)
    for i in vocab:
        print(i)
    print("Total is " + str(len(vocab)) + " word")
    # god tum ja
    f = open("output.txt","w+")
    for List in vocab:
        for word in List:
            f.write(str(word)+" ")
        f.write("\n")
    f.close() 
