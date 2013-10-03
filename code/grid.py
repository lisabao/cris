"""
A grid class storing the dimensions and layout of a grid, any letters
in it, and that allows access to different numbers

The grid is an array of arrays. So g[r][c] is row r, column c.

Stored in the array are Square objects that can hold letters
and have info about numbers. Part of the Grid class is a function for
accessing a certain answer.

"""

class Square:

  def __init__(self, r = 0, c = 0, black = False, number = None, letter = "-"):
    self.black = black
    self.letter = letter
    self.number = number
    self.r = r
    self.c = c

  # regardless of any letters, returns the number or star for black
  def printEmpty(self):
    if self.black:
      return "*"
    elif self.number != None:
      return str(self.number)
    else:
      return "-"
    
  def __repr__(self):
    if self.black:
      return "*"
    else:
      return self.letter

class Grid:

  def __init__(self, size, contents): # contents is string
    self.size = size
    self.numbers = {} # key: numbers, value: [row, column] of that number
    self.clues = {} # key: number + "A" or "D", value: clue
    self.grid = self.buildGridString(contents)
    self.number()

  # Builds grid from a string of "-" for blank and "." for black
  def buildGridString(self, contents):
    if len(contents) != self.size * self.size:
      print "Error: mistmatch between grid size and grid array"

    grid = []
    for r in range(self.size):
      row = []
      for c in range(self.size):
        if contents[c] == ".":
          s = Square(r, c, True)
        else:  
          s = Square(r, c)
          s.letter = contents[c]
        row.append(s)
      grid.append(row)
      contents = contents[self.size:]
    return grid

  # Given a list of clues, in order by number with acrosses first and then downs,
  # puts them in the clues dictionary
  def addClues(self, clueList):
    i = 0
    num = 1
    while i < len(clueList):
      coord = self.numbers[num]
      r, c = coord[0], coord[1]
      if c==0 or self.grid[r][c-1].black:
        self.clues[str(num) + "A"] = clueList[i]
        i += 1
      if r==0 or self.grid[r-1][c].black:
        self.clues[str(num) + "D"] = clueList[i]
        i += 1
      num += 1

  # Figure out which numbers go where and assign them
  def number(self):
    i = 1
    for r in range(self.size):
      for c in range(self.size):
        if not self.grid[r][c].black and (r == 0 or c == 0 or \
            self.grid[r - 1][c].black or self.grid[r][c - 1].black):
          self.grid[r][c].number = i
          self.numbers[i] = [r, c]
          i += 1


  # Prints an empty grid to show numbers
  def printEmpty(self):
    s = " " + "---" * self.size + "\n"
    for r in range(self.size):
      s += "|"
      for c in range(self.size):
        char = self.grid[r][c].printEmpty()
        if len(char) == 1:
          char += " "
        s += char + " "
      s += "|"
      s += "\n"
    s += " " + "---" * self.size + "\n"
    print s

  # Print current grid with letters and no numbers
  def __repr__(self):
    s = "-" * (self.size + 1) * 2 + "\n"
    for r in range(self.size):
      s += "|"
      for c in range(self.size):
        s += str(self.grid[r][c]) + " "
      s += "|"
      s += "\n"
    s += "-" * (self.size + 1) * 2
    return s

  # Prints the clues in order
  # TODO: Fix so it prints in the right order 
  def printClues(self):
    clueList = self.clues.items()
    across = [clue for clue in clueList if clue[0][-1] == 'A']
    down = [clue for clue in clueList if clue[0][-1] == 'D']
    across.sort()
    down.sort()
    print "Across:"
    for clue in across:
      print clue[0], clue[1]
    print "Down:"
    for clue in down:
      print clue[0], clue[1]

  # Checks if all squares have been filled in
  def isFull(self):
    for r in range(self.size):
      for c in range(self.size):
        s = self.grid[r][c]
        if not s.black and s.letter == '-':
          return False
    return True


  # Given a list of squares, returns a list of all numbers intersecting them
  def allAffected(self, sList):
    a = []
    for s in sList:
      a += self.affectedNumbers(s.r, s.c)
    return set(a)


  # Given coordinates, returns a list of the two answers intersecting there
  def affectedNumbers(self, r, c):
    ccol = c
    while not self.grid[r][ccol - 1].black and ccol > 0:
      ccol -= 1
    a = str(self.grid[r][ccol].number) + "A"

    crow = r
    while not self.grid[crow - 1][c].black and crow > 0:
      crow -= 1
    d = str(self.grid[crow][c].number) + "D"

    return [a, d]


  # Given a list of numbers, returns a set of squares covered by those numbers
  def allSquares(self, numList):
    s = []
    for num in numList:
      s += self.squares(num)
    return set(s)


  # Given a number, returns each square covered by that number
  def squares(self, num):
    number = int(num[:-1])
    direction = num[-1]
    location = self.numbers[number]
    row = location[0]
    col = location[1]
    current = self.grid[row][col]
    squares = []

    if direction == "A" or direction == "a":
      ccol = col
      while ccol < self.size and not current.black:
        squares.append(current)
        ccol += 1
        if ccol < self.size:
          current = self.grid[row][ccol]

    elif direction == "D" or direction == "d":
      crow = row
      while crow < self.size and not current.black:
        squares.append(current)
        crow += 1
        if crow < self.size:
          current = self.grid[crow][col]

    return squares

  # Given a number, returns a string of the current letters
  def readAnswer(self, num):
    squares = self.squares(num)
    s = ""
    for square in squares:
      s += square.letter
    return s

  # Given a number, fills in as much of the string as will fit
  def fillAnswer(self, num, string):
    squares = self.squares(num)
    i = 0
    for square in squares:
      if i >= len(string):
        break
      square.letter = string[i]
      i += 1
     

def main():
  g = Grid(4, '------.--.------')
  print g
  g.printEmpty()
  g.fillAnswer("1A", "THAW")
  g.fillAnswer("4A", "AG")
  g.fillAnswer("5A", "QI")
  g.fillAnswer("6A", "LETT")
  g.fillAnswer("1D", "TALL")
  g.fillAnswer("2D", "HG")
  g.fillAnswer("3D", "WRIT")
  g.fillAnswer("5D", "QT")
  #g.fillAnswer("3A", "TEST") # not a real clue
  print g
  print "1D:", g.readAnswer("1A"), len(g.readAnswer("1A"))
  #"""


if __name__=='__main__':
    main()

    
