for i in range(3, 16):
  c = open(str(i) + ".txt", "r")
  d = {}
  for line in c:
    l = line.split(",")
    d[l[0]] = 1
  print i, len(d)
