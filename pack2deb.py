import os
for f in os.listdir("outputs"):
  os.system("cd outputs/ && dpkg -b " + f)
