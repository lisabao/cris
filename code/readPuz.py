from grid import *

# Read a .puz file and extracts a string representing the blank puzzle,
# the solved puzzle, and a list of the clues
def parsePuz(filename):
  f = open(filename, "r")
  for line in f:
    l = line
  answers = l[52:277]
  blank = l[277:502]
  #i = 532
  i = 502
  while l[i:i+5] != "Times":
    i += 1
  i += 5
  while l[i:i+5] != "Times":
    i += 1
  i += 5
  clues = l[i+1:]
  cluesList = []
  s= ""
  i = 0
  while i < len(clues) - 1 and (i + 2 > len(clues) or clues[i:i+3] != "GRB"):
    while clues[i] != "\x00":
      s += clues[i]
      i += 1
      #print i
    #print "Adding", s
    cluesList.append(s)
    s = ""
    i += 1
    #print "\t", i, len(clues)
  if cluesList[-1] == "":
    cluesList = cluesList[:-1]

  return blank, answers, cluesList

# 52 = start of answers
# 52 + 15 * 15 = 277 = start of blank layout
# 277 + 15 * 15 = 502 = start of info
# 584 = start of clues

# Returns a correct and a blank puzzle and the cluelist
def readPuz(filename):
  blank, answers, cluesList = parsePuz(filename)
  c = Grid(15, answers)
  b = Grid(15, blank)
  return c, b, cluesList

def main():
  c, b, cluesList = readPuz("../puz/Dec1412.puz")

  print b
  b.printEmpty()
  b.addClues(cluesList)
  b.printClues()
  print b
  #print cluesList
  #g.printEmpty()
  return 0


if __name__=="__main__":
  main()
