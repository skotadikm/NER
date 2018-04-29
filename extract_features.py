#vocab is list of word features
#word feature = [original word,w0,w-1,w-2,w-3,w-4,w-5,w+1,w+2,w+3,w+4,w+5,alphanum(w0),Num(w0),special_char(w0),English(w0),blank_front(w0),blank_behind(w0),dic n dic,class]
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
dicname = sys.argv[2]
vocab = []
corpus_text = ""
front_space = 0
vocab_count = 0

#original dictionary
dic_list = []

def create_dic_list(dicname):
    tmp = glob.glob("/home/tin/scripts/extract_feature/NER/dic/"+'*')
    tmp.sort()
    temp = []
    for path in tmp:
        i = re.split(r'\/', path)
        name = i[len(i)-1].replace(".txt", "")
        temp.append(name)
        txt_file = open(path,"r",encoding="utf-8-sig")
        text = txt_file.read()
        txt_file.close()
        raw = re.split(r'\n', text)
        for comp in raw:
            temp.append(comp)
        dic_list.append(temp)
        temp = []
    tmp = []
    txt_file = open(dicname,"r",encoding="utf-8-sig")
    text = txt_file.read()
    txt_file.close()
    tmp = re.split(r'/n', text)
    for path in tmp:
        i = re.split(r'\/', path)
        name = i[len(i)-1].replace(".txt", "")
        temp.append(name)
        txt_file = open(path,"r",encoding="utf-8-sig")
        text = txt_file.read()
        txt_file.close()
        raw = re.split(r'\n', text)
        for comp in raw:
            temp.append(comp)
        dic_list.append(temp)
        temp = []
    for i in range(len(dic_list)):
        print(dic_list[i][0])

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
    tmp = glob.glob(corpus+'*')
    for i in tmp:
        txt_file = open(i,"r",encoding="utf-8-sig")
        corpus_text += txt_file.read()
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

def dic_check(dic,index):
    temp = []
    checklist = []
    tmp = ""
    check_in_dic = False
    check_substring = False
    maxlength = 0
    for i in range(vocab_count):
        checklist = ["False",0]
        for j in range(vocab_count):
            if(i+j > vocab_count-1):
                break
            tmp += vocab[i+j][0]
            for word in dic:
                if(tmp == word):
                    check_in_dic = True
                if(word.startswith(tmp)):
                    check_substring = True    
                if(check_in_dic and check_substring):
                    break            
            if(check_substring):
                checklist[1] += 1
            else:
                tmp = ""
                break
            checklist.append(check_in_dic)
            check_in_dic = False
            check_substring = False
        for i in range(checklist[1]):
            if(checklist[checklist[1]-i+1]):
                checklist[1] = checklist[1] - i
                break
            elif(checklist[1] - i == 1):
                checklist[1] = 0
            checklist.pop()
        if(checklist[1] > maxlength):
            maxlength = checklist[1]
        temp.append(checklist)
    temp =  dic_summary(temp, maxlength, dic)
    for i in range(vocab_count):
        vocab[i][18+index] = temp[i][0]
            
def dic_summary(temp, maxlength, dic):
    #temp = [[label,maxlength,1,2,3,4,...,maxlength]]
    for i in range(maxlength):
        index = maxlength - i
        for j in range(vocab_count):
            if(temp[j][1] == index):
                init = 0
                for k in range(index):
                    if(temp[j+k][0] == "False"):
                        init += 1

                if(init == temp[j][1] and init > 2):
                    temp[j][0] = dic[0] + "_start"
                    temp[j+index-1][0] = dic[0] + "_end"
                    for l in range(1,index-1):
                        temp[j+l][0] = dic[0] + "_cont"
                elif(init == temp[j][1] and init == 2):
                    temp[j][0] = dic[0] + "_start"
                    temp[j+index-1][0] = dic[0] + "_end"
                elif(init == temp[j][1] and init == 1):
                    temp[j][0] = dic[0]
                else:
                    for l in range(init):
                        if(temp[j][init+1]):
                            temp[j][1] = init
                            break    
                        init -= 1
                        temp[j].pop()
                        if(len(temp[j]) == 2):
                            temp[j][1] = 0

    return temp

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
    create_dic_list(dicname)
    create_vocab(corpus_text)
    vocab_check()
    """
    for i in range(len(dic_list)):
        dic_check(dic_list[i],i)
    """

    """
    for i in vocab:
        print(i)
    print("Total is " + str(len(vocab)) + " word")
    """
    # god tum ja
    f = open("output.txt","w+")
    c = 0
    for List in vocab:
        i = 0
        c += 1
        for word in List:
            i += 1
            f.write(str(word))
            if(i < len(List)):
                f.write("\t")
        if(c < vocab_count):
            f.write("\n")
    f.close() 
