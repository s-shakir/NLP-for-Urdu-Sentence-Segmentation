# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/gdrive')
# %cd /gdrive

from google.colab import drive
drive.mount('/content/gdrive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/gdrive/My Drive

import re
import os
import csv
import sys
import random

"""# code:"""

def training_model():
  c = []
  nxt = []
  with open('training_corpus.txt', encoding="utf-8") as f1:
      print("segmented training corpus: ")
      for line in f1:#split text in line
        print(line)
        for word in line.split(): #split line into words
        # find all the stop words or boundary words that indicates end of line
          w = re.findall('\w+(?=\s*۔)', word) # find all the words \w+ before the symbol ۔?=\s*
          if w: #if you find the words before symbol ۔
            c += w # add the words in list
  stop_words = list(set(c)) # convert list to set to eliminate any duplicates


  with open('training_corpus.txt', encoding="utf-8") as f1:
      for line in f1:
        word = line.split()
        # find all the continuing words or words if found you can't put full stop afterwards even if there is stop word
        for idx, w in enumerate(word): # store the word and it's corresponding index
          if w in stop_words: # check if the word is present in stop_words
            chk = word[idx + 1] # if the word is stop_word, get word after this word
            if chk != "۔": # if the next word is not symbol ۔ then add that word to a list
              nxt.append(chk)

  nxt_words = list(set(nxt)) # remove duplicates

  return stop_words, nxt_words

def testing_model(stop_words, nxt_words):
  k = " "
  with open('sent-test.txt', encoding="utf-8") as f2:
      print("\nunsegmented test text: ")
      for line in f2:
        print(line)
        word = line.split()
        # read the words and check if there are stop words if there is no next_word after it then split the line and put it as a seperate line in the list
        for idx, w in enumerate(word):
           if w in stop_words: # check if the word is stop word
             k = word[idx + 1] # get next word to the stop word
           for i in nxt_words: # check if the next word is not continuiung word
             if k != i:
                lines = line.split(k) # split the line indicating end of sentence and store it in list
  output = list(set(lines)) # remove duplicates
  print("\n after segmentation: ", output)

  with open('output.txt', 'wt', encoding="utf-8") as f2: #open a file to write the segmented text
    for item in output:
      f2.write("%s۔" % item)# copy the lines from the list above into the file

  return output


def model_accuracy():
  c2 = []
  c3 = []
  res = 0
  with open('output.txt', encoding="utf-8") as f3:
    for line in f3:
      for word in line.split():
        w = re.findall('\w+(?=\s*۔)', word) # find end of sentence in the text file
        if w: # find words indicating end of sentence
          c2 += w
  out_eos = list(set(c2))

  with open('sent-segmented.txt', encoding="utf-8") as f4:
    for line in f4:
      for word in line.split():
        w = re.findall('\w+(?=\s*۔)', word) # find end of sentence in the text file
        if w:# find words indicating end of sentence
          c3 += w
  seg_eos = list(set(c3))

  if(set(out_eos).intersection(seg_eos)): # check if the above to list have similar end of sentence
    res += 1 # if yes then add the counter
  score = (res/len(seg_eos))*100 #calculate overall score by diving the count with total number of sentences in the segmented file and multiply by 100

  print("\naccuracy score between two text files is: ",score,"%")

def main():
  stop_words, nxt_words = training_model()
  output = testing_model(stop_words, nxt_words)
  model_accuracy()

if __name__ == '__main__':
    main()

