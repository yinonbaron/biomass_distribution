import numpy as np
import fnmatch
import os

def sortedWalk(top, topdown=True, onerror=None):
    from os.path import join, isdir, islink
 
    names = os.listdir(top)
    names.sort(key=lambda v: v.upper())
    dirs, nondirs = [], []
 
    for name in names:
        if isdir(os.path.join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)
 
    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        path = join(top, name)
        if not os.path.islink(path):
            for x in sortedWalk(path, topdown, onerror):
                yield x
    if not topdown:
        yield top, dirs, nondirs


matches = []
for root, dirnames, filenames in sortedWalk('.',topdown=False):
    #root.sort()
    for filename in fnmatch.filter(filenames, '*.ipynb'):
        if 'checkpoint' in filename:
            continue
        print(os.path.join(root, filename))
        matches.append(os.path.join(root, filename))

#print(matches.__contains__('checkpoint'))
#matches = [f for f in matches if 'checkpoint' not in f]
#print(matches)
os.system('jupyter nbconvert --to notebook --execute ' + matches[0])

