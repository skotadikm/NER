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
common = []
loc_name = []
loc_clue = []
org_name = []
org_clue = []
per_clue = []
per_first = []
per_last = []

def create_dic(dic):
    #แก้ไขpath dic
    filenames = "loc_clue"
    txt_file = open(filenames+".txt","r",encoding="utf8")
    text = txt_file.read()
    txt_file.close()
    print (text)
    raw = re.split(r'\n', text)
    for comp in raw:
        count = 0
        front = 0
        tmp = []
        if(comp != " "):
            count += 1
            tmp.append(comp)
            if(front_space != 0):
                    tmp.append("True")
                    front = 0
                else:
                    tmp.append("False")
            tmp.append("False")
            dic.append(tmp)
        else:
            if(dic != []):
                i = count-1
                dic[i][2] = "True"
                front = 1

    oldstr = dic[0][0]
    dic[0][0] = oldstr.replace("\ufeff", "")
    print(dic)    

def read_txt(filenames):
    global corpus_text
    txt_file = open(filenames,"r",encoding="utf8")
    corpus_text = txt_file.read()
    txt_file.close()

def create_vocab(corpus_text):
    global front_space
    global vocab_count
    global vocab
    raw = re.split(r'\|*', corpus_text)
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
        print(tmp)
        print(count)
        return True
    else :
        print(tmp)
        print(count)
        return False

def Num(word):
    return word.isdigit()
    #return any(char.isdigit() for char in word)

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

if __name__ == '__main__':
    read_txt(filename)
    create_dic(loc_clue)
    create_vocab(corpus_text)
    vocab_check()
    print(corpus_text)
    for i in vocab:
        print(i)
    print("Total is " + str(len(vocab)) + " word")


# god tum ja
    f = open("output.txt","w+")
    for List in vocab:
        for word in List:
            f.write("|"+str(word))
        f.write("|"+"\n")
    f.close() 
