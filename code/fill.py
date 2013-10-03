from cris import *
import copy

###########################################################################
### A Square object storing letter probabilites

class FillSquare(Square):
  def __init__(self, r, c, black = False):
    Square.__init__(self, r, c, black)
    self.letters = {} # key is letter, value is probability


  # Return the highest-probability string
  def getTop(self):
    letterList = sorted(self.letters.items(), key=itemgetter(1), reverse=True)
    if len(letterList) == 0:
      return "-"
    return letterList[0][0]
    
###########################################################################
### A Grid object storing answer probabilities for each number


class FillGrid(Grid):
  def __init__(self, filename):
    blank, answers, cluesList = parsePuz(filename)
    Grid.__init__(self, 15, blank)
    self.addClues(cluesList)
    self.possAnswers = {} # key = num, value = list of [answer, prob] pairs
    self.origAnswers = {} # same as above, but never changes


  # Builds grid from a string of "-" for blank and "." for black
  def buildGridString(self, contents):
    if len(contents) != self.size * self.size:
      print "Error: mistmatch between grid size and grid array"

    grid = []
    for r in range(self.size):
      row = []
      for c in range(self.size):
        if contents[c] == ".":
          s = FillSquare(r, c, True)
        else:  
          s = FillSquare(r, c)
          s.letter = contents[c]
        row.append(s)
      grid.append(row)
      contents = contents[self.size:]
    return grid


  # Fills possAnswers using unigramDiscountedAnswer
  def getPossibleAnswers(self):
    for num in self.clues:
      clue = self.clues[num]
      length = len(self.squares(num))
      answers = unigramDiscountedAnswer(length, clue)
      self.possAnswers[num] = answers
      self.origAnswers[num] = dict(answers)


  # Checks if two strings are compatible ( - for blank)
  def compatible(self, s1, s2):
    if len(s1) != len(s2):
      return False
    for i in range(len(s1)):
      if s1[i] != '-' and s2[i] != '-' and s1[i] != s2[i]:
        return False
    return True


############################################################################
### Fill grid iteratively by adding most likely words

  def fillWords(self, verbose = 0):
    print "Filling..."
    good = True
    while good and not self.isFull():
      good, affected = self.fixWords(1) # Write top word
      if verbose:
        print self
      if not good:
        break
      self.eliminate(affected)          # Eliminate words that conflict with grid
      self.normalizeWordProbs(affected) # Normalize word probs for each number


  # Normalizes the probabilites of words for each clue
  def normalizeWordProbs(self, affected):
    for num in affected:
      if len(self.possAnswers[num]) > 0:
        total = sum([ans[1] for ans in self.possAnswers[num]])
        if total > 0:
          normalAnswers = []
          for ans in self.possAnswers[num]:
            normalAnswers.append([ans[0], ans[1] / total])
          self.possAnswers[num] = normalAnswers

  # Fills in the top n words and returns the numbers affected
  def fixWords(self, n):
    topWords = []
    for num in self.possAnswers:
      if len(self.possAnswers[num]) > 0:
        topWords.append([self.possAnswers[num][0][1], num])
    topWords.sort(reverse = True)
    saff = [] # Affected squares
    for i in range(n):
      if i >= len(topWords):
        return False, None
      num = topWords[i][1]
      answer = self.possAnswers[num][0][0]
      self.fillAnswer(num, answer)
      self.possAnswers[num] = []
      saff += self.squares(num)
    saff = set(saff)
    affected = self.allAffected(saff)
    return True, affected


  # Eliminates possible answers that don't fit with the current grid
  def eliminate(self, affected):
    for num in affected:
      compAnswers = []
      current = self.readAnswer(num)
      compAnswers = [ans for ans in self.possAnswers[num] if self.compatible(current, ans[0])]
      self.possAnswers[num] = compAnswers


