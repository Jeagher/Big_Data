#!/usr/bin/env python3

# python vowel_mrjob.py -r inline < dic_fr.txt  > resultInline.txt

#-*- coding: utf-8 -*-
from mrjob.job import MRJob
from mrjob.step import MRStep
import unicodedata

class MRWordCount(MRJob):
  def mapper1(self, _, word):
    vowels = ['a','i','o','u','e','y']
    
    # unicodedata library to remoove accents in latin words, it keeps only the simplest unicode entities 
    def strip_accents(s):
      return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    
    clean_word = strip_accents(word)
    valid = True
    first_vowel = None
    for i in range(len(clean_word)) : 
      char = clean_word[i]
      if char in vowels :
        if first_vowel is None : # If no vowel encountered yet 
          first_vowel = char
        else :
          if first_vowel != char :
            valid = False
            break # Break, the word has 2 diffent vowels 
    if valid == True and first_vowel != None and '-' not in clean_word: # remoove portmanteau words 
      yield(first_vowel, (len(clean_word), clean_word))
        
  def reducer1(self, first_vowel, tuple):
    yield(first_vowel, max(tuple, key=lambda x:x[0]))
  
  def steps(self):
      return [
          MRStep(mapper=self.mapper1, reducer=self.reducer1)
      ]

if __name__ == '__main__':
    MRWordCount.run()