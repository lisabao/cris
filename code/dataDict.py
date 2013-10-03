import pickle

# Goes through all clue databases and counts word frequencies
def makeDataDict():
  d = {}
  for i in range(3, 16):
    f = open("../clues/" + str(i) + ".txt")
    for line in f:
      l = line.lower().split(",", 1)
      oldClue = l[1].rstrip().strip('"').split()
      for word in oldClue:
        d[word] = d.get(word, 0) + 1
  pickle.dump(d, open("dataCount.p", "wb"))

makeDataDict()

