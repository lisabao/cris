from operator import itemgetter
from readPuz import *
import pickle
import re

def unigramDiscountedAnswer(length, clue):
  dataDict = pickle.load(open("dataCount.p", "rb"))
  """
  dl = dataDict.items()
  dl.sort(key=itemgetter(1), reverse=True)
  print dl[:20]
  print
  print dl[-20:]
  """

  possAnswers = {}
  f = open("../clues/" + str(length) + ".txt")
  thisClue = clue.lower().strip('*').strip('?').split() #hm
  for line in f:
    l = line.lower().split(",", 1)
    answer = l[0]
    oldClue = l[1].rstrip().strip('"').strip('*').strip('?').split()
    score = 0
    if thisClue == oldClue:
      score = 1
    for token in thisClue:      # for word in this mystery clue:
      if token in oldClue:      # +1 to score if it appears in the database line
        score += 1.0 / dataDict[token] # divide by frequency in entire database
    possAnswers[answer] = possAnswers.get(answer, .00001) + score # smoothing

  listAnswers = possAnswers.items()
  total = sum([ans[1] for ans in listAnswers])
  sortedAnswers = sorted(listAnswers, key=itemgetter(1), reverse=True)
  return sortedAnswers


def main():
  g, f, clues = readPuz("../puz/Dec1412.puz")
  g.printEmpty()
  g.addClues(clues)
  g.printClues()
  for num in g.clues:
    clue = g.clues[num]
    length = g.readAnswer(num)
    print length
    print num, clue, len(length)
    #unigramAnswer(len(length), clue)
    answers = unigramDiscountedAnswer(len(length), clue)
    print answers[:10]


if __name__=="__main__":
  main()
