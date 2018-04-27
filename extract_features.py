#vocab is list of word features
#word feature = [original word,w0,w-1,w-2,w-3,w-4,w-5,w+1,w+2,w+3,w+4,w+5,alphanum(w0),Num(w0),special_char(w0),English(w0),blank_front(w0),blank_behind(w0),class]
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
import glob

corpus = sys.argv[1]
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

def read_corpus(corpus):
    global corpus_text
    print(glob.glob(corpus))
    for i in glob.glob(corpus):
        txt_file = open(i,"r",encoding="utf-8-sig")
        print(txt_file)
        corpus_text += txt_file.read()
        print(corpus_text)
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
                feature_extend = len(dic_list)
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
    for i in range(vocab_count):
        del vocab[i][1]

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
"""
def dic_check(dic,index):
    tmp = ""
    check = False
    init = 0
    for i in range(vocab_count):
        if(check):
            tmp += vocab[i][0]
            counter += 1
        else:
            if(counter == 1):
                vocab[init][index] = dic[0]
            elif(counter > 1):
                vocab[init][index] = dic[0] + "_start"
                vocab[init+counter][index] = dic[0] + "_end"
                for k in range(1,counter-1):
                    vocab[init+k][index] = dic[0] + "_cont"
            tmp = vocab[i][0]
            intit = i
        for word in dic:
            if(tmpเ is word substring):
                check = True
                break
            check = False
"""            
def dic_check_11words():
    temp = ["ool","ool","ool","ool","ool","ool","ool","ool","ool","ool","ool"]
    check_list = ["False","False","False","False","False","False","False","False","False","False","False"]
    for i in range(vocab_count):
        temp[5] = vocab[i][0]
        for j in range(6):
            if(i-j >= 0):
                temp[5-j] = vocab[i-j][0]
            if(i+j < vocab_count):
                temp[5+j] = vocab[i+j][0]
            if(i+j >= vocab_count):
                temp[5+j] = "ool"
        ########ได้list w ที่มาเช็ค
        init = 19
        for k in range(len(dic_list)):    
            check_list = match_11(dic_list[k],temp,check_list)
            for l in range(len(temp)):
                vocab[i][init+l] = check_list[l]
            print(check_list)
            print(temp)
            check_list = ["False","False","False","False","False","False","False","False","False","False","False"]
            init += 11

def match_11(dic, temp, check_list):
    word = ""
    for i in range(len(temp)):
        word += temp[i]
    result = dic_compare(dic, word)
    if(result == dic[0]):
                check_list[i] = dic[0] + "_start"
                check_list[i+1] = dic[0] + "_cont"
                check_list[i+2] = dic[0] + "_cont"
                check_list[i+3] = dic[0] + "_cont"
                check_list[i+4] = dic[0] + "_cont"
                check_list[i+5] = dic[0] + "_cont"
                check_list[i+6] = dic[0] + "_cont"
                check_list[i+7] = dic[0] + "_cont"
                check_list[i+8] = dic[0] + "_cont"
                check_list[i+9] = dic[0] + "_cont"
                check_list[i+10] = dic[0] + "_end"
    else:
        check_list = match_10(dic, temp, check_list)
    return check_list

