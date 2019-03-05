#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 18:50:02 2019

@author: sonalijohari
"""

import nltk
from nltk.util import ngrams
from nltk.tokenize import sent_tokenize
from nltk import load

# return all the 'adv adj' twograms
"""def getAdvAdjTwograms(terms,adj,adv):
    result=[]
    twograms = ngrams(terms,2) #compute 2-grams    
   	 #for each 2gram
    for tg in twograms:  
        if tg[0] in adv and tg[1] in adj: # if the 2gram is a an adverb followed by an adjective
            result.append(tg)

    return result"""

def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())# remember to strip to remove the lin-change character
    lex_conn.close()

    return newLex

# return all the terms that belong to a specific POS type
def getPOSterms(terms,POStags,tagger):
	
    tagged_terms=tagger.tag(terms)#do POS tagging on the tokenized sentence

    POSterms={}
    for tag in POStags:POSterms[tag]=set()

    #for each tagged term
    for pair in tagged_terms:
        for tag in POStags: # for each POS tag 
            if pair[1].startswith(tag): POSterms[tag].add(pair[0].lower())

    return POSterms


def processSentence(sentence, posLex, negLex, tagger):
    result=[]
    
    
    #tokenize the sentence
    terms = nltk.word_tokenize(sentence.lower())   

    POStags=['NN'] # POS tags of interest 		
    POSterms=getPOSterms(terms,POStags,tagger)

    noun=POSterms['NN']
        
    
    fourgrams = ngrams(terms,4) #compute 2-grams    
   	 #for each 4gram
    for tg in fourgrams:  
        if tg[0] == "not" and tg[2] in posLex or tg[2] in negLex and tg[3] in noun: # if the 4gram is in the format "not <any word> <pos/neg word> <noun>
            result.append(tg)

    return result




def run(fpath):
    
    posLex = loadLexicon("positive-words.txt")
    negLex = loadLexicon("negative-words.txt")

    #make a new tagger
    _POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
    tagger = load(_POS_TAGGER)

    #read the input
    f=open(fpath)
    text=f.read().strip()
    f.close()

    #split sentences
    sentences=sent_tokenize(text)
    
    fgram=[]

  

    # for each sentence
    for sentence in sentences:

        
        fgram += processSentence(sentence,posLex, negLex,tagger)
        #adjAfterAdv+=getAdvAdjTwograms(terms, adjectives, adverbs)
		
    return fgram


if __name__=='__main__':
    print (run('input.txt'))



