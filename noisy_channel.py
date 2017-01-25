import re
import collections as cc
text=re.findall(r'\w+', open('C:/Users/rishav106934/Desktop/big.txt').read().lower())


def unigm(text): 
    return cc.Counter(text)

unigm_set=unigm(text)

def P(words):
    N= sum(unigm_set.values())
    return unigm_set[words]/N


def correct_word(word): 
    #print(len(edits))
    candidates=candidate(word)
    knowns=known(candidates)
    #print(knowns)
    pwx={x : candidates[x]*P(x) for x in knowns}
    #print(pwx)
    if knowns:
        return max(pwx, key =pwx.get)
    return word

def known(word):
    return set(w for w in word if w in unigm_set)

def candidate(word):
    edits=edits1(word)
    if word in unigm_set.keys():
        edits.update({word:0.9})
    edit_2=edits2(word)
    for k in edit_2.keys():
        if k not in edits.keys():
            edits[k]=edit_2[k]
    return edits

def edits1(word):
    word=re.sub('[^A-Za-z]+', '', word.lower())
    letters="abcdefghijklmnopqrstuvwxyz"
    splits= [(word[:i], word[i:]) for i in range(len(word)+1)]
    edits={}
    deletes = deletes1(word, splits, letters)
    edits.update(deletes)
   # print(len(edits))
    inserts = inserts1(word, splits, letters)
    edits.update(inserts)
    #print(len(edits))
    subts = { L +c +R[1:] : subs[letters.index(c), letters.index(R[0])]/counts1[c]  for L,R in splits if R for c in letters}
    edits.update(subts)
    #print(len(edits))
    transpose= { L + R[1]+R[0]+R[2:] : transp[letters.index(R[0]), letters.index(R[1]) ] /counts[R[1], R[0] ]  for L, R in splits if len(R)>1}
    edits.update(transpose)
    #print(len(edits))
    return edits

def edits2(word):
    edits=edits1(word)
    e2={}
    for e in edits.keys():
        e2.update(edits1(e))
    return e2

def deletes1(word, splits, letters):
    letters="abcdefghijklmnopqrstuvwxyz"
    splits= [(word[:i], word[i:]) for i in range(len(word)+1)]
    deletes={}
    for L,R in splits:
        if R:
            if L:
                deletes.update( {L+R[1:] : delete[ letters.index(L[-1]), letters.index(R[0]) ]/ counts[ L[-1], R[0] ]})
            else:
                deletes.update({ R[1:] : delete[26, letters.index(R[0]) ]/counts1[R[0]]})
    return(deletes)

def inserts1(word, splits, letters):
    inserts={}
    for c in letters:
        for L,R in splits:
            if L:
                inserts.update( { L+c+R: insert[letters.index(L[-1]), letters.index(c)]/counts1[L[-1]]  })
            else:
                inserts.update({ c+R : insert[26, letters.index(c)]/counts1[c] })
    return(inserts)


import numpy as np

delete =  np.reshape(np.array([int(i) for i in open('C:/Users/rishav106934/Desktop/del.txt').read().strip(' ').split(' \n')]), (27,26))

insert= np.reshape(np.array([int(i) for i in   open('C:/Users/rishav106934/Desktop/ins.txt').read().split(' \n') ] ), (27,26))

subs= np.reshape(np.array( [ int(i) for i in open('C:/Users/rishav106934/Desktop/subs.txt').read().split(' \n')]), (26,26))

transp= np.reshape(np.array( [ int (i) for i in open('C:/Users/rishav106934/Desktop/trans.txt').read().split(' \n')]), (26,26))

def countbig(text):
    return [b for x in text for b in zip(x[:-1], x[1:])]

counts=unigm(countbig(text))
counts1=unigm([b for x in text for b in x])