def match_10(dic, temp, check_list):
    new_temp = []
    new_check_list = []
    pointer = 12
    for i in range(len(temp)):
        if(check_list[i] == "False" and i+9 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5] + temp[i+6] + temp[i+7] + temp[i+8] + temp[i+9]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                check_list[i] = dic[0] + "_start"
                check_list[i+1] = dic[0] + "_cont"
                check_list[i+2] = dic[0] + "_cont"
                check_list[i+3] = dic[0] + "_cont"
                check_list[i+4] = dic[0] + "_cont"
                check_list[i+5] = dic[0] + "_cont"
                check_list[i+6] = dic[0] + "_cont"
                check_list[i+7] = dic[0] + "_cont"
                check_list[i+8] = dic[0] + "_cont"
                check_list[i+9] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_9(dic, new_temp, new_check_list)
                    for j in range(len(new_temp)):
                        check_list[pointer+j] = new_temp[j]
                new_temp = []
                new_check_list = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
                new_check_list.append(check_list[i])
        elif(check_list[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
            new_check_list.append(check_list[i])
    if(new_temp != []):
        new_temp = match_9(dic, new_temp, new_check_list)
        for i in range(len(new_temp)):
            check_list[pointer+i] = new_temp[i]
    return check_list

def match_9(dic, temp, check_list):
    new_temp = []
    new_check_list = []
    pointer = 12
    for i in range(len(temp)):
        if(check_list[i] == "False" and i+8 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5] + temp[i+6] + temp[i+7] + temp[i+8]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                check_list[i] = dic[0] + "_start"
                check_list[i+1] = dic[0] + "_cont"
                check_list[i+2] = dic[0] + "_cont"
                check_list[i+3] = dic[0] + "_cont"
                check_list[i+4] = dic[0] + "_cont"
                check_list[i+5] = dic[0] + "_cont"
                check_list[i+6] = dic[0] + "_cont"
                check_list[i+7] = dic[0] + "_cont"
                check_list[i+8] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_8(dic, new_temp, new_check_list)
                    for j in range(len(new_temp)):
                        check_list[pointer+j] = new_temp[j]
                new_temp = []
                new_check_list = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
                new_check_list.append(check_list[i])
        elif(check_list[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
            new_check_list.append(check_list[i])
    if(new_temp != []):
        new_temp = match_8(dic, new_temp, new_check_list)
        for i in range(len(new_temp)):
            check_list[pointer+i] = new_temp[i]
    return check_list

def match_8(dic, temp, check_list):
    new_temp = []
    new_check_list = []
    pointer = 12
    for i in range(len(temp)):
        if(check_list[i] == "False" and i+7 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5] + temp[i+6] + temp[i+7]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                check_list[i] = dic[0] + "_start"
                check_list[i+1] = dic[0] + "_cont"
                check_list[i+2] = dic[0] + "_cont"
                check_list[i+3] = dic[0] + "_cont"
                check_list[i+4] = dic[0] + "_cont"
                check_list[i+5] = dic[0] + "_cont"
                check_list[i+6] = dic[0] + "_cont"
                check_list[i+7] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_7(dic, new_temp, new_check_list)
                    for j in range(len(new_temp)):
                        check_list[pointer+j] = new_temp[j]
                new_temp = []
                new_check_list = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
                new_check_list.append(check_list[i])
        elif(check_list[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
            new_check_list.append(check_list[i])
    if(new_temp != []):
        new_temp = match_7(dic, new_temp, new_check_list)
        for i in range(len(new_temp)):
            check_list[pointer+i] = new_temp[i]
    return check_list

def match_7(dic, temp, check_list):
    new_temp = []
    new_check_list = []
    pointer = 12
    for i in range(len(temp)):
        if(check_list[i] == "False" and i+6 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5] + temp[i+6]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                check_list[i] = dic[0] + "_start"
                check_list[i+1] = dic[0] + "_cont"
                check_list[i+2] = dic[0] + "_cont"
                check_list[i+3] = dic[0] + "_cont"
                check_list[i+4] = dic[0] + "_cont"
                check_list[i+5] = dic[0] + "_cont"
                check_list[i+6] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_6(dic, new_temp, new_check_list)
                    for j in range(len(new_temp)):
                        check_list[pointer+j] = new_temp[j]
                new_temp = []
                new_check_list = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
                new_check_list.append(check_list[i])
        elif(check_list[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
            new_check_list.append(check_list[i])
    if(new_temp != []):
        new_temp = match_6(dic, new_temp, new_check_list)
        for i in range(len(new_temp)):
            check_list[pointer+i] = new_temp[i]
    return check_list

def match_6(dic, temp, check_list):
    new_temp = []
    new_check_list = []
    pointer = 12
    for i in range(len(temp)):
        if(check_list[i] == "False" and i+5 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4] + temp[i+5]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                check_list[i] = dic[0] + "_start"
                check_list[i+1] = dic[0] + "_cont"
                check_list[i+2] = dic[0] + "_cont"
                check_list[i+3] = dic[0] + "_cont"
                check_list[i+4] = dic[0] + "_cont"
                check_list[i+5] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_5(dic, new_temp, new_check_list)
                    for j in range(len(new_temp)):
                        check_list[pointer+j] = new_temp[j]
                new_temp = []
                new_check_list = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
                new_check_list.append(check_list[i])
        elif(check_list[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
            new_check_list.append(check_list[i])
    if(new_temp != []):
        new_temp = match_5(dic, new_temp, new_check_list)
        for i in range(len(new_temp)):
            check_list[pointer+i] = new_temp[i]
    return check_list

def match_5(dic, temp, check_list):
    new_temp = []
    new_check_list = []
    pointer = 12
    for i in range(len(temp)):
        if(check_list[i] == "False" and i+4 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3] + temp[i+4]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                check_list[i] = dic[0] + "_start"
                check_list[i+1] = dic[0] + "_cont"
                check_list[i+2] = dic[0] + "_cont"
                check_list[i+3] = dic[0] + "_cont"
                check_list[i+4] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_4(dic, new_temp, new_check_list)
                    for j in range(len(new_temp)):
                        check_list[pointer+j] = new_temp[j]
                new_temp = []
                new_check_list = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
                new_check_list.append(check_list[i])
        elif(check_list[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
            new_check_list.append(check_list[i])
    if(new_temp != []):
        new_temp = match_4(dic, new_temp, new_check_list)
        for i in range(len(new_temp)):
            check_list[pointer+i] = new_temp[i]
    return check_list

def match_4(dic, temp, check_list):
    new_temp = []
    new_check_list = []
    pointer = 12
    for i in range(len(temp)):
        if(check_list[i] == "False" and i+3 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2] + temp[i+3]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                check_list[i] = dic[0] + "_start"
                check_list[i+1] = dic[0] + "_cont"
                check_list[i+2] = dic[0] + "_cont"
                check_list[i+3] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_3(dic, new_temp, new_check_list)
                    for j in range(len(new_temp)):
                        check_list[pointer+j] = new_temp[j]
                new_temp = []
                new_check_list = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
                new_check_list.append(check_list[i])
        elif(check_list[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
            new_check_list.append(check_list[i])
    if(new_temp != []):
        new_temp = match_3(dic, new_temp, new_check_list)
        for i in range(len(new_temp)):
            check_list[pointer+i] = new_temp[i]
    return check_list

def match_3(dic, temp, check_list):
    new_temp = []
    new_check_list = []
    pointer = 12
    for i in range(len(temp)):
        if(check_list[i] == "False" and i+2 < len(temp)):
            word = temp[i] + temp[i+1] + temp[i+2]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                check_list[i] = dic[0] + "_start"
                check_list[i+1] = dic[0] + "_cont"
                check_list[i+2] = dic[0] + "_end"
                if(new_temp != []):
                    new_temp = match_2(dic, new_temp, new_check_list)
                    for j in range(len(new_temp)):
                        check_list[pointer+j] = new_temp[j]
                new_temp = []
                new_check_list = []
                pointer = 12
            else:
                if(pointer > i):
                    pointer = i
                new_temp.append(temp[i])
                new_check_list.append(check_list[i])
        elif(check_list[i] == "False"):
            if(pointer > i):
                    pointer = i
            new_temp.append(temp[i])
            new_check_list.append(check_list[i])
    if(new_temp != []):
        new_temp = match_2(dic, new_temp, new_check_list)
        for i in range(len(new_temp)):
            check_list[pointer+i] = new_temp[i]
    return check_list

def match_2(dic, temp, check_list):
    for i in range(len(temp)):
        if(check_list[i] == "False" and i+1 < len(temp)):
            word = temp[i] + temp[i+1]
            result = dic_compare(dic, word)
            if(result == dic[0]):
                check_list[i] = dic[0] + "_start"
                check_list[i+1] = dic[0] + "_end"
            else:
                check_list[i] = dic_compare(dic,temp[i])
        elif(check_list[i] == "False"):
            check_list[i] = dic_compare(dic,temp[i])
    return check_list

def dic_compare(dic, test):
    for word in dic:
        if(test == word):
            return dic[0]
    return "False"

if __name__ == '__main__':
    read_corpus(corpus)
    for i in range(len(dic_list)):
        create_dic(i)
    create_vocab(corpus_text)
    vocab_check()
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