############################################################################
### Fills grid iteratively using most likely letters

  def fillLetters(self, verbose = 0):
    print "Filling..."
    good = True
    affected = self.possAnswers.keys()
    saff = self.allSquares(affected)
    while good and not self.isFull():
      self.fillLetterProbs(saff)    # Uses word prob to fill letter prob
      self.normalizeLetterProbs(saff)   # Normalize letter prob for each square
      good, affected = self.fixLetters(5) # Writes in top 5 letters
      if verbose:
        print self
      if not good:
        break      
      saff = self.allSquares(affected)
      self.eliminate(affected)          # Eliminates words that conflict with grid
      self.reset(saff)                  # Reset letter prob
      self.normalizeWordProbs(affected) # Normalize word prob for each num


  # Adds all letter probabilities based on possAnswers
  def fillLetterProbs(self, saff):
    for square in saff:
      self.fillSquareProbs(square)


  # Given a square, fills the letter probabilities with intersecting words
  def fillSquareProbs(self, square):
    nums = self.affectedNumbers(square.r, square.c)
    for num in nums:
      for answer in self.possAnswers[num]:
        if num[-1] == "A":
          diff = square.c - self.numbers[int(num[:-1])][1]
        elif num[-1] == "D":
          diff = square.r - self.numbers[int(num[:-1])][0]          
        let = answer[0][diff]
        prob = answer[1]
        square.letters[let] = square.letters.get(let, 0) + prob


  # Normalizes letter probabilites
  def normalizeLetterProbs(self, saff):
    for s in saff:
      total = sum([s.letters[let] for let in s.letters])
      if total > 0:
        for let in s.letters:
          s.letters[let] = s.letters[let] / total


  # Fills in certain letters (top n)
  # Returns False if it runs out of stuff to fill
  # Also returns a list of the numbers that were affected
  def fixLetters(self, n):
    topLets = []
    for r in range(self.size):
      for c in range(self.size):
        s = self.grid[r][c]
        let = s.getTop()
        if let != '-':
          topLets.append([s.letters[let], s, let])
    topLets.sort(reverse = True)
    affected = []
    i = 0
    done = 0
    while done < n:
      if i >= len(topLets):
        return False, None
      if topLets[i][1].letter == '-':
        topLets[i][1].letter = topLets[i][2]
        affected += self.affectedNumbers(topLets[i][1].r, topLets[i][1].c)
        done += 1
      i += 1
    return True, set(affected)


  # Resets letter dictionaries (so all letter probs are 0)
  def reset(self, affected):
    for square in affected:
      square.letters = {}


############################################################################
### Fill grid iteratively by combining letter probability into word prob.

  def combo(self, verbose = 0):
    print "Filling..."
    good = True
    affected = self.possAnswers.keys()
    saff = self.allSquares(affected)
    while good and not self.isFull():
      self.fillLetterProbs(saff)    # Uses word prob to fill letter prob
      self.normalizeLetterProbs(saff)   # Normalize letter prob for each square
      extended = self.allAffected(saff)
      self.updateWordProbs(extended)
      self.normalizeWordProbs(extended)
      good, affected = self.fixWords(1)
      if verbose:
        print self
      if not good:
        break      
      saff = self.allSquares(affected)
      self.eliminate(affected)          # Eliminates words that conflict with grid
      self.reset(saff)                  # Reset letter prob
      self.normalizeWordProbs(affected) # Normalize word prob for each num


  # Update word probs based on letters
  def updateWordProbs(self, extended):
    for num in extended:
      newAns = []
      for ans in self.possAnswers[num]:
        oldProb = self.origAnswers[num][ans[0]]
        prob = self.updateWord(num, ans[0], oldProb)
        newAns.append([ans[0], prob])
      newAns.sort(key=itemgetter(1), reverse=True)
      self.possAnswers[num] = newAns


  # Given a number and a word, updates word's probs using letters
  def updateWord(self, num, string, prob):
    s = self.squares(num)
    i = 0
    for current in s:
      if current.letter != string[i]:
        prob = prob * current.letters[string[i]]
      i += 1
    return prob


############################################################################

# Counts letters that are the same between two grids
def compare(a, b):
  if a.size != b.size:
    return 0
  tp = 0 # correct letter
  fp = 0 # incorrect letter
  fn = 0 # blank
  for r in range(a.size):
    for c in range(a.size):
      if not a.grid[r][c].black:
        if a.grid[r][c].letter.lower() == b.grid[r][c].letter.lower():
          tp += 1
        elif a.grid[r][c].letter == '-' or b.grid[r][c].letter == '-':
          fn += 1
        else:
          fp += 1
  return tp, fp, fn

# Calculates precision, recall, and percent correct
def score(guess, answer):
  tp, fp, fn = compare(guess, answer)
  precision = 100.0 * tp / (tp + fp) # tp / everything answered
  recall = 100.0 * tp / (tp + fn) # tp / correct + blanks
  pc = 100.0 * tp / (fp + fn + tp) # tp / everything
  return precision, recall, pc

def main():
  puz = "../puz/Nov1912.puz"
  
  c, b, cluesList = readPuz(puz)
  #print cluesList
  print c
  #c.printEmpty()

  #"""
  print "Searching for possible answers..."
  g = FillGrid(puz)
  g.getPossibleAnswers()
  g.normalizeWordProbs(g.possAnswers.keys())
  pickle.dump(g, open("grid.p", "wb"))
  #""" 
  #o = pickle.load(open("grid.p", "rb"))
  #o.printClues()
  
  #"""
  g = copy.deepcopy(o)
  g.fillLetters(1)
  print "\nFillLetters:"
  print g
  p, r, pc = score(g, c)
  print "Precision:", p, "Recall:", r, "Percent correct:", pc
  #"""
  #"""
  g = copy.deepcopy(o)
  g.fillWords(1)
  print "\nFillWords:"
  print g
  p, r, pc = score(g, c)
  print "Precision:", p, "Recall:", r, "Percent correct:", pc
  #"""
  #"""
  g = copy.deepcopy(o)
  g.combo(1)
  print "\nCombo:"
  print g
  p, r, pc = score(g, c)
  print "Precision:", p, "Recall:", r, "Percent correct:", pc
  #"""


if __name__=="__main__":
  main()
