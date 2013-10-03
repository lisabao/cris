from fill import *

def runExp(day, date):

  month = "Nov"

  f = open("../results/" + day + ".txt", "w")

  for i in range(5):
    if len(date) == 1:
      date = '0' + date
    puz = "../puz/" + month + str(date) + "12.puz"
    f.write("\n\n" + day + " " + month + " " + date + "\n")
    print day, month, date
    
    c, b, cluesList = readPuz(puz)
    #f.write(str(c) + "\n")
    
    o = FillGrid(puz)
    o.getPossibleAnswers()
    o.normalizeWordProbs(o.possAnswers.keys())
    
    g = copy.deepcopy(o)
    g.fillLetters()
    f.write("\nFillLetters: ")
    #f.write(str(g) + "\n")
    p, r, pc = score(g, c)
    f.write("Precision: " + str(p) + " Recall: " + str(r) + " Percent correct:" + str(pc) + "\n")

    g = copy.deepcopy(o)
    g.fillWords()
    f.write("\nFillWords: ")
    #f.write(str(g) + "\n")
    p, r, pc = score(g, c)
    f.write("Precision: " + str(p) + " Recall: " + str(r) + " Percent correct:" + str(pc) + "\n")

    g = copy.deepcopy(o)
    g.combo()
    f.write("\nCombo: ")
    #f.write(str(g) + "\n")
    p, r, pc = score(g, c)
    f.write("Precision: " + str(p) + " Recall: " + str(r) + " Percent correct:" + str(pc) + "\n")

    if day == "thur" and date == '15':
      date = '22'
    date = str(int(date) + 7)
    if int(date) > 30:
      date = str(int(date) - 30)
      month = "Dec"

def main():
  runExp("mon", "12")
  runExp("tue", "13")
  runExp("wed", "14")
  runExp("thur", "08")
  runExp("fri", "16")
  runExp("sat", "17")

if __name__=="__main__":
  main()
