#vocab is list of word features
#word feature = [w0,w-1,w-2,w-3,w-4,w-5,w+1,w+2,w+3,w+4,w+5,alphanum(w0),Num(w0),special_char(w0),English(w0),blank_front(w0),blank_behind(w0),class]
#if it has dicts,dict will be appended in the end of feature list.

#define
#alphanum = contained with num and anylangauge alphabets (it can contrain special char)
#num = contained with only numberic
#special_char = atleast it has to contain special char
#English = contained with only english alphabet

#####################################################################################
import re
import sys

filename = sys.argv[1]
vocab = []
text = ""
front_space = 0
vocab_count = 0

def read_txt():
    global text
    txt_file = open(filename,"r",encoding="utf8")
    text = txt_file.read()
    txt_file.close()

def create_vocab(text):
    global front_space
    global vocab_count
    global vocab
    law = re.split(r'\|*', text)
    for comp in law:
        tmp = []
        if(comp != " " and comp != "\n"):
            vocab_count += 1
            tag = re.findall(r"\(+\w+\)",comp)
            tag1 = re.findall(r"\(+\(+\w+\)",comp)
            if(tag1 != []):
                word = "("
                temp = tag[0]
                tag[0] = temp[1:]
            elif(tag == []):
                tag.append("o")
                word = comp
            else:
                word =  comp.replace(tag[0], "")
            tmp = [word,"ool","ool","ool","ool","ool","ool","ool","ool","ool","ool"]
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
            tmp.append(tag)
            vocab.append(tmp)
        else:
            if(vocab != []):
                i = vocab_count-1
                vocab[i][16] = "True"
                front_space = 1
    for i in range(vocab_count):
        f = 1
        e = 6
        for j in range(1,6):
            if(i-j >= 0):
                vocab[i][f] = vocab[i-j][0]
                f += 1
            if(i+j < vocab_count-1):
                vocab[i][e] = vocab[i+j][0]
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
    read_txt()
    create_vocab(text)
    print(text)
    print(vocab)
    print("Total is " + str(len(vocab)) + " word")
    #f = open("train.txt","w+")
    #f.write(vocab)
    #f.close() 
