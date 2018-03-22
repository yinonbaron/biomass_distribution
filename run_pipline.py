import numpy as np
from os import listdir
from os.path import isfile, join, isdir
print([f for f in listdir('.') if isdir(join('.',f))])