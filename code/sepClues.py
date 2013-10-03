# Read the clues file and separate by answer length

def main():
  f = open("clues.csv", "r")
  files = [0, 0, 0] # filler for easier indexing
  for i in range(3, 16):
    path = "clues/" + str(i) + ".txt"
    n = open(path, "w")
    files.append(n)
  
  for line in f:
    l = line.split(",", 1)
    length = len(l[0])
    if length <= 15: # exclude Sunday puzzles
      files[length].write(line)
    

main()

